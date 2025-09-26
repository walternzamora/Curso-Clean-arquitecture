# app/infrastructure/config/mysql.py
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path

# carga .env si existe
env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(env_path)

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "clean_arch"),
}

DDL_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;
"""

def get_conn():
    return mysql.connector.connect(**MYSQL_CONFIG)

def init_db():
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(DDL_PRODUCTS)
        conn.commit()
    finally:
        conn.close()
