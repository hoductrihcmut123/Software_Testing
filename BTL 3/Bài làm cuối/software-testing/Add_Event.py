import time
# import XLUtils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from utils.web_driver import getDriverInit


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

        # Login
        driver.find_element(By.NAME, "username").send_keys(Account[0])
        driver.find_element(By.NAME, "password").send_keys(Account[1])
        driver.find_element(By.ID, "loginbtn").click()

        # Change language
        if Env[env] == "Chrome":               # Firefox has an HTML bug so it can't work here
            driver.find_element(By.ID, "user-menu-toggle").click()
            driver.find_element(
                By.XPATH, "//a[@class='carousel-navigation-link dropdown-item']").click()
            driver.find_element(
                By.XPATH, "//a[@class='dropdown-item pl-5'][103]").click()

        # Add new event
        nav_link = driver.find_elements(By.CLASS_NAME, 'nav-link')
        nav_link[1].click()
        time.sleep(3)
        for i in range(len(Events)):
            driver.find_element(
                By.XPATH, "//button[@class='btn btn-primary float-sm-right float-right']").click()
            time.sleep(3)
            driver.find_element(By.ID, "id_name").send_keys(Events[i])
            time.sleep(delayTime)

            if (i == 1):
                driver.find_element(By.CLASS_NAME, 'moreless-toggler').click()
                time.sleep(3)
                driver.find_element(By.ID, 'id_duration_1').click()
                time.sleep(3)
                driver.find_element(
                    By.ID, 'id_timedurationuntil_year').send_keys('2023')
            elif (i == 2):
                driver.find_element(By.CLASS_NAME, 'moreless-toggler').click()
                time.sleep(3)
                driver.find_element(By.ID, 'id_duration_1').click()
                time.sleep(3)
                driver.find_element(
                    By.ID, 'id_timedurationuntil_year').send_keys('2021')
                # save event
                elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(
                    By.XPATH, "//button[@data-action='save']").is_enabled())
                elem = driver.find_element(
                    By.XPATH, "//button[@data-action='save']")
                elem.click()

                time.sleep(15)

                # save event fail
                elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(
                    By.XPATH, "//button[@data-action='hide']").is_enabled())
                elem = driver.find_element(
                    By.XPATH, "//button[@data-action='hide']")
                elem.click()

                time.sleep(3)
                continue

            elif (i == 3):
                driver.find_element(By.CLASS_NAME, 'moreless-toggler').click()
                time.sleep(3)
                driver.find_element(By.ID, 'id_duration_2').click()
                time.sleep(3)
                driver.find_element(
                    By.ID, 'id_timedurationminutes').send_keys('0')

                # save event
                elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(
                    By.XPATH, "//button[@data-action='save']").is_enabled())
                elem = driver.find_element(
                    By.XPATH, "//button[@data-action='save']")
                elem.click()

                time.sleep(15)

                # save event fail
                elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(
                    By.XPATH, "//button[@data-action='hide']").is_enabled())
                elem = driver.find_element(
                    By.XPATH, "//button[@data-action='hide']")
                elem.click()

                time.sleep(3)
                continue
            elif (i == 4):
                driver.find_element(By.CLASS_NAME, 'moreless-toggler').click()
                time.sleep(3)
                driver.find_element(By.ID, 'id_duration_2').click()
                time.sleep(3)
                driver.find_element(
                    By.ID, 'id_timedurationminutes').send_keys('1')

            # save event
            elem = WebDriverWait(driver, 3).until(lambda x: x.find_element(
                By.XPATH, "//button[@data-action='save']").is_enabled())
            elem = driver.find_element(
                By.XPATH, "//button[@data-action='save']")
            elem.click()

            time.sleep(3)


input = [
    "",
    "",
    "https://sandbox.moodledemo.net/login/index.php",
    0.5,
        ["Chrome", "Firefox"],
        ["student", "sandbox"],
        ["TCB-AEC-001", "TCB-AEC-002", "TCB-AEC-003", "TCB-AEC-004", "TCB-AEC-005"]
]


test2(input)
