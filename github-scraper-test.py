from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

#s = Service(ChromeDriverManager().install())

#new version of selenium
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)



#cdp = "chromedriver.exe"
#driver = webdriver.Chrome(executable_path=cdp)

driver.get("https://www.google.com")
driver.quit()

 