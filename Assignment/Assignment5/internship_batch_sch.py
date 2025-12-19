# import all neccessary libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def sunbeam_internship_schedule_scraping(url):
    # start the selenium browser session
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # load the desired page in the browser
    driver.get(url)
    
    # define wait stratergy 
    driver.implicitly_wait(10)

    # interact the web controls
    t_base_class = driver.find_element(By.CLASS_NAME, "table-responsive")
    t_css = t_base_class.find_element(By.CSS_SELECTOR, "table.table-bordered.table-striped")
    t_body = t_css.find_element(By.TAG_NAME,"tbody")
    t_row = t_body.find_elements(By.TAG_NAME, "tr")

    internships = []

    for row in t_row:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 5:
            continue

        internship = {
            "Sr. No.":cols[0].text.strip(),
            "Batch":cols[1].text.strip(),
            "Batch Duration":cols[2].text.strip(),
            "Start Date":cols[3].text.strip(),
            "End Date":cols[4].text.strip(),
            "Time":cols[5].text.strip(),
            "Fees":cols[6].text.strip(),
            # "Download":cols[7].text.strip()
        }
        internships.append(internship)

    # Stop the session
    driver.quit()
    return internships

if __name__ == "__main__":
    url = "https://www.sunbeaminfo.in/internship"
    internship = sunbeam_internship_schedule_scraping(url)
    for intern in internship:
        print(intern)

