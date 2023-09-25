from selenium import webdriver
import time
import pandas as pd

filename = './TestCase.xlsx'


def test(webAddress, item, target, sheet_name):
    input = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
    for inp in range(len(input)):
        data = str(input["Input"][inp]).split("#")

        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get(webAddress)
        driver.maximize_window()
        time.sleep(delay_time)

        for i in item:
            if i[0] == 'sleep':
                time.sleep(i[1])
                continue

            index = i[1].find('=')
            type = i[1][:index]
            adr = i[1][index + 1:]

            if i[0] == 'click':
                driver.find_element(type, adr).click()
            elif i[0] == 'type':
                input_field = driver.find_element(type, adr)
                driver.execute_script("arguments[0].value = ''", input_field)
                input_field.send_keys(data[0])
                data = data[1:]

            time.sleep(delay_time)

        index = target[1].find('=')
        type = target[1][:index]
        adr = target[1][index + 1:]
        result = driver.find_element(type, adr).text
        print("???", result)
        input["Got"][inp] = str(result)
        if(input['Got'][inp] == input['Expect'][inp] or result == "" and input['Expect'][inp] =="Test Passed"):
            input['Result'][inp] = "Passed"
        else:
            input['Result'][inp] = "Failed"
        # time.sleep(5)
        driver.quit()

    input.to_excel('./TestCase'+sheet_name+".xlsx", sheet_name, index=False)


# create
webAddress = 'https://visualgo.net/en/heap'

item = [
    ['click', "id=gdpr-accept"],
    ['click', "xpath=//div[@id='overlay']/div[2]"],
    ['click', "id=createN"],
    ['click', "id=arrv2"],
    ['type', "id=arrv2"],
    ['click', "xpath=//div[@id='createN-go']/p"],
]
target = ['get', "id=createN-err"]
sheet_name = 'BinaryHeap'
delay_time = 0

test(webAddress, item, target, sheet_name)
