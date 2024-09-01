from sqlalchemy.orm import Session
from app.database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import random


class BCrawlerData(Base):
    __tablename__ = "b_crawler_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(String)


Base.metadata.create_all(bind=engine)


def run_b_crawler(db: Session):
    new_data = BCrawlerData(value=f"B-{random.randint(1, 100)}")
    db.add(new_data)
    db.commit()
    print(f"B 크롤러 실행: {new_data.value}")
