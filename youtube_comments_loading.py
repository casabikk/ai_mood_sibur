from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import yaml


with open('configuration/yaml.yml', 'r') as file:
    config = yaml.safe_load(file)


url = config['youtube_urls'][0]['url']



service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))


body = driver.find_element(By.TAG_NAME, 'body')
for i in range(20):  
    body.send_keys(Keys.PAGE_DOWN)
    sleep(2)  


comments = []
comment_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

for comment in comment_elements:
    comments.append(comment.text)


driver.quit()

for comment in comments:
    print(comment)