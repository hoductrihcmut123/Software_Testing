from selenium import webdriver
from webdriver_manager import chrome,firefox,microsoft
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

chromepath=chrome.ChromeDriverManager().install()
firefoxpath=firefox.GeckoDriverManager().install()
edgepath=microsoft.EdgeChromiumDriverManager().install()
def getDriverInit(name):
    if name == 'Chrome':
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return lambda: webdriver.Chrome(service=ChromeService(chromepath),options=options)
    elif name == 'Firefox':
        return lambda: webdriver.Firefox(service=FirefoxService(firefoxpath))
    elif name == 'Edge':
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return lambda: webdriver.Edge(service=EdgeService(edgepath),options=options)
