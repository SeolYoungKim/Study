import requests
from bs4 import BeautifulSoup
import re

my_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

for i in range(1, 6):
    print(" 현재 페이지는 {} 입니다. ".format(i))
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=1=5&backgroundColor=".format(i)

    res = requests.get(url, headers=my_headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items = soup.find_all("li", attrs={"class":re.compile("^search-product")})
    # print(items[0].find("div", attrs={"class":"name"}).get_text())

    for item in items:

        # 광고 제품 제외
        ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
        if ad_badge:
            # print(" [광고 상품은 제외합니다.] ")
            continue  # 광고 상품이라면, continue 를 통해서 아래 구문은 실행하지 않고, 바로 for문으로 넘어감.

        name = item.find("div", attrs={"class":"name"}).get_text()

        # 애플 제품 제외
        if "Apple" in name:
            # print(" [Apple 제품은 제외합니다.] ")
            continue

        price = item.find("strong", attrs={"class":"price-value"})
        
        if price:  # 가격이 없는 제품은 text를 가져오지 않고, 
            price = price.get_text()

        else:
            price = "가격 정보 없음"
            # print(" [가격 정보가 없는 상품은 제외합니다.] ")
            continue

        rate = item.find("em", attrs={"class":"rating"})
        rating_total_count = item.find("span", attrs={"class":"rating-total-count"})

        if rate or rating_total_count:  # 값이 있다면
            rate = rate.get_text()
            rating_total_count = rating_total_count.get_text()[1:-1]
            # 평점 수 : (25)로 출력. 1번 index부터 -1번 전까지 슬라이싱.
        else:
            rate = "평점 없음"
            rating_total_count = "평점 수 없음"
            # print(" [평점이 없는 상품은 제외합니다.] ")
            continue
        
        link = "https://www.coupang.com" + item.a["href"]

        # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회
        if float(rate) >= 4.5 and int(rating_total_count) >= 100:
            # print(name, price, rate, rating_total_count)
            with open("notebook.txt", "a", encoding="utf8") as f:
                f.write(f"제품명 : {name} \n노트북 가격 : {price} \n평점: {rate} \n평점 수 : {rating_total_count} \n구매링크 : {link}\n--------------------\n")

        # if rating_total_count:  # 값이 있다면
        #     rate = rate.get_text()
        # else:
        #     rate = "평점 없음"
        
        
