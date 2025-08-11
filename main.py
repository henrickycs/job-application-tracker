import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

options = Options()
options.add_argument("--start-maximized")

service = Service(r"F:/chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/login")
time.sleep(2)

email_input = driver.find_element(By.ID, "username")
email_input.send_keys(EMAIL)

senha_input = driver.find_element(By.ID, "password")
senha_input.send_keys(PASSWORD)

senha_input.send_keys(Keys.RETURN)
time.sleep(5)  # esperar login concluir

index = 0
data = []
while True:
    driver.get(f"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start={index}")
    try:
        time.sleep(5)

        ul = driver.find_element(By.CSS_SELECTOR, ".hZRqGQjZkeoyTtaUlHFlUDfmbvQbtmbCgyo.list-style-none")
        lis = ul.find_elements(By.CLASS_NAME, "yEVDvREvYAajFiBIIVhkzjsMXySLhBCUA ")

        for li in lis:
                line = li.text.strip().split("\n")
                title = line[0]
                business = li.find_element(By.CSS_SELECTOR, ".xbQbBliPjkmWUSjRqkTSFsPJqspuFTLRySodk.t-14.t-black.t-normal").text.strip()
                localization = li.find_element(By.CSS_SELECTOR, ".FMtHznKrVeoQCZyiyseTglmsAmMqGROzOlZdY.t-14.t-normal").text.strip()
                application_date = li.find_element(By.CSS_SELECTOR, ".gyOdlZQjtxbuVjKvZqzHCMJYwnbHIJVhcumU.reusable-search-simple-insight__text--small").text.strip()

                data.append({
                        "Título": title,
                        "Empresa": business,
                        "Localização": localization,
                        "Tempo Candidatura": application_date,
                        "Site": "LinkedIn"
                })
        print(data)
        index +=10

    except:
        print(f"Não encontrou vagas na página {index}, finalizando.")
        break
         

print(data)
df = pd.DataFrame(data)
df.to_csv("vagas_aplicadas.csv", index = False, encoding="UTF-8")

driver.quit()