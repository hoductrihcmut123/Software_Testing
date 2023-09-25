import XLUtils
from selenium import webdriver
import time

testFile = "testcase.xlsx"
defaultSheet = "Sheet1"
linkWeb = "https://visualgo.net/en/hashtable"

# delay time between step
delay_time = 0


class By(object):
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


rows = XLUtils.getRowCount(testFile, defaultSheet)

for row in range(2, rows + 1):
    value = XLUtils.readData(testFile, defaultSheet, row, 2)
    testcaseNo = XLUtils.readData(testFile, defaultSheet, row, 1)
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(linkWeb)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(delay_time)
    driver.find_element(
        By.CSS_SELECTOR, "#electure-1 > .electure-end > u").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "create").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "v-create").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "v-create").clear()
    time.sleep(delay_time)
    driver.find_element(By.ID, "v-create").send_keys("5")
    time.sleep(delay_time)
    driver.find_element(By.CSS_SELECTOR, "#create-go > p").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "insert").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "v-insert").clear()
    time.sleep(delay_time)
    driver.find_element(By.ID, "v-insert").send_keys(value)
    time.sleep(delay_time)
    driver.find_element(By.CSS_SELECTOR, "#insert-go > p").click()
    # wait for the insertion finished
    time.sleep(10)
    # print the test result
    output = driver.find_element(
        By.CSS_SELECTOR, "#status > p").get_attribute("innerHTML")
    if output.__contains__("We append"):
        print("Test " + str(testcaseNo) + " passed")
        XLUtils.writeData(testFile, defaultSheet, row, 3, "test passed")
    else:
        print("Test " + str(testcaseNo) + " failed")
        XLUtils.writeData(testFile, defaultSheet, row, 3, "test failed")
    driver.close()
