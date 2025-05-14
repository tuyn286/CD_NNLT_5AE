from dotenv import load_dotenv
import os
import json
import aiohttp
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import aiofiles
import sys
from datetime import datetime, timedelta, timezone
from filelock import FileLock
sys.path.append(".")
from src.logger import logger
from fastapi import FastAPI
import asyncio

# Load environment variables
load_dotenv()

# Load constants from environment variables
BASE_URL = os.getenv('BASE_UR',"https://gateway.chotot.com/v1/public/ad-listing")

app = FastAPI()

class PetCrawler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.data_dir = "data"
        self.data_file = os.path.join(self.data_dir, "pets_data.json")
        self.session = None
        self._init_data_file() # Create data directory if it does not exist, # Create JSON file if it does not exist
    
        
    def _init_data_file(self):
        """Initialize data directory and file if they don't exist"""
        # Create data directory if it does not exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create JSON file if it does not exist
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
                 
    # Read data from json file
    async def load_pet_data(self):
        """Load existing pet data with proper UTF-8 encoding"""
        try:
            async with aiofiles.open(self.data_file, 'r', encoding='utf-8', errors='replace') as file:
                content = await file.read()
                data = json.loads(content)
                logger.info(f"Loaded {len(data)} existing records")
                return data
        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.data_file}")
            return []
        except json.JSONDecodeError as e:
            # Backup corrupted file instead of losing data
            backup_file = f"{self.data_file}.corrupted"
            logger.error(f"JSON decode error. Backing up to {backup_file}")
            os.rename(self.data_file, backup_file)
            return []
        except Exception as e:
            logger.error(f"Error loading pet data: {e}")
            return []
    
    async def save_pet_data(self, data):
        """Save raw pet data to JSON file with proper UTF-8 encoding"""
        backup_file = None
        lock = FileLock(f"{self.data_file}.lock")
        
        try:
            with lock:
                
                # Create backup before saving new data
                if os.path.exists(self.data_file):
                    backup_file = f"{self.data_file}.bak"
                    async with aiofiles.open(self.data_file, 'r', encoding='utf-8', errors='replace') as src, \
                            aiofiles.open(backup_file, 'w', encoding='utf-8') as dst:
                        content = await src.read()
                        await dst.write(content)
                
                # Save to file with proper UTF-8 encoding
                async with aiofiles.open(self.data_file, 'w', encoding='utf-8') as file:
                    await file.write(json.dumps(data, indent=4, ensure_ascii=False))
                
                # Remove backup if save successful    
                if backup_file and os.path.exists(backup_file):
                    os.remove(backup_file)
                
                data_size = data['ads']

                
                logger.info(f"Successfully saved new data. Total records: {len(data_size)}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving pet data: {e}")
            # Restore from backup if save failed
            if backup_file and os.path.exists(backup_file):
                os.replace(backup_file, self.data_file)
                logger.info("Restored from backup file")
            return False
    
    
    
    #Open HTTP Connection CALL API
    async def init_session(self):
        """Initialize aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    #Close HTTP Connection
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    #Fetch data from API
    async def fetch_pet_data(self):
        retries = 0
        while retries < 5:
            try:
                await self.init_session()
                # Cấu hình params cho API Chợ Tốt
                params = {
                    "region_v2": 13000,     # Mã vùng
                    "cg": 12000,            # Danh mục chung
                    "f": "c",               # Trạng thái
                    "st": "s,k",            # Loại tin đăng
                    "limit":200,
                    "w": 1,
                    # "include_expired_ads":"true",                 
                    # "fingerprint": "29053124", # Dấu vân tay
                    "key_param_included": "true"    # Bao gồm các tham số chính
                }

                async with self.session.get(BASE_URL, params=params) as response:
                    if response.status == 429:  # Too Many Requests
                        logger.warning("API rate limit reached. Sleeping for 1 minute...")
                        await asyncio.sleep(60)
                        continue

                    response.raise_for_status()
                    data = await response.json()
                    logger.info("Successfully fetched pet data")
                    
                    # Only save if fetch was successful
                    if data and 'ads' in data and data['ads']:
                        await self.save_pet_data(data)
                        return data
                    else:
                        logger.error("Invalid data format received from API or no ads found.")
                        return None

            except aiohttp.ClientError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                if getattr(http_err, 'status', None) == 429:
                    logger.warning("API rate limit hit. Sleeping for 1 minute...")
                    await asyncio.sleep(60)
                else:
                    retries += 1
                    logger.warning(f"Retrying... ({retries}/{5})")
                    await asyncio.sleep(5)
    
        
    async def daily_job(self):
        """Job to fetch current pet data every x hour"""
        try:
            data = await self.fetch_pet_data()
            if data:
                logger.info("Pet data fetch completed successfully")
            else:
                logger.error("Failed to fetch Pet data")
        except Exception as e:
            logger.error(f"Error in hourly job: {e}")    
    
    def start_scheduler(self):
        """Start the scheduler for hourly jobs"""
        # Xóa tất cả các job cũ nếu có
        self.scheduler.remove_all_jobs()
        
        # Thêm job mới
        self.scheduler.add_job(
            self.daily_job,
            CronTrigger(hour='*/2', minute='5',timezone="Asia/Ho_Chi_Minh"),   # Run at minute 5 of every time call
            id='pet_crawler_job', # Đặt ID rõ ràng hơn
            replace_existing=True # Ghi đè job cũ nếu ID trùng
        )
        logger.info("Added Pet Crawler job (every 2 hours at xx:05) to scheduler")

        logger.info("Starting the scheduler...")
        self.scheduler.start()
        
    async def start(self):
        """Main function to start crawling and scheduling"""
        try:
            self.start_scheduler()
            
            # Giữ chương trình chạy
            while True:
                await asyncio.sleep(3600)  # Đợi 1 giờ
                
        except asyncio.CancelledError:
            logger.info("Crawler is shutting down...")
        except Exception as e:
            logger.error(f"Error while running crawler: {e}")
        finally:
            await self.close_session()
            if self.scheduler.running:
                self.scheduler.shutdown()
async def run_manual_crawl():
    """Hàm để chạy crawl thủ công một lần."""
    crawler = PetCrawler()
    try:
        logger.info("Starting manual crawl...")
        
        # Khởi tạo session HTTP (quan trọng)
        await crawler.init_session() 
        
        # Gọi trực tiếp hàm fetch và save dữ liệu
        logger.info("Fetching pet data manually...")
        fetched_data = await crawler.fetch_pet_data() 
        
        if fetched_data:
            # fetch_pet_data đã tự động lưu nếu thành công và có dữ liệu
            logger.info("Manual crawl successful. Data fetched and potentially saved.")
            # print(json.dumps(fetched_data, indent=4)) # In ra dữ liệu nếu cần xem
        else:
            logger.warning("Manual crawl finished, but no new data was fetched or saved.")
            
    except Exception as e:
        logger.error(f"An error occurred during manual crawl: {e}", exc_info=True)
    finally:
        # Luôn đóng session sau khi hoàn thành (quan trọng)
        logger.info("Closing HTTP session.")
        await crawler.close_session()
        logger.info("Manual crawl finished.")
       
# ----- API -----
@app.on_event("startup")
async def startup_event():
    crawler = PetCrawler()
    asyncio.create_task(crawler.start())

@app.get("/manual-crawl")
async def manual_crawl():
    await run_manual_crawl()
    return {"message": "Manual crawl started"}

# ----- Run -----
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("pet_crawl:app", host="0.0.0.0", port=8080, reload=True)
