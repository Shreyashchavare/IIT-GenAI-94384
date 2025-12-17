#import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# start the selenium browser session
# time.sleep(5)

driver = webdriver.Chrome()

driver.implicitly_wait(5)
# load desired page in ther browser
driver.get("http://duckduckgo.com")
print("Initial Page Title:", driver.title)

#access control on the page 
search_box = driver.find_element(By.NAME, "q")

# interact with the control
for ch in "dkte college ichalkaranji":
    search_box.send_keys(ch)
    time.sleep(0.2)
search_box.send_keys("dkte college Ichalkaranji")
search_box.send_keys(Keys.RETURN)


# wait for the result
print("Later Page Title: ", driver.title)

#stop session
time.sleep(10)
driver.quit()