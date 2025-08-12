import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_linkedin_jobs(chromedriver_path, email, password):
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    data = []
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(email)

        senha_input = driver.find_element(By.ID, "password")
        senha_input.send_keys(password)

        senha_input.send_keys(Keys.RETURN)
        time.sleep(20)  # esperar login concluir e/ou captcha

        index = 0
        while True:
            driver.get(f"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start={index}")
            try:
                ul = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, ".list-style-none")
                        )
                    )
                divs = ul.find_elements(By.CSS_SELECTOR, ".linked-area.flex-1.cursor-pointer")

            except:
                print(f"Não encontrou vagas na página {index}, finalizando.")
                break

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
            index +=10

    finally:
        driver.quit()

    return data