# import all neccessary libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def sunbeam_internship_scraping(url):
    # start the selenium browser session
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # load the desired page in the browser
    driver.get(url)
    # Scroll to the bottom (makes sure that dynamic contents load)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # define wait stratergy 
    wait =WebDriverWait(driver, 10)

    # wait for and click the "Available Internship Programs" toggle button
    plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
    plus_button.click()


    # interact the web controls
    t_div = driver.find_element(By.ID, "collapseSix")
    t_class = t_div.find_element(By.TAG_NAME, "table")
    t_body = t_class.find_element(By.TAG_NAME,"tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        # print(len(cols))
        if len(cols) < 5:
            continue

        internship = {
            "Technology":cols[0].text.strip(),
            "Aim":cols[1].text.strip(),
            "Prerequisite":cols[2].text.strip(),
            "Learning":cols[3].text.strip(),
            "Location":cols[4].text.strip()
        }
        internships.append(internship)

    # Stop the session
    driver.quit()
    return internships

if __name__ == "__main__":
    url = "https://www.sunbeaminfo.in/internship"
    internship = sunbeam_internship_scraping(url)
    for intern in internship:
        print(intern)

