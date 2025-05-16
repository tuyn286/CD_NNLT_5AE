# **Ho Chi Minh Pets**

A comprehensive project for gathering pet data in Ho Chi Minh using ChoTot API. This system automates data ingestion, storage.

---

## **Project Overview**
This project aims to build a data pipeline for pet data in Ho Chi Minh, from data collection to advanced analysis and prediction. Key features include:
- **Data Ingestion**: Collects data every 2 minutes from ChoTot API.
- **Database Management**: Stores raw and processed pet data.
- **Front-End Interface**: A Vuejs-based web interface to visualize and explore pet data.

---

## **Features**
1. **Data Ingestion**
   - Periodically fetches pet data from ChoTot API every 2 minutes.
   - Stores raw pet data in a MySQL database.
   - Logs and handles errors during data collection.
2. **Database API**
3. **Visualization**
   - A Vuejs-based front-end interface to visualize pet trends and insights.
   - Filters and Searching of pet data.

---

## **Technologies Used**
- **Programming Languages**: Python, JavaScript (Vuejs)
- **Frameworks**: 
  - Backend: FastAPI (API development)
  - Frontend: Vuejs (for building user interfaces)
  - Docker/Docker Compose (Containerization)
- **Databases**: MySQL
- **Libraries**:
  - Pandas, NumPy (Data Processing)
- **APIs**: ChoTot API
- **API GateWay**: NGINX



---

## **System Architecture**

- **Data Source**: ChoTot API
- **Data Ingestion**: Collects and stores raw pet data.
- **Database API**: Handles interaction with the database.
- **Front End**: React-based interface to display pet insights in a user-friendly format.
- **API GateWay**: NGINX API Gateway receives all the requests from the client and routing to the corresponding     microservices.
---

## **Initialization**
The database tables are initialized using an SQL script located in `mysql/init_db/`. When the MySQL container starts, this script is executed automatically.

To initialize manually:
```bash
docker exec -i mysql_container_name mysql -u root -pet_db < src/init_db/init.sql
```
---

## **Folder Structure**
```plaintext
project/
├── configs
├── data
├── logs
├── nginx
│   ├── conf.d
│   └── logs
└── src
│   ├── crawl_data/
│   ├── data_ingestion/
│   ├── db_api/
│   ├── front_end
│   │   ├── .vscode
│   │   └── src
│   │       ├── components/
│   │       ├── router/
│   │       └── views/
│   └── init_db/
│       
├── docker-compose.yml  
├── .gitignore              
├── README.md               
└── requirements.txt        
```
---

## **Getting Started**

### **System Requirements**
- **Python** >= 3.10
- **Node.js** >= 20.x (for Vuejs frontend)
- **Docker** and **Docker Compose**
- **MySQL**
---

### **Configuration**

1. Create a `.env` file based on the template:
   ```bash
   cp .env.example .env
   ```
   Edit the .env file with the necessary configuration information.
---

### **Start the Project**
1. Start all services using Docker Compose:
    ```bash
    docker-compose up --build
    ```
2. The project will run at:
    - Frontend: http://localhost:3000
    - API: http://localhost:8000
    - Crawl: http://localhost:8080
    - NGINX: http://localhost:8088
---



### **Processing Schedule**
- Data Crawling: Every 3 minutes
- Data Collection: Every 2 minutes.