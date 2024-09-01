from sqlalchemy.orm import Session
from app.database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import random


class ACrawlerData(Base):
    __tablename__ = "a_crawler_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(String)


Base.metadata.create_all(bind=engine)


def run_a_crawler(db: Session):
    new_data = ACrawlerData(value=f"A-{random.randint(1, 100)}")
    db.add(new_data)
    db.commit()
    print(f"A 크롤러 실행: {new_data.value}")
