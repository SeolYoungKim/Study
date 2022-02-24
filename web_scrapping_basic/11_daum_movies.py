import requests
from bs4 import BeautifulSoup
# import re

my_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}



for year in range(2015, 2022):
    url = "https://search.daum.net/search?w=tot&q={}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR".format(year)

    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    images = soup.find_all("img", attrs={"class":"thumb_img"})

    for idx, image in enumerate(images):
        image_url = image["src"]
        if image_url.startswith("//"):
            image_url = "https:" + image_url

        
        image_res = requests.get(image_url)
        image_res.raise_for_status()

            # page에 접속해서 페이지에 있는 정보를 파일로 저장할것임
        with open("movie_{}_{}.jpg".format(year, idx + 1), "ab") as f:
            f.write(image_res.content) 

        if idx >= 4:  # 상위 5개 이미지까지만 다운로드 
            break


        





