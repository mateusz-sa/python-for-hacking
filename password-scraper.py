from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


repo = input(" repo you would like to target ")
repo1 = repo
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get(repo)
res = driver.find_elements(By.CLASS_NAME, "repo")
actual_txt_file = []

def going_for_raw(repo5):
    driver.get(repo5)
    # print("worked")
    raw = driver.find_element(By.CLASS_NAME, "js-permalink-replaceable-link")
    raw.click()
    html = driver.page_source
    html = f"{html}"
    # print(html)  
    if "pass" in html:
        print(f"\n pass found inside {repo5}")
        # this = re.findall(r"([^.]password[^.]*\.)",html)
        # print(this)

def loop(repo3):
    global a
    driver.get(repo3)
    ress = driver.find_elements(By.CLASS_NAME, "js-navigation-open")
    for a in ress:
        pass
        # print(a.text)
    if "py" in a.text:
        # print("py")
        repo5 = f"{repo3}/blob/main/{a.text}"
        going_for_raw(repo5)
    elif "js" in a.text:
        # print("py")
        repo5 = f"{repo3}/blob/main/{a.text}"
        going_for_raw(repo5)
    elif "xml" in a.text:
        # print("py")
        repo5 = f"{repo3}/blob/main/{a.text}"
        going_for_raw(repo5)
    elif "txt" in a.text:
        print("txt")
        repo5 = f"{repo3}/blob/main/{a.text}"
        going_for_raw(repo5)


links = []
flinks = []

for e in res:
    links.append(e.text)


for l in links:
    repo3 = f"{repo}/{l}"
    flinks.append(repo3)
    loop(repo3)
    repo = f"{repo1}"

driver.close()
driver.quit()

