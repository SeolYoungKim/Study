# Selenium 은 Web driver 를 설치 해야 한다.
# 본인의 web 버전과 맞는 걸 설치 하자.
import time
from selenium import webdriver

# Chrome browser object 생성
browser = webdriver.Chrome(r"C:\Users\Home\Desktop\PythonWorkspace\chromedriver.exe")  # 완전히 같은 폴더 내에 있으면 작성 안해도 됨.

# 1. 네이버 url 로 이동
browser.get("http://naver.com")

# 2. login 버튼 클릭
elem = browser.find_element_by_class_name("link_login")
elem.click()

# 3. id, pw 입력
browser.find_element_by_id("id").send_keys("naver_id")
browser.find_element_by_id("pw").send_keys("password")

# 4. login 버튼 클릭
browser.find_element_by_id("log.login").click()

time.sleep(3)

# 5. id 를 새로 입력
browser.find_element_by_id("id").clear()
browser.find_element_by_id("id").send_keys("my_id")

# 6. html 정보 출력
print(browser.page_source)

# 7. browser 종료
# browser.close()  # 현재 탭만 종료
browser.quit()  # 전체 브라우저 종료
