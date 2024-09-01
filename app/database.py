from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class WaterQuality(Base):
    __tablename__ = "water_quality"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    place_code = Column(String)
    measure_time = Column(DateTime)
    organic = Column(Float)
    organic_status = Column(String)
    suspended = Column(Float)
    suspended_status = Column(String)
    total_p = Column(Float)
    total_p_status = Column(String)
    total_n = Column(Float)
    total_n_status = Column(String)
    comm_disorder = Column(String)


engine = create_engine("sqlite:///./jeju_data.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
