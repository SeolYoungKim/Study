import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

s = Service(r"C:\Users\Home\Desktop\PythonWorkspace\chromedriver.exe")
browser = webdriver.Chrome(service=s)
browser.maximize_window()

# 페이지 이동
url = "https://www.daum.net/"

browser.get(url)

browser.find_element(by=By.CLASS_NAME, value="inner_search").click()
browser.find_element(by=By.CLASS_NAME, value="tf_keyword").send_keys("광교 더샵 레이크 시티")
time.sleep(1)
browser.find_element(by=By.XPATH, value='//*[@id="daumSearch"]/fieldset/div/div/button[2]').click()

soup = BeautifulSoup(browser.page_source, "lxml")

estates = soup.find("tbody").find_all("tr")

for idx, estate in enumerate(estates):
    estate_info = estate.find_all("td")
    print(f"=========== 매물 {idx + 1} ===========")

    info = [info.get_text().strip() for info in estate_info]
    info_left = ["거래 :", "면적 :", "가격 :", "동 :", "층 :"]
    info_right = ["", "(공급/전용)", "(만원)", "", ""]

    for left, information, right in zip(info_left, info, info_right):
        print(left, information, right)

    # for info in estate_info:
    #     print(info.get_text())

    # print(f"거래 :{info[0]}\n면적 :{info[1]} (공급/전용)\n가격 :{info[2]} (만원)\n동 :{info[3]}\n층 :{info[4]}")

time.sleep(2)
