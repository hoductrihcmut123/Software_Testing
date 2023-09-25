from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from utils.test_feature import TestFeature
from utils.io_testcase import Testcase

homeUrl="https://e-learning.hcmut.edu.vn/"
delay = 10
driver = None

## util ##
def waitGetEle(driver,locator):
    return WebDriverWait(driver, delay).until(EC.visibility_of_element_located(locator))
def shutdownDriver():
    global driver
    if driver:
        driver.quit()
        driver=None

## test function
def test_change_language(driverInit,testcase:Testcase):
    global driver
    shutdownDriver()
    driver=driverInit()
    driver.maximize_window()
    driver.get(homeUrl)

    # click button and return page loading check
    def select(lang):
        while True:
            elem = driver.find_element(*testcase.elems['langbutton'])
            elem.click()
            waitGetEle(driver,testcase.elems['schoolimage'])
            buttons = driver.find_elements(*testcase.elems['dropdownbutton'])
            for button in buttons:
                if lang in button.text:
                    button.click()
                    # Check load page or not by waiting image to disappear
                    try:
                        WebDriverWait(driver,1,0.01,()).until_not(EC.visibility_of_element_located(testcase.elems['schoolimage']))
                    except Exception as e:
                        if  isinstance(e,TimeoutException): return False
                    #Wait load 
                    waitGetEle(driver,testcase.elems['schoolimage'])
                    return True
    
    select(testcase.input['langfrom'])
    loadpage = select(testcase.input['langto'])
    loginbutton_text = waitGetEle(driver,testcase.elems['loginbutton']).text.strip()


    #Checking
    #Check not loadpage
    if not testcase.expected_output['needloadpage']:
        assert(loadpage==testcase.expected_output['needloadpage'])
    #Check text of language
    assert(loginbutton_text==testcase.expected_output['loginbutton_text'])


feature= {
    'name': 'Change_Language',
    'test_function': test_change_language,
    'testcase_path': './testcases/testcase.xlsx',
}
if __name__=='__main__':
    TestFeature(feature['name'],feature['test_function'],feature['testcase_path'])
    shutdownDriver()