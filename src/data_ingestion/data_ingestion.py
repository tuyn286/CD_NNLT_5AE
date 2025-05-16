import os
import sys
import json
import aiohttp
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiofiles
import pandas as pd
from filelock import FileLock
from dotenv import load_dotenv

sys.path.append(".")
from src.logger import logger

# Load environment variables
load_dotenv()

class DataIngrestion:
    def __init__(self):
        """Initialize DataIngestion"""
        self.api_url = os.getenv('DB_API_URL')
        self.scheduler = AsyncIOScheduler()
        self.data_path = os.getenv('DATA_PATH', 'data')
        self.data_file = f"{self.data_path}/pets_data.json"
        self.processed_file = f"{self.data_path}/processed_data.json"
        self.session = None
        # Create the data directory if it does not exist
        os.makedirs(self.data_path, exist_ok=True)
        # Initialize files
        self._init_files()
    
    #Create file processed_data.json if not exist
    def _init_files(self):
        if not os.path.exists(self.processed_file):
            with open(self.processed_file, 'w') as f:
                json.dump({"last_processed_dt": 0}, f)
           
    #Load data from JSON file     
    async def load_pet_data(self):
        """Load pet data from file"""
        lock = FileLock(f"{self.data_file}.lock")
        
        try:
            with lock:
                if not os.path.exists(self.data_file):
                    logger.warning(f"Data file {self.data_file} not found")
                    return []

                async with aiofiles.open(self.data_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    if not content:
                        logger.warning("Data file is empty")
                        return []
                        
                    data = json.loads(content)
                    logger.info(f"Loaded {len(data)} pet records")
                    return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading pet data: {e}")
            return []
        
    @staticmethod
    def convert_to_vietnam_time(utc_timestamp_ms: int) -> int:
        """
        Convert UTC timestamp in milliseconds to Vietnam time in milliseconds
        """
        VIETNAM_OFFSET_MS = 25200000  # 7 hours * 3600 seconds * 1000 milliseconds
        return utc_timestamp_ms + VIETNAM_OFFSET_MS

    @staticmethod
    def ms_to_seconds(timestamp_ms: int) -> int:
        """
        Convert milliseconds timestamp to seconds timestamp
        """
        return timestamp_ms // 1000

    #Filter data JSON
    def filter_data(self, pet_data):
        """Only filter necessary fields while preserving null values"""
        try:
          
            utc_timestamp_ms = pet_data.get("list_time")
            
            # Convert to Vietnam time zone
            vietnam_timestamp_ms = self.convert_to_vietnam_time(utc_timestamp_ms)
            
            # You can choose to keep in milliseconds or convert to seconds
            vietnam_timestamp_sec = self.ms_to_seconds(vietnam_timestamp_ms)
            filtered_data = {
                "id": pet_data.get("ad_id"),
                "list_time": vietnam_timestamp_ms,  # Store in milliseconds to maintain original format
                "list_time_sec": vietnam_timestamp_sec,  # Also store in seconds if needed
                "subject": pet_data.get("subject"),
                "param_value": pet_data.get("params")[0].get("value"),
                "price_string": pet_data.get("price_string"),
                "price":pet_data.get("price"), 
                "area_name": pet_data.get("area_name"),
                "date_string": pet_data.get("date"),
                "seller_name": pet_data.get("seller_info").get("full_name"),
                "average_rating": pet_data.get("average_rating"),
                "sold_ads": pet_data.get("seller_info").get("sold_ads"),
                "image_url":pet_data.get("image"),
                "category_name": pet_data.get("category_name")
            }
            return filtered_data
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return None
        
    async def _load_processed_data(self):
        """
        Load the last processed timestamp from file
        """
        try:
            async with aiofiles.open(self.processed_file, 'r') as f:
                content = await f.read()
                return json.loads(content)
        except Exception as e:
            logger.error(f"Error loading processed data: {e}")
            return {"last_processed_dt": 0}
    
    async def _save_processed_data(self, data: dict):
        """
        Save the last processed timestamp to file
        """
        try:
            async with aiofiles.open(self.processed_file, 'w') as f:
                await f.write(json.dumps(data))
                await f.flush()
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise
    
    #CALL API DB
    async def send_to_api(self, raw_data_list: list):
        """Send bulk data to API"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        try:
            if not self.api_url:
                raise ValueError("API URL is not set")

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            logger.info(f"Sending bulk data with {len(raw_data_list)} entries")

            async with self.session.post(
                f"{self.api_url}/db/api/pet/bulk",
                json=raw_data_list,
                headers=headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Successfully saved {result['count']} entries")
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Failed to send bulk data: {response.status}, error: {error}")
                    return False

        except Exception as e:
            logger.error(f"Error sending bulk data to API: {e}")
            return False
        
    #Ingest
    async def ingest(self, is_initial_run: bool = False):
        try:
            pet_data = await self.load_pet_data()
            if not pet_data:
                if is_initial_run:
                    logger.info("No pet data found during initial run")
                else:
                    logger.info("No pet data found during scheduled check")
                return

            # Get last processed timestamp
            processed_data = await self._load_processed_data()
            last_processed_dt = processed_data.get("last_processed_dt", 0)

            if is_initial_run:
                logger.info(f"Initial run - Last processed timestamp: {last_processed_dt}")
            else:
                logger.info(f"Checking for data newer than: {last_processed_dt}")

            # Filter only new data
            raw_data_list = []
            latest_dt = last_processed_dt
            
            # Bên trong ingest()
            ads_list = pet_data.get("ads")

            if not ads_list or not isinstance(ads_list, list):
                logger.warning(f"No 'ads' list found in loaded data or 'ads' is not a list.")
                # Xử lý tiếp logic báo không có data mới nếu cần (như ở cuối hàm)
                # ... (phần này sẽ được xử lý bởi khối `if final_filtered_ads_list:` bên dưới)
            else:
                logger.info(f"Found {len(ads_list)} ad objects in the 'ads' list.") # Log số lượng ad objects thực sự
                for ad_object in ads_list: 
                    filtered_item = self.filter_data(ad_object) # filter_data nhận một ad_object
                    if filtered_item and filtered_item.get("list_time") is not None and filtered_item["list_time"] > last_processed_dt:
                        raw_data_list.append(filtered_item)
                        latest_dt = max(latest_dt, filtered_item["list_time"])

            if raw_data_list:
                count = len(raw_data_list)
                if is_initial_run:
                    logger.info(f"Initial run - Found {count} entries to process")
                else:
                    logger.info(f"Found {count} new entries to process")

                # Send new data to API
                success = await self.send_to_api(raw_data_list)
                
                if success:
                    await self._save_processed_data({"last_processed_dt": latest_dt})
                    if is_initial_run:
                        logger.info(f"Initial run - Successfully processed {count} entries")
                    else:
                        logger.info(f"Successfully processed {count} new entries")
                else:
                    logger.error("Failed to send bulk data")
            else:
                if is_initial_run:
                    logger.info("Initial run - No new data to process")
                else:
                    logger.info("No new data to process")

        except Exception as e:
            if is_initial_run:
                logger.error(f"Error during initial ingestion: {e}")
            else:
                logger.error(f"Error during scheduled ingestion: {e}")
            logger.exception("Full traceback:")
        
    async def start(self):
        """Start the Pet Data Ingestion service"""
        try:
            logger.info("Starting Pet Data Ingestion service")
            
            # First run - process all existing data
            await self.ingest(is_initial_run=True)
            
            # Schedule future runs 2 minutes
            logger.info("Adding scheduled job for pet ingestion every 2 minutes")
            self.scheduler.add_job(
                self.ingest,
                'interval',
                minutes=2,
                id='pet_data_ingestion'
            )
            
            self.scheduler.start(paused=False)

            # Đảm bảo giữ scheduler chạy bằng asyncio event loop chuẩn
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Error starting service: {e}")
            await self.stop()
            
    async def stop(self):
        try:
            self.scheduler.shutdown()
            if self.session:
                await self.session.close()
            logger.info("Pet Data Ingestion service stopped")
        except Exception as e:
            logger.error(f"Error stopping service: {e}")
    
async def main():
    service = DataIngrestion()
    await service.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
