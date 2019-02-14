import unittest
import platform
import pygame.sysfont

class SysfontModuleTest(unittest.TestCase):
    def todo_test_create_aliases(self):
        self.fail()

    def todo_test_initsysfonts(self):
        self.fail()

    @unittest.skipIf('Darwin' not in platform.platform(), 'Not mac we skip.')
    def test_initsysfonts_darwin(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 10)

    def test_sysfont_good(self):
        import pygame.font
        pygame.font.init()
        arial = pygame.font.SysFont('Arial', 40, 1, 0)
        self.assertTrue(arial.get_bold())
        self.assertFalse(arial.get_italic())

    @unittest.skipIf('Linux' not in platform.platform(), 'Not linux we skip.')
    def test_initsysfonts_unix(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 1)

    def test_sysfont_notRecognized(self):
        arial = pygame.sysfont.SysFont('1234567890', 40, 1, 1)
        self.assertTrue(arial.get_bold())
        self.assertTrue(arial.get_italic())

    def test_sysfont_setFontName(self):
        fontname, bold, italic = pygame.sysfont.set_font_name('Arial', 0, 0)  
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setFontNameWithStyles(self):
        fontname, bold, italic = pygame.sysfont.set_font_name('Arial', 1, 1)  
        self.assertTrue(fontname)
        self.assertTrue(bold)
        self.assertTrue(italic)

    def test_sysfont_setFontNameNoName(self):
        fontname = pygame.sysfont.set_font_name(None, 0, 0)  
        self.assertIsNone(fontname)

    def test_sysfont_setStyles(self):
        fontname, bold, italic = pygame.sysfont.set_styles('sans', 1, 1)
        self.assertTrue(fontname)
        self.assertTrue(bold)
        self.assertTrue(italic)

    def test_sysfont_setNoStyles(self):
        fontname, bold, italic = pygame.sysfont.set_styles('sans', 0, 0)  
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setStylesNoName(self):
        fontname, bold, italic = pygame.sysfont.set_styles(None, 0, 0)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setInvalidFont(self):
        fontname, bold, italic = pygame.sysfont.set_styles('1234567890', 0, 0)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)
    
    def test_sysfont_setStylesNotFoundValidFont(self):
        fontname, bold, italic = pygame.sysfont.set_styles('notosanstaile', 1, 1)
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def todo_test_initsysfonts_win32(self):
        self.fail()

################################################################################

if __name__ == '__main__':
    unittest.main()
