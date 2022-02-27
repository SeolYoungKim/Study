from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# 헤드리스 크롬 : 눈에 보이진 않지만 실행은 됨.
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")  # 해당 크기에 맞춰서 브라우저를 띄운 후 동작
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

s = Service(r"C:\Users\Home\Desktop\PythonWorkspace\chromedriver.exe")
browser = webdriver.Chrome(service=s, options=options)
browser.maximize_window()

url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent/'
browser.get(url)

detected_value = browser.find_element(by=By.ID, value="detected_value")

print(detected_value.text)  # User-agent 값이 HeadlessChrome으로 넘어가기 때문에 주의해야 함.

browser.quit()

