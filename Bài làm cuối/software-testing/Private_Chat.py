import unittest
import time
import csv
from parameterized import parameterized
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.web_driver import getDriverInit


def getTestcase():
    with open('./testcases/dataPrivateChat.csv', 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[1:]

class TestData:
    username = "student"
    password = "sandbox"
    url = "https://sandbox.moodledemo.net"
    
    testcase = getTestcase()
    

class TestPrivateChat(unittest.TestCase):    
    driver = None
    
    @classmethod
    def setUpClass(self):
        driver = self.driver
        driver.get(TestData.url)
        loginBtn = driver.find_element(By.XPATH, "//a[contains(@href, 'login')]")
        loginBtn.click()
        usernameTextbox = driver.find_element(By.NAME, "username")
        passwordTextBox = driver.find_element(By.NAME, "password")
        usernameTextbox.send_keys(TestData.username)
        passwordTextBox.send_keys(TestData.password)
        # loginBtn = driver.find_element(By.XPATH, "//button[contains(@id, 'login')]")
        # loginBtn.click()
        passwordTextBox.send_keys(Keys.ENTER)
        menuChat = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@id, 'message')]")))
        menuChat.click()
        starredChat = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@aria-controls, 'favourites')]")))
        if (starredChat.get_attribute("aria-expanded") == "false"):
            starredChat.click()
        contact = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='list-group']/a[contains(@href, '#')]")))
        contact.click()
        
        
        super().setUpClass()

    @classmethod
    def tearDownClass(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
    
    @parameterized.expand(TestData.testcase[:5])
    def testNormalTrimmedMessage(self, name, desc, message):
        driver = self.driver
        messageBox = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@data-region, 'send-message')]")))
        messageBox.click()
        messageBox.clear()
        messageBox.send_keys(message)
        # Prevent overflooding
        time.sleep(1)
        textLengthCap = len(message)
        textLengthCap = textLengthCap if textLengthCap < 4096 else 4096
        visibleMessage = message[0:textLengthCap]
        self.assertEqual(messageBox.get_attribute("value"), visibleMessage)
        sendBtn = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@data-action, 'send-message')]")))
        sendBtn.click()
        # Prevent overflooding
        time.sleep(1)
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//p[contains(text(),'{visibleMessage}')]")))
        except:
            self.assertTrue(False, "Message sent did not matched or correctly trimmed")
        # Prevent overflooding
        time.sleep(2)
            
    
    @parameterized.expand(TestData.testcase[6:])
    def testNotSentMessage(self, name, desc, message):
        driver = self.driver
        if message is not None:
            messageBox = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@data-region, 'send-message')]")))
            messageBox.click()
            messageBox.clear()
            messageBox.send_keys(message)
            self.assertEqual(messageBox.get_attribute("value"), message)
            # Prevent overflooding
            time.sleep(1)
        sendBtn = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@data-action, 'send-message')]")))
        sendBtn.click()
        sentMessages = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'message') and @tabindex='0']/div/p")))
        if sentMessages[-1].text == message:
            self.assertTrue(False, "Message is sent")
        # Prevent overflooding
        time.sleep(2)
            
            
class TestPrivateChatChrome(TestPrivateChat):
    @classmethod
    def setUpClass(self):
        print("\nTest in Chrome")
        self.driver = getDriverInit("Chrome")()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(self):
        return super().tearDownClass()

class TestPrivateChatFirefox(TestPrivateChat):
    @classmethod
    def setUpClass(self):
        print("\nTest in Firefox")
        self.driver = getDriverInit("Firefox")()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(self):
        return super().tearDownClass()
     

class TestPrivateChatMSEdge(TestPrivateChat):
    @classmethod
    def setUpClass(self):
        print("\nTest in MS Edge")
        self.driver = getDriverInit("Edge")()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(self):
        return super().tearDownClass()
    
    
def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTests([
        unittest.makeSuite(TestPrivateChatChrome),
        unittest.makeSuite(TestPrivateChatFirefox),
        unittest.makeSuite(TestPrivateChatMSEdge),
    ])
    return testSuite

unittest.TextTestRunner().run(suite())