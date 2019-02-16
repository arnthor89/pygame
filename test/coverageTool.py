import unittest
import cursors_test
import draw_test

# Coverage tool for measuring how much of a function is covered by tests
# Note: Is currently only supported by pytohn 3.x not python 2.x
class coverageTool():
    def __init__(self):
        self.load_xbm = [False] * 28
        self.compile = [False] * 10
        self._draw_line = [False] * 18

    def run(self):
        # Test for load_xbm
        ct = cursors_test.CursorsModuleTest()
        ct.test_load_xbm(self.load_xbm)
        # Test for compile
        ct = cursors_test.CursorsModuleTest()
        ct.test_compile(self.compile)

        # Test for _draw_line funtion
        ct = draw_test.PythonDrawLineTest()
        ct.test_line_color(self._draw_line)
        ct.test_line_gaps(self._draw_line)
        ct.test_lines_color(self._draw_line)
        ct.test_lines_gaps(self._draw_line)

    def report(self):
        self.present("pygame.cursors.load_xbm", self.load_xbm)
        self.present("pygame.cursors.compile", self.compile)
        self.present("pygame.draw_py._draw_line", self._draw_line)

    def present(self, name ,result):
        print("-"*10 + name + "-"*10)
        for i in range(0,len(result)):
            print(str(i) + ": " + str(result[i]))
        print("Coverage = " + str(100*float(sum(result))/len(result))+ "%")
        print("-"*(20+len(name))+"\n")


if __name__=="__main__":
    ct = coverageTool()
    ct.run()
    ct.report()
