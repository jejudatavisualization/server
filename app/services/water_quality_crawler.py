import requests
from lxml import etree
from datetime import datetime
from sqlalchemy.orm import Session
from database import WaterQuality, get_db


def parse_date(date_string):
    return datetime.strptime(date_string, "%Y%m%d%H%M%S")


def fetch_water_quality_data(db: Session):
    url = (
        "http://211.184.196.130/rest/JejuSewerWaterQDataService/getJejuSewerWaterQData/"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()

        # XML 데이터 파싱
        decoded_content = response.content.decode("utf-8", errors="ignore")
        cleaned_content = decoded_content.strip()

        # lxml 파서로 재시도
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(cleaned_content.encode("utf-8"), parser=parser)

        timestamp = datetime.now()

        for list_element in root.findall(".//list"):
            try:
                water_quality = WaterQuality(
                    timestamp=timestamp,
                    place_code=(
                        list_element.find("PlaceCode").text
                        if list_element.find("PlaceCode") is not None
                        else None
                    ),
                    measure_time=(
                        parse_date(list_element.find("MeasureTime").text)
                        if list_element.find("MeasureTime") is not None
                        else None
                    ),
                    organic=(
                        float(list_element.find("Organic").text.strip())
                        if list_element.find("Organic") is not None
                        else None
                    ),
                    organic_status=(
                        list_element.find("Organic_Status").text
                        if list_element.find("Organic_Status") is not None
                        else None
                    ),
                    suspended=(
                        float(list_element.find("Suspended").text.strip())
                        if list_element.find("Suspended") is not None
                        else None
                    ),
                    suspended_status=(
                        list_element.find("Suspended_Status").text
                        if list_element.find("Suspended_Status") is not None
                        else None
                    ),
                    total_p=(
                        float(list_element.find("TotalP").text.strip())
                        if list_element.find("TotalP") is not None
                        else None
                    ),
                    total_p_status=(
                        list_element.find("TotalP_Status").text
                        if list_element.find("TotalP_Status") is not None
                        else None
                    ),
                    total_n=(
                        float(list_element.find("TotalN").text.strip())
                        if list_element.find("TotalN") is not None
                        else None
                    ),
                    total_n_status=(
                        list_element.find("TotalN_Status").text
                        if list_element.find("TotalN_Status") is not None
                        else None
                    ),
                    comm_disorder=(
                        list_element.find("CommDisorder").text
                        if list_element.find("CommDisorder") is not None
                        else None
                    ),
                )
                db.add(water_quality)
            except Exception as e:
                continue
        db.commit()
        print(f"Water quality data fetched and saved at {timestamp}")
    except Exception as e:
        print(f"Failed to fetch water quality data: {str(e)}")
        db.rollback()


# colab 전용 데이터
# import requests
# import csv
# import os
# from datetime import datetime
# from lxml import etree  # lxml 라이브러리 추가

# def fetch_data():
#     url = "http://211.184.196.130/rest/JejuSewerWaterQDataService/getJejuSewerWaterQData/"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
#     except requests.RequestException as e:
#         print(f"데이터 요청 실패: {e}")
#         return

#     # XML 데이터 파싱
#     decoded_content = response.content.decode('utf-8', errors='ignore')
#     cleaned_content = decoded_content.strip()

#     # lxml 파서로 재시도
#     parser = etree.XMLParser(recover=True)
#     root = etree.fromstring(cleaned_content.encode('utf-8'), parser=parser)

#     # 데이터 처리 및 출력
#     process_data(root)

# def process_data(root):
#     for item in root.findall('.//list'):
#         place_code = item.find('PlaceCode').text if item.find('PlaceCode') is not None else "N/A"
#         measure_time = item.find('MeasureTime').text if item.find('MeasureTime') is not None else "N/A"
#         organic = item.find('Organic').text if item.find('Organic') is not None else "N/A"
#         suspended = item.find('Suspended').text if item.find('Suspended') is not None else "N/A"
#         total_p = item.find('TotalP').text if item.find('TotalP') is not None else "N/A"
#         total_n = item.find('TotalN').text if item.find('TotalN') is not None else "N/A"
#         comm_disorder = item.find('CommDisorder').text if item.find('CommDisorder') is not None else "N/A"

#         print(f"Place: {place_code}, Time: {measure_time}, Organic: {organic}, "
#               f"Suspended: {suspended}, TotalP: {total_p}, TotalN: {total_n}, "
#               f"CommDisorder: {comm_disorder}")

# if __name__ == "__main__":
#     fetch_data()
