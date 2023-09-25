import XLUtils
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

testFile = "testcase.xlsx"
defaultSheet = "Sheet1"
linkWeb = "https://visualgo.net/en/heap"

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
    expect = XLUtils.readData(testFile, defaultSheet, row, 4)
    if value == None:
        value = ""
    print(value)
    testcaseNo = XLUtils.readData(testFile, defaultSheet, row, 1)
    # driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=Service("chromedriver.exe"))
    driver.get(linkWeb)
    driver.maximize_window()
    driver.implicitly_wait(20)
    time.sleep(delay_time)
    # driver.find_element(
    #     By.CSS_SELECTOR, "#electure-1 > .electure-end > u").click()
    driver.find_element(By.ID, "gdpr-reject").click()
    time.sleep(delay_time)
    driver.find_element(By.CLASS_NAME, "electure-end").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "createN").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "arrv2").click()
    time.sleep(delay_time)
    driver.find_element(By.ID, "arrv2").clear()
    time.sleep(delay_time)
    driver.find_element(By.ID, "arrv2").send_keys(value)
    time.sleep(delay_time)
    driver.find_element(By.CSS_SELECTOR, "#createN-go > p").click()
    # time.sleep(delay_time)
    # driver.find_element(By.ID, "insert").click()
    # time.sleep(delay_time)
    # driver.find_element(By.ID, "v-insert").clear()
    # time.sleep(delay_time)
    # driver.find_element(By.ID, "v-insert").send_keys(value)
    # time.sleep(delay_time)
    # driver.find_element(By.CSS_SELECTOR, "#insert-go > p").click()
    # wait for the insertion finished
    time.sleep(10)
    # print the test result
    # output = driver.find_element(
    #     By.CSS_SELECTOR, "#status > p").get_attribute("innerHTML")
    output = driver.find_element(
        By.ID, "createN-err").get_attribute("innerHTML")
    if output.__contains__("Sorry, you cannot build a Binary Max Heap with more than 31 integers in this visualization."):
        print("Test " + str(testcaseNo) + " failed")
        XLUtils.writeData(testFile, defaultSheet, row, 3, "test failed")
        if expect == "test failed":
            XLUtils.writeData(testFile, defaultSheet, row, 5, "test passed")
        else:
            XLUtils.writeData(testFile, defaultSheet, row, 5, "test failed")
    else:
        print("Test " + str(testcaseNo) + " passed")
        XLUtils.writeData(testFile, defaultSheet, row, 3, "test passed")
        if expect == "test passed":
            XLUtils.writeData(testFile, defaultSheet, row, 5, "test passed")
        else:
            XLUtils.writeData(testFile, defaultSheet, row, 5, "test failed")
    driver.close()
