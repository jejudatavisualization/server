from sqlalchemy.orm import Session
from app.database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import random


class CCrawlerData(Base):
    __tablename__ = "c_crawler_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(String)


Base.metadata.create_all(bind=engine)


def run_c_crawler(db: Session):
    new_data = CCrawlerData(value=f"C-{random.randint(1, 100)}")
    db.add(new_data)
    db.commit()
    print(f"C 크롤러 실행: {new_data.value}")
