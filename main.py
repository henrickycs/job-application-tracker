import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_to_drive(file_path, folder_id=None):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype='text/csv')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f'Arquivo enviado para o Drive. ID: {file.get("id")}')

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
time.sleep(20)  # esperar login concluir e/ou captcha

index = 0
data = []
while True:
    driver.get(f"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start={index}")
    try:
        time.sleep(5)

        ul = driver.find_element(By.CSS_SELECTOR, ".list-style-none")
        divs = ul.find_elements(By.CSS_SELECTOR, ".linked-area.flex-1.cursor-pointer")

        if not divs:
             print(f"Não encontrou vagas na página {index}, finalizando.")
             break

        for div in divs:
                line = div.text.strip().split("\n")
                title = line[0]
                business = div.find_element(By.CSS_SELECTOR, ".t-14.t-black.t-normal").text.strip()
                localization = div.find_element(By.CSS_SELECTOR, ".t-14.t-normal:not(.t-black)").text.strip()
                application_date = div.find_element(By.CSS_SELECTOR, ".workflow-posted-jobs__jobs-insight").text.strip()

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

csv_path = "vagas_aplicadas.csv"
df = pd.DataFrame(data)
df.to_csv(csv_path, index = False, encoding="UTF-8")

driver.quit()

upload_to_drive(csv_path)