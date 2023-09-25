from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.io_testcase import Testcase
from utils.test_feature import TestFeature
from time import sleep

homeUrl="https://sandbox.moodledemo.net"
delay = 10
driver,driver2 = None,None
## util ##
def waitGetEle(driver,locator,delay=delay):
    return WebDriverWait(driver, delay).until(EC.visibility_of_element_located(locator))
def shutdownDriver():
    global driver
    if driver:
        driver.quit()
        driver=None
def shutdownDriver2():
    global driver2
    if driver2:
        driver2.quit()
        driver2=None

def login(driver,username,password):
    # load homepage
    driver.get(homeUrl)

    # go login
    while True:
        try:
            elem = driver.find_element(By.XPATH, "//div[@class='usermenu']")
            elem.click()
            sleep(1)
        except:break
        

    # fill in username and password
    usr = waitGetEle(driver,(By.XPATH, "//input[@id='username']"))
    pwd = waitGetEle(driver,(By.XPATH, "//input[@id='password']"))
    usr.clear()
    usr.send_keys(username)
    pwd.clear()
    pwd.send_keys(password)

    # Wait logged in
    while True:
        try:
            loginbtn = driver.find_element(By.ID, "loginbtn")
            loginbtn.click()
        except: break
    waitGetEle(driver,(By.ID, "user-menu-toggle"),5)

# send message when opened the content message container
def sendMessage(driver, message):
    # wait for seen all message
    waitGetEle(driver,(By.XPATH, "//div[contains(@data-region, 'content-message-container')]"))
  
    # messageBox
    messageBox = waitGetEle(driver,(By.XPATH, "//textarea[contains(@data-region, 'send-message')]"))
    messageBox.click()
    messageBox.clear()
    messageBox.send_keys(message)

    # click send to send message
    sendBtn = waitGetEle(driver,(By.XPATH, "//button[contains(@data-action, 'send-message')]"))
    sendBtn.click()

    # wait for message to be sent (by finding loading icon)
    WebDriverWait(driver, delay).until_not(EC.visibility_of_any_elements_located((By.XPATH, f"//div[@data-region='loading-icon-container']")))

# function to send message for user1
def user1SendMessage(driver,testcase):
    driver.get(testcase.input['user2profileurl'])
    # click and wait for the "Private Chat" button to show up
    while True:
        messBut=waitGetEle(driver,(By.XPATH,"//a[@id='message-user-button']"))
        messBut.click()
        try:waitGetEle(driver,(By.XPATH, "//textarea[contains(@data-region, 'send-message')]"),2)
        except: continue
        break
    
    for msg in testcase.input['msg'].split(','):
        sendMessage(driver,msg)

# function to count unread message of user2
def user2UnreadCount(driver):

    # click and wait for the "Private Chat" button to show up
    while True:
        # the message icon button on top right corner
        messageIconButton = waitGetEle(driver,(By.XPATH, "//div[@data-region='popover-region-messages']/a"))
        messageIconButton.click()
        try:waitGetEle(driver,(By.XPATH, "//div[@id='view-overview-messages-toggle']"),2)
        except: continue
        break
    
    # expand the private chat
    while True:
        privateChatDropdown = waitGetEle(driver,(By.XPATH, "//div[@id='view-overview-messages-toggle']/button"))
        if privateChatDropdown.get_attribute("aria-expanded")=='false':
            privateChatDropdown.click()
        else: break

    # waiting for all private chats to be loaded
    waitGetEle(driver,(By.XPATH, "//div[@aria-labelledby='view-overview-messages-toggle' and @data-loaded-all='true' and @data-loading='false']"))

    re = 0 # store for result of this function

    # click to the first unread chat
    try: 
        first_unread_chat = driver.find_element(By.XPATH, "//span[@data-region='unread-count']/span[1]")
        re = int(first_unread_chat.text.strip())
        first_unread_chat.click()
    
        # wait for seen all message
        waitGetEle(driver,(By.XPATH, "//div[contains(@data-region, 'content-message-container')]"))
        sleep(1)
    except: pass

    # close the message tab
    messageIconButton = waitGetEle(driver,(By.XPATH, "//div[@data-region='popover-region-messages']/a"))
    messageIconButton.click()
    return re
 
def test_new_message_noti(driverInit,testcase:Testcase):
    global driver,driver2
    shutdownDriver();shutdownDriver2()
    # read all unread message of user2
    driver2 = driverInit()
    driver2.maximize_window()
    login(driver2,testcase.input['username2'],testcase.input['password2'])
    user2UnreadCount(driver2)

    # send message from user1 to user2
    driver = driverInit()
    driver.maximize_window()
    login(driver,testcase.input['username1'],testcase.input['password1'])
    user1SendMessage(driver,testcase)
    shutdownDriver()

    # get the unread_count of user2
    driver2.get(homeUrl)
    unread_count=user2UnreadCount(driver2)
    shutdownDriver2()

    assert(unread_count==testcase.expected_output['unread_count'])


feature= {
    'name': 'New_Message_Noti',
    'test_function': test_new_message_noti,
    'testcase_path': './testcases/testcase.xlsx',
}
if __name__=='__main__':
    TestFeature(feature['name'],feature['test_function'],feature['testcase_path'])
    shutdownDriver()
    shutdownDriver2()