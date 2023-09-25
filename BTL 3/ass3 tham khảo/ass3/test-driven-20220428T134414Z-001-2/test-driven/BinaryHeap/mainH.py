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
            adr = i[1][index + 1 :]

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
        adr = target[1][index + 1 :]
        result = driver.find_element(type, adr).text
        print("???",result)
        input["Got"][inp] = str(result)
        if(input['Got'][inp]==input['Expect'][inp] or result ==""): input['Result'][inp]="Passed"
        else: input['Result'][inp]="Failed"
        # time.sleep(5)
        driver.quit()
    

    input.to_excel('./TestCase'+sheet_name+".xlsx", sheet_name, index=False)


# create 
webAddress = 'https://visualgo.net/en/list'

item = [
    ['click', "id=gdpr-accept"],
    ['click', "xpath=//div[14]/div[2]"],
    ['click', "id=insert"],
    ['click', "xpath=//div[@id='insert-head']/p"],
    ['click', "id=inserthead-input"],
    ['type', "id=v-insert-head-value"],
    ['click', "xpath=//div[@id='inserthead-go']/p"],
]
target = ['get', "id=insert-err"]
sheet_name = 'List_Insert'
delay_time = 0

test(webAddress, item, target, sheet_name)



itemCreate = [
    ['click', "id=gdpr-accept"],
    ['click', "xpath=//div[14]/div[2]"],
    ['click', "id=create"],
    ['click', "xpath=//div[5]/p"],
    ['click', "id=v-create-arr"],
    ['type', "id=v-create-arr"],
    ['click', "xpath=//div[5]/div/div[2]/p"],
]
targetCreate = ['get', "id=create-err"]
sheet_nameCreate = 'List_Create'
delay_time = 1
test(webAddress, itemCreate, targetCreate, sheet_nameCreate)
