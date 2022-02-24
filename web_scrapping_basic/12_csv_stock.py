import csv
import requests
from bs4 import BeautifulSoup

my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

file_name = "시가총액 1-200.csv"
f = open(file_name, "w", encoding="utf-8-sig", newline="")  # 자동 줄바꿈을 없애줌.
writer = csv.writer(f)  # 엑셀 파일에서 열 때 한글이 깨지면 utf-8-sig 이용

title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE	토론실".split("\t")
print(type(title))
writer.writerow(title)  # List 형태로 넘겨주어야 함.

for page_num in range(1, 6):
    print("{}페이지 입니다.".format(page_num))
    # 문자열은 문자열끼리 더해라~!
    res = requests.get(url + str(page_num))
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")

    for row in data_rows:
        columns = row.find_all("td")
        
        if len(columns) <= 1:  # 의미 없는 data는 skip
            continue
        
        # print(columns)
        # print("----------------------")

        data = [column.get_text().strip() for column in columns]
        # print(data)
        writer.writerow(data)  # 리스트 data를 넣어준다.
