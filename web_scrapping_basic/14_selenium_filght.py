import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.maximize_window()  # 창 최대화

url = "https://flight.naver.com/"
browser.get(url)  # url로 이동

# 가는 날 선택 > click
browser.find_element_by_xpath("//*[@id='__next']/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]").click()
time.sleep(1)

# 이번 달 27일, 28일 선택
# browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[1]/button/b').click()  # 27일을 가진 값들 중, 첫번째 값 선택
# time.sleep(1)
# browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[5]/td[2]/button/b').click() 

# 3월 1일, 2일 선택. 나머지 일자는 스크롤을 내려야 돼서 안됨 ㅠ
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[3]/button/b').click()  # 27일을 가진 값들 중, 첫번째 값 선택
time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/div[1]/div[2]/div/div[3]/table/tbody/tr[1]/td[4]/button/b').click() 

# 제주도 고르기
time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/b').click()
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/section/button[1]').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[9]/div[2]/section/section/div/button[2]/i[1]').click()

# 항공권 검색
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/button/span').click()

# 몇 초를 기다려 주는 방식 > 로딩이 언제 끝나는지 모름..!
# 엘리먼트가 나올 때까지만 기다리라고 할 수 있음.
# WebDriverWait을 통해서, browser를 10초동안 기다려줌. > 10초가 넘으면 에러가 나고 끝남.
# 10초 내에 무엇을 진행하느냐, Expected_condition 에 대한 것을 기다림. 
# XPATH라는 조건으로, XPATH 값에 해당하는 엘리먼트가 "나올 때 까지" 기다림.
try:
    elem = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/div/div[2]/div[2]')))
    # 성공했을 때 동작 수행
    print(elem.text)  # 첫 번째 결과 출력
finally:
    time.sleep(2)
    browser.quit()


# 첫 번째 결과 출력
# elem = browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div[2]/div[2]/div/button')
# print(elem.text)