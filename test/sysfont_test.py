import unittest
import platform
import pygame.sysfont
import pygame.font

class SysfontModuleTest(unittest.TestCase):
    FONT = None
    FONTSLIST = []
    PREFERED_FONT = 'Arial'
    UNKOWN_FONT = '1234567890'
    
    pygame.font.init()
    FONTSLIST = pygame.font.get_fonts()
    # FONTS = ",".join(FONTSLIST)
    if PREFERED_FONT in FONTSLIST:
        # Try to use arial rather than random font based on installed fonts on the system.
        FONT = PREFERED_FONT
    else:
        FONT = sorted(FONTSLIST)[0]

    # def todo_test_create_aliases(self):
    #     self.fail()

    # def todo_test_initsysfonts(self):
    #     self.fail()

    @unittest.skipIf('Darwin' not in platform.platform(), 'Not mac we skip.')
    def test_initsysfonts_darwin(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 10)

    @unittest.skipIf('Linux' not in platform.platform(), 'Not linux we skip.')
    def test_initsysfonts_unix(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 1)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_sysfont_known(self):
        font = pygame.font.SysFont(self.FONT, 40, 1, 1)
        self.assertTrue(font.get_bold())
        self.assertTrue(font.get_italic())

    def test_sysfont_unkown(self):
        font = pygame.sysfont.SysFont(self.UNKOWN_FONT, 40, 1, 1)
        self.assertTrue(font.get_bold())
        self.assertTrue(font.get_italic())

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_sysfont_setFontName(self):
        fontname, bold, italic = pygame.sysfont.get_font_name(self.FONT, 0, 0)  
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_sysfont_setFontNameWithStyles(self):
        fontname = pygame.sysfont.get_font_name(self.FONT, 1, 1)  
        self.assertTrue(fontname)

    def test_sysfont_setFontNameNoName(self):
        fontname = pygame.sysfont.get_font_name(None, 0, 0)  
        self.assertIsNone(fontname)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_sysfont_setNoStyles(self):
        fontname, bold, italic = pygame.sysfont.get_styles(self.FONT, 0, 0)  
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setStylesNoName(self):
        fontname, bold, italic = pygame.sysfont.get_styles(None, 0, 0)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setInvalidFont(self):
        fontname, bold, italic = pygame.sysfont.get_styles(self.UNKOWN_FONT, 1, 1)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)
    
    # def todo_test_initsysfonts_win32(self):
    #     self.fail()

################################################################################

if __name__ == '__main__':
    unittest.main()
