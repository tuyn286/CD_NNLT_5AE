CREATE DATABASE IF NOT EXISTS pet_db;
USE pet_db;
-- Create pet data table
CREATE TABLE IF NOT EXISTS pets (
  id INT NOT NULL,                         -- Từ pet_data.get("ad_id")
  list_time BIGINT NULL,                   -- Từ pet_data.get("list_time"), đơn vị milliseconds, đã chuyển sang giờ Việt Nam
  list_time_sec BIGINT NULL,               -- Đã chuyển sang giờ Việt Nam và đơn vị seconds
  subject VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("subject")
  param_value VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("params")[0].get("value") (cần xem lại key "param" hay "params" trong code Python)
  price_string VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("price_string")
  price BIGINT UNSIGNED NULL,                -- Từ pet_data.get("price"), giả sử giá không âm
  area_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("area_name")
  date_string VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("date"), ví dụ: "8 phút trước"
  seller_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("seller_info").get("fullname")
  average_rating DECIMAL(2,1) NULL,        -- Từ pet_data.get("average_rating"), ví dụ: 4.5
  sold_ads INT UNSIGNED NULL,              -- Từ pet_data.get("seller_info").get("sold_ads"), không âm
  image_url VARCHAR(2048) NULL,            -- Từ pet_data.get("image")[0] hoặc pet_data.get("image") (cần xem lại logic trích xuất trong Python)
  category_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, -- Từ pet_data.get("category_name")
  
  PRIMARY KEY (id)
);