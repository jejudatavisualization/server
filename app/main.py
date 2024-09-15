from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import get_db, WaterQuality
from services.water_quality_crawler import fetch_water_quality_data
import os
import csv
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "http://jejudata.com/"으로 추후 변경
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


def run_crawler(crawler_func):
    db = next(get_db())
    try:
        crawler_func(db)
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(lambda: run_crawler(fetch_water_quality_data), "interval", hours=1)
scheduler.start()


@app.on_event("startup")
async def startup_event():
    run_crawler(fetch_water_quality_data)


@app.get("/water_quality")
async def get_water_quality_data(db: Session = Depends(get_db)):
    data = (
        db.query(WaterQuality).order_by(WaterQuality.timestamp.desc()).limit(10).all()
    )
    return [
        {
            "timestamp": item.timestamp,
            "place_code": item.place_code,
            "measure_time": item.measure_time,
            "organic": item.organic,
            "organic_status": item.organic_status,
            "suspended": item.suspended,
            "suspended_status": item.suspended_status,
            "total_p": item.total_p,
            "total_p_status": item.total_p_status,
            "total_n": item.total_n,
            "total_n_status": item.total_n_status,
            "comm_disorder": item.comm_disorder,
        }
        for item in data
    ]


# CSV 파일을 JSON으로 변환하는 함수
def csv_to_json(csv_file_path):
    encodings = ["utf-8", "cp949", "euc-kr"]
    for encoding in encodings:
        try:
            with open(csv_file_path, "r", encoding=encoding) as csvfile:
                csvreader = csv.DictReader(csvfile)
                data = [row for row in csvreader]
            return data
        except UnicodeDecodeError:
            continue
    raise HTTPException(
        status_code=500, detail="Unable to decode the file with available encodings"
    )


# 데이터 디렉토리 경로
data_dir = os.path.join(os.path.dirname(__file__), "data")


@app.get("/crime_data")
async def get_crime_data():
    file_path = os.path.join(data_dir, "crime.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return csv_to_json(file_path)


@app.get("/energy_data")
async def get_energy_data():
    file_path = os.path.join(data_dir, "energy_info.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return csv_to_json(file_path)


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
