from utils.io_testcase import read_testcase,write_res
from utils.web_driver import getDriverInit

def TestFeature(feature_name,feature_test_function,testcase_path):
    print("---------------------------------------")
    print("Testing for feature %s"%feature_name)
    passed,fail=0,0
    res=[]
    for testcase in read_testcase(testcase_path,feature_name):
        batch=[]
        for env in ['Chrome','Firefox','Edge']:
            print("Testing with input=%s, output=%s, env=%s"%(str(testcase.input),str(testcase.expected_output),env))
            try:
                feature_test_function(getDriverInit(env),testcase)
                print("-> Passed")
                passed+=1
                batch.append("Passed")
            except Exception as e:
                print("-> Failed, exception:",e)
                fail+=1
                batch.append("Failed")
        res.append(batch)
    print("Testing complete, %d/%d passed testcases"%(passed,passed+fail))
    print("---------------------------------------")
    
    write_res(testcase_path,feature_name,res)
