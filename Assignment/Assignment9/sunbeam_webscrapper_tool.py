from langchain.tools import tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@tool
def sunbeam_scrapper_tool():
    """
    Fetch internship batch details and available internship programs
    from Sunbeam website.

    Returns:
        dict: {
            "internship_batches": [...],
            "internship_programs": [...]
        }
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.sunbeaminfo.in/internship")
    driver.implicitly_wait(10)

    # ===================== Internship Batch Table =====================
    internships_batch = []

    try:
        table_container = driver.find_element(By.CLASS_NAME, "table-responsive")
        table = table_container.find_element(
            By.CSS_SELECTOR, "table.table-bordered.table-striped"
        )
        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 7:
                continue

            internships_batch.append({
                "Sr_No": cols[0].text.strip(),
                "Batch": cols[1].text.strip(),
                "Batch_Duration": cols[2].text.strip(),
                "Start_Date": cols[3].text.strip(),
                "End_Date": cols[4].text.strip(),
                "Time": cols[5].text.strip(),
                "Fees": cols[6].text.strip(),
            })
    except Exception as e:
        internships_batch.append({"error": str(e)})

    # ===================== Available Internship Programs =====================
    internships = []

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(driver, 10)

        plus_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
        plus_button.click()

        program_table = driver.find_element(By.ID, "collapseSix") \
                              .find_element(By.TAG_NAME, "table")

        rows = program_table.find_element(By.TAG_NAME, "tbody") \
                            .find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            internships.append({
                "Technology": cols[0].text.strip(),
                "Aim": cols[1].text.strip(),
                "Prerequisite": cols[2].text.strip(),
                "Learning": cols[3].text.strip(),
                "Location": cols[4].text.strip(),
            })
    except Exception as e:
        internships.append({"error": str(e)})

    driver.quit()

    return {
        "internship_batches": internships_batch,
        "internship_programs": internships
    }
