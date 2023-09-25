from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from utils.web_driver import getDriverInit

driver = getDriverInit("Chrome")()
driver.get("https://sandbox.moodledemo.net/login/index.php")
user= driver.find_element(By.ID, "username")
user.send_keys("student")

pa = driver.find_element(By.ID,"password")
pa.send_keys("sandbox")

btn = driver.find_element(By.ID,"loginbtn")
btn.click()

driver.find_element(By.LINK_TEXT, "My courses").click()

search= driver.find_element(By.ID,"searchinput")
search.clear()
search.send_keys("my first")
search.send_keys(Keys.RETURN)
time.sleep(5)

search= driver.find_element(By.ID,"searchinput")
search.clear()
search.send_keys("MY FIRST")
search.send_keys(Keys.RETURN)
time.sleep(5)

search= driver.find_element(By.ID,"searchinput")
search.clear()
search.send_keys("20")
search.send_keys(Keys.RETURN)
time.sleep(5)

search= driver.find_element(By.ID,"searchinput")
search.clear()
search.send_keys("!@")
search.send_keys(Keys.RETURN)




time.sleep(5)



driver.quit()