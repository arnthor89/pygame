import unittest
import cursors_test

class coverageTool():
    def __init__(self):
        self.load_xbm = [False] * 28

    def run(self):
        ct = cursors_test.CursorsModuleTest()
        ct.test_load_xbm(self.load_xbm)

    def report(self):
        self.present("load xbm",self.load_xbm)

    def present(self, name ,result):
        print("-"*10 + name + "-"*10)
        for i in range(0,len(result)):
            print(str(i) + ": " + str(result[i]))
        print("-"*(20+len(name))+"\n")

if __name__=="__main__":
    ct = coverageTool()
    ct.run()
    ct.report()
