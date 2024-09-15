from fastapi import FastAPI, Depends
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import get_db, WaterQuality
from services.water_quality_crawler import fetch_water_quality_data

# from app.services.a_crawler import run_a_crawler, ACrawlerData
# from app.services.b_crawler import run_b_crawler, BCrawlerData
# from app.services.c_crawler import run_c_crawler, CCrawlerData

app = FastAPI()


def run_crawler(crawler_func):
    db = next(get_db())
    try:
        crawler_func(db)
    finally:
        db.close()


scheduler = BackgroundScheduler()
# scheduler.add_job(lambda: run_crawler(run_a_crawler), "interval", minutes=1)
# scheduler.add_job(lambda: run_crawler(run_b_crawler), "interval", minutes=5)
# scheduler.add_job(lambda: run_crawler(run_c_crawler), "interval", minutes=30)
scheduler.add_job(lambda: run_crawler(fetch_water_quality_data), "interval", hours=1)
scheduler.start()


@app.on_event("startup")
async def startup_event():
    # run_crawler(run_a_crawler)
    # run_crawler(run_b_crawler)
    # run_crawler(run_c_crawler)
    run_crawler(fetch_water_quality_data)


# @app.get("/a")
# async def get_a_data(db: Session = Depends(get_db)):
#     data = (
#         db.query(ACrawlerData).order_by(ACrawlerData.timestamp.desc()).limit(10).all()
#     )
#     return [{"timestamp": item.timestamp, "value": item.value} for item in data]


# @app.get("/b")
# async def get_b_data(db: Session = Depends(get_db)):
#     data = (
#         db.query(BCrawlerData).order_by(BCrawlerData.timestamp.desc()).limit(10).all()
#     )
#     return [{"timestamp": item.timestamp, "value": item.value} for item in data]


# @app.get("/c")
# async def get_c_data(db: Session = Depends(get_db)):
#     data = (
#         db.query(CCrawlerData).order_by(CCrawlerData.timestamp.desc()).limit(10).all()
#     )
#     return [{"timestamp": item.timestamp, "value": item.value} for item in data]


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


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
