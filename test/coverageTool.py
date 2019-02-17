import unittest
import cursors_test
import draw_test

# Coverage tool for measuring how much of a function is covered by tests
# Note: Is currently only supported by pytohn 3.x not python 2.x
class coverageTool():
    def __init__(self):
        self.TrueCount = 0
        self.totCount = 0
        self.branchArray = {}
        self.branchArray['load_xbm'] = [False] * 28
        self.branchArray['compile'] = [False] * 10
        self.branchArray['_draw_line'] = [False] * 18
        self.branchArray['clip_line'] = [False] * 23

    def run(self):
        # Test for load_xbm
        ct = cursors_test.CursorsModuleTest()
        ct.test_load_xbm(self.branchArray['load_xbm'])

        # Test for compile
        ct = cursors_test.CursorsModuleTest()
        ct.test_compile(self.branchArray['compile'])

        # Test for _draw_line funtion
        ct = draw_test.PythonDrawLineTest()
        ct.test_line_color(self.branchArray['_draw_line'])
        ct.test_line_gaps(self.branchArray['_draw_line'])
        ct.test_lines_color(self.branchArray['_draw_line'])
        ct.test_lines_gaps(self.branchArray['_draw_line'])

        # Test for clip_line funtion
        ct = draw_test.PythonDrawLineTest()
        ct.test_line_color(self.branchArray['clip_line'])
        ct.test_line_gaps(self.branchArray['clip_line'])
        ct.test_lines_color(self.branchArray['clip_line'])
        ct.test_lines_gaps(self.branchArray['clip_line'])

        self.totCount = 0
        self.TrueCount = 0
        for key in self.branchArray:
            self.TrueCount += sum(self.branchArray[key])
            self.totCount += len(self.branchArray[key])


    def report(self):
        self.present("pygame.cursors.load_xbm", self.branchArray['load_xbm'])
        self.present("pygame.cursors.compile", self.branchArray['compile'])
        self.present("pygame.draw_py._draw_line", self.branchArray['_draw_line'])
        self.present("pygame.draw_py.clip_line", self.branchArray['clip_line'])

        if self.totCount != 0:
            print("Total coverage: " + str(100*self.TrueCount/self.totCount) + "%")

    def present(self, name ,result):
        print("-"*10 + name + "-"*10)
        for i in range(0,len(result)):
            print(str(i) + ": " + str(result[i]))
        print("Coverage = " + str(self.calculate_coverage(result))+ "%")
        print("-"*(20+len(name))+"\n")

    def calculate_coverage(self,result):
        return 100*float(sum(result))/len(result)


if __name__=="__main__":
    ct = coverageTool()
    ct.run()
    ct.report()
