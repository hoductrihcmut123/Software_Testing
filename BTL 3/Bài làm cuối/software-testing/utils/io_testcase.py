from utils.XLUtils import *
import pandas as pd

class Testcase:
    def __init__(self,input,expected_output,elems):
        self.input=input
        self.expected_output=expected_output
        self.elems=elems

def read_testcase(filename,sheetname):
    df = pd.read_excel(filename,sheet_name=sheetname)

    list_testcase=[]
    for i in range(df.shape[0]):
        row=df.iloc[i]
        inp,out,items={},{},{}

        for col in df.columns[1:]:
            typ,key=col.split(':')
            if typ=='in':
                inp[key]=row[col]
            elif typ=='out':
                out[key]=row[col]
            elif typ=='item':
                items[key]=row[col].split(',')
        list_testcase.append(Testcase(inp,out,items))
    return list_testcase

def write_res(filename,sheetname,res):
    max_col=getColumnCount(filename,sheetname)
    for r in range(len(res)):
        for envNo in range(3):
            writeData(filename,sheetname,r+2,max_col-2+envNo,res[r][envNo])