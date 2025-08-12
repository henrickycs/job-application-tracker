import os
import pandas as pd
from dotenv import load_dotenv

from linkedin_scraper import scrape_linkedin_jobs
from drive_uploader import upload_to_drive

load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

def main():
    print("Iniciando scraping do LinkedIn")
    data = scrape_linkedin_jobs(CHROMEDRIVER_PATH, EMAIL, PASSWORD)

    if not data:
        print("Nenhuma vaga encontrada")
        return
    
    csv_path = "vagas_aplicadas.csv"
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index = False, encoding="UTF-8")
    print(f"Dados salvos em {csv_path}")

    print("Enviando para o Google Drive")
    upload_to_drive(csv_path)
    print("Upload concluído")

if __name__ == "__main__":
    main()