import asyncio
from contextlib import asynccontextmanager
import aiomysql
from fastapi import FastAPI, HTTPException, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
import os
from typing import List, Dict, Any, Optional

import logging
from fastapi import FastAPI

from src.db_api.pet import FilteredPetData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

pet_api = None

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    global pet_api
    #await asyncio.sleep(5)  # Chờ 5 giây
    try:
        # Create PetAPI instance first
        pet_api = PetAPI()
        # Connect database
        await pet_api.connect_pool()
        logger.info("Database connection initialized")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

class PetAPI:
    def __init__(self):
        self.pool = None
    
    async def connect_pool(self):
        """Initialize database and redis connection pools"""
        if not self.pool:
            # Connect MySQL
            self.pool = await aiomysql.create_pool(
                # host=os.getenv('DB_HOST'),
                # port=int(os.getenv('3309')),
                # user=os.getenv('root'),
                # password=os.getenv('root'),
                # db=os.getenv('local_db'),
                # autocommit=True
                host=os.getenv('DB_HOST', '127.0.0.1'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'root'),
                db=os.getenv('DB_NAME', 'pet_db'),
                autocommit=True
            )
    
    async def close_pool(self):
        """Close the database connection pool."""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
            logger.info("MySQL connection pool closed")


@app.get("/health")
async def health_check():
    try:
        # Kiểm tra kết nối MySQL
        async with pet_api.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
                await cur.fetchone()
        
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

#/api/pet/bulk  
@app.post("/api/pet/bulk")
async def insert_pet_bulk(raw_data_list: List[FilteredPetData]):
    """Insert bulk pet data - both raw and processed"""
    try:
        async with  pet_api.pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Insert raw data
                await cur.executemany("""
                    INSERT INTO pets 
                    (id, list_time, list_time_sec, subject, param_value, 
                    price_string, price, area_name, date_string, seller_name, 
                    average_rating, sold_ads, image_url, category_name)
                    VALUES (%(id)s, %(list_time)s, %(list_time_sec)s, %(subject)s, %(param_value)s,
                            %(price_string)s, %(price)s, %(area_name)s, %(date_string)s, %(seller_name)s,
                            %(average_rating)s, %(sold_ads)s, %(image_url)s, %(category_name)s)
                    ON DUPLICATE KEY UPDATE
                        list_time = VALUES(list_time),
                        list_time_sec = VALUES(list_time_sec),
                        subject = VALUES(subject),
                        param_value = VALUES(param_value),
                        price_string = VALUES(price_string),
                        price = VALUES(price),
                        area_name = VALUES(area_name),
                        date_string = VALUES(date_string),
                        seller_name = VALUES(seller_name),
                        average_rating = VALUES(average_rating),
                        sold_ads = VALUES(sold_ads),
                        image_url = VALUES(image_url),
                        category_name = VALUES(category_name)
                """, [data.model_dump() for data in raw_data_list])
                
                return {
                    "message": "Bulk insert successful",
                    "count": len(raw_data_list)
                }

    except Exception as e:
        logger.error(f"Error bulk inserting pet data: {e}")
        raise HTTPException(status_code=500, detail=str(e))  

@app.get("/api/pet")
async def get_pet_data(
    page: int = Query(..., gt=0),
    size: int = Query(..., gt=0, le=100),
    filter: Optional[str] = "",
    search: Optional[str] = ""
):
    """Get pet data with pagination and optional filtering/search"""
    try:
        conditions = []
        values = []

        if filter:
            conditions.append("category_name = %s")
            values.append(filter)
        if search:
            conditions.append("subject LIKE %s")
            values.append(f"%{search}%")

        where_clause = " AND ".join(conditions)
        sql = "SELECT * FROM pets"
        if where_clause:
            sql += " WHERE " + where_clause
        sql += " LIMIT %s OFFSET %s"

        values.extend([size, (page - 1) * size])

        async with pet_api.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, tuple(values))
                result = await cur.fetchall()

        return {
            "message": "Data retrieved successfully",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error retrieving pet data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)