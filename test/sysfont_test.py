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

    def todo_test_create_aliases(self):
        self.fail()

    def todo_test_initsysfonts(self):
        self.fail()

    @unittest.skipIf('Darwin' not in platform.platform(), 'Not mac we skip.')
    def test_initsysfonts_darwin(self):
        self.assertGreater(len(pygame.sysfont.get_fonts()), 10)

    # def test_sysfont(self, branchArray):
    #     arial = pygame.font.SysFont('Arial', 40, branchArray)

    @unittest.skipIf('Linux' not in platform.platform(), 'Not linux we skip.')
    def test_initsysfonts_unix(self):
        self.assertGreater(len(pygame.sysfont.get_fonts()), 1)

    @unittest.skipIf('Windows' not in platform.system(), 'Not win we skip.')
    def test_initsysfonts_win32(self):
        fonts = pygame.sysfont.initsysfonts_win32()
        self.assertTrue(fonts)
        
    def test_get_fonts(self):
        self.assertGreater(len(pygame.sysfont.get_fonts()), 1)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_sysfont_known(self, branchArray):
        font = pygame.font.SysFont(self.FONT, 40, branchArray, 1, 1)
        self.assertIsNotNone(font)
        self.assertTrue(font.get_bold())
        self.assertTrue(font.get_italic())

    def test_sysfont_unkown(self, branchArray):
        font = pygame.sysfont.SysFont(self.UNKOWN_FONT, 40, branchArray, 1, 1)
        self.assertIsNotNone(font)
        self.assertTrue(font.get_bold())
        self.assertTrue(font.get_italic())

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_get_font_name(self, branchArray):
        fontname, bold, italic = pygame.sysfont.get_font_name(self.FONT, branchArray, 0, 0)  
        self.assertIsNotNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_get_font_name_with_styles(self, branchArray):
        fontname = pygame.sysfont.get_font_name(self.FONT, branchArray, 1, 1)  
        self.assertIsNotNone(fontname)

    def test_get_font_name_none(self, branchArray):
        fontname = pygame.sysfont.get_font_name(None, branchArray, 0, 0)  
        self.assertIsNone(fontname)

    @unittest.skipIf(not FONT, 'No fonts found, skip')
    def test_get_styles(self, branchArray):
        fontname, bold, italic = pygame.sysfont.get_styles(self.FONT, branchArray, 0, 0)  
        self.assertIsNotNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_get_styles_none(self, branchArray):
        fontname, bold, italic = pygame.sysfont.get_styles(None, branchArray, 0, 0)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_set_styles_unkown(self, branchArray):
        fontname, bold, italic = pygame.sysfont.get_styles(self.UNKOWN_FONT, branchArray, 1, 1)  
        self.assertIsNone(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_match_font_known(self, branchArray):
        font = pygame.sysfont.match_font(self.FONT, branchArray, 1, 1)
        self.assertTrue(font)
        self.assertTrue(font.endswith((".ttf", ".ttc", "otf", "eot", "woff", "svg")))

    def test_match_font_unkown(self, branchArray):
        font = pygame.sysfont.match_font('1234567890', branchArray)
        self.assertIsNone(font)

    def test_match_font_none(self, branchArray):
        self.assertRaises(Exception, pygame.sysfont.match_font, None, branchArray)

################################################################################

if __name__ == '__main__':
    unittest.main()
