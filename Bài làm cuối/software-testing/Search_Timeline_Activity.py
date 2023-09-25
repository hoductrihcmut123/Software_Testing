import time
import utils.XLUtils as XLUtils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.web_driver import getDriverInit

def waitGetEle(driver,locator,delay=10):
    return WebDriverWait(driver, delay).until(EC.visibility_of_element_located(locator))

def test2(input):
    
    testFile = input[0]
    defaultSheet = input[1]
    webAddress = input[2]
    delayTime = input[3]
    Env = input[4]
    Account = input[5]
    Events = input[6]
    gotCol = 0
    resultCol = 0
    
    for env in range(len(Env)):     
        if Env[env] == "Chrome":
            gotCol = 4
            resultCol = 6
        if Env[env] == "Firefox":
            gotCol = 5
            resultCol = 7
        driver = getDriverInit(Env[env])()
        driver.get(webAddress)
        driver.maximize_window()
        
        #Login
        driver.find_element(By.NAME, "username").send_keys(Account[0])
        driver.find_element(By.NAME, "password").send_keys(Account[1])
        driver.find_element(By.ID, "loginbtn").click()
        
        #Change language
        if Env[env] == "Chrome":               # Firefox has an HTML bug so it can't work here 
            driver.find_element(By.ID, "user-menu-toggle").click()
            driver.find_element(By.XPATH, "//a[@class='carousel-navigation-link dropdown-item']").click()
            driver.find_element(By.XPATH, "//a[@class='dropdown-item pl-5'][103]").click()
        
        #Add new event
        nav_link = driver.find_elements(By.CLASS_NAME, 'nav-link')
        nav_link[1].click()
        time.sleep(3)
        for i in range(len(Events)):
            driver.find_element(By.XPATH, "//button[@class='btn btn-primary float-sm-right float-right']").click()
            waitGetEle(driver,(By.ID, "id_name")).send_keys(Events[i])
            time.sleep(delayTime)
                 
            # save event
            elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(By.XPATH, "//button[@data-action='save']").is_enabled())
            elem = driver.find_element(By.XPATH, "//button[@data-action='save']")
            elem.click()

            time.sleep(3)
        
        #Search timeline activity
        rows = XLUtils.getRowCount(testFile, defaultSheet)
        for row in range(2, rows + 1):
            value = XLUtils.readData(testFile, defaultSheet, row, 2)
            expect = XLUtils.readData(testFile, defaultSheet, row, 3)
            if value == None:
                value = " "
            testcaseNo = XLUtils.readData(testFile, defaultSheet, row, 1)
            
            searchForm = driver.find_element(By.ID, "searchinput")
            searchForm.clear()
            searchForm.send_keys(value)
            searchForm.send_keys(Keys.RETURN)
        
            time.sleep(5)
        
            try:
                output = driver.find_element(By.XPATH, "//p[@class='text-muted mt-1 xh-highlight']").get_attribute("innerHTML")
            except NoSuchElementException:
                output = ""
        
            if output.__contains__("No activities require action"):
                print("Test " + str(testcaseNo))
                XLUtils.writeData(testFile, defaultSheet, row, gotCol, "No activities require action")
                if expect == "No activities require action":
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Passed")
                else:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Failed")
            else:
                print("Test " + str(testcaseNo))
                XLUtils.writeData(testFile, defaultSheet, row, gotCol, "Kết quả tìm kiếm ra các Event")
                if expect != "No activities require action":
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Passed")
                else:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Failed")    
                     
        driver.close()
        
        
             
input = [
        "./testcases/testcase.xlsx",
        "Search_Timeline_Activity",
        "https://sandbox.moodledemo.net/login/index.php",
        0.5,
        ["Chrome", "Firefox"],
        ["student", "sandbox"],
        ["#Software testing UNIT 18", "Quiz 18", "Assignment 2 software testing"]
        ]   
     
     
test2(input)