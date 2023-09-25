import time
import XLUtils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def test1(input):
    
    testFile = input[0]
    defaultSheet = input[1]
    webAddress = input[2]
    delayTime = input[3]
    Env = input[4]
    Account = input[5]
    gotCol = 0
    resultCol = 0
    
    for env in range(len(Env)):     
        rows = XLUtils.getRowCount(testFile, defaultSheet)
        for row in range(2, rows + 1):
            value = XLUtils.readData(testFile, defaultSheet, row, 2)
            expect = XLUtils.readData(testFile, defaultSheet, row, 3)
            if value == None:
                value = ""
            testcaseNo = XLUtils.readData(testFile, defaultSheet, row, 1)
        
            if Env[env] == "Chrome":
                driver = webdriver.Chrome()
                gotCol = 4
                resultCol = 6
            if Env[env] == "Firefox":
                driver = webdriver.Firefox()
                gotCol = 5
                resultCol = 7
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
        
            #Access profile
            driver.find_element(By.ID, "user-menu-toggle").click()
            driver.find_element(By.XPATH, "//a[@class='dropdown-item'][1]").click()
            driver.find_element(By.XPATH, "//li[@class='editprofile']/span/a").click()
        
            time.sleep(delayTime)
        
            #Edit email
            try:
                EmailForm = driver.find_element(By.ID, "id_email")
            except NoSuchElementException:
                driver.find_element(By.XPATH, "//div[@class='form-control-static']/a").click()
                time.sleep(delayTime)
                EmailForm = driver.find_element(By.ID, "id_email")
            EmailForm.clear()
            EmailForm.send_keys(value)
            driver.find_element(By.ID, "id_submitbutton").click()
        
            time.sleep(delayTime)
        
            try:
                output = driver.find_element(By.ID, "id_error_email").get_attribute("innerHTML")
            except NoSuchElementException:
                output = ""
        
            if output.__contains__("Bắt buộc") or output.__contains__("Required"):
                print("Test " + str(testcaseNo))
                XLUtils.writeData(testFile, defaultSheet, row, gotCol, "Bắt buộc")
                if expect == "Bắt buộc":
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Passed")
                else:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Failed")
            elif output.__contains__("Địa chỉ thư điện tử không hợp lệ") or output.__contains__("Invalid email address"):
                print("Test " + str(testcaseNo))
                XLUtils.writeData(testFile, defaultSheet, row, gotCol, "Địa chỉ thư điện tử không hợp lệ")
                if expect == "Địa chỉ thư điện tử không hợp lệ":
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Passed")
                else:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Failed")
            else:
                print("Test " + str(testcaseNo))
                XLUtils.writeData(testFile, defaultSheet, row, gotCol, "")
                if expect == None:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Passed")
                else:
                    XLUtils.writeData(testFile, defaultSheet, row, resultCol, "Failed")    
                     
            driver.close()
        
        
             
input = [
        "Testcase_Tri.xlsx",
        "Edit_Email",
        "https://sandbox.moodledemo.net/login/index.php",
        0.5,
        ["Chrome", "Firefox"],
        ["student", "sandbox"]
        ]   
     
     
test1(input)