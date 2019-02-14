import unittest
import platform
import pygame.sysfont
import pygame.font

class SysfontModuleTest(unittest.TestCase):
    FONT = "notosanscjktcregular,notosansmonocjktcregular,notosansregular,microsoftjhengheimicrosoftjhengheiuilight,microsoftyaheimicrosoftyaheiuilight,msgothicmsuigothicmspgothic,msmincho,Arial"
    PREFERED_FONT = 'Arial'
    fonts = pygame.font.get_fonts()
    if PREFERED_FONT in fonts:
        # Try to use arial rather than random font based on installed fonts on the system.
        FONT = PREFERED_FONT + FONT
    else:
        FONT = sorted(fonts)[0]

    # def todo_test_create_aliases(self):
    #     self.fail()

    # def todo_test_initsysfonts(self):
    #     self.fail()

    @unittest.skipIf('Darwin' not in platform.platform(), 'Not mac we skip.')
    def test_initsysfonts_darwin(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 10)

    def test_sysfont_good(self):
        pygame.font.init()
        arial = pygame.font.SysFont(self.FONT, 40, 1, 0)
        self.assertTrue(arial.get_bold())
        self.assertFalse(arial.get_italic())

    @unittest.skipIf('Linux' not in platform.platform(), 'Not linux we skip.')
    def test_initsysfonts_unix(self):
        self.assertTrue(len(pygame.sysfont.get_fonts()) > 1)

    def test_sysfont_notRecognized(self):
        arial = pygame.sysfont.SysFont('1234567890', 40, 1, 1)
        self.assertTrue(arial.get_bold())
        self.assertTrue(arial.get_italic())

    @unittest.skipIf(not FONT, 'No font, skip')
    def test_sysfont_setFontName(self):
        fontname, bold, italic = pygame.sysfont.set_font_name(self.FONT, 0, 0)  
        self.assertTrue(fontname)
        self.assertFalse(bold)
        self.assertFalse(italic)

    def test_sysfont_setFontNameNoName(self):
        fontname = pygame.sysfont.set_font_name(None, 0, 0)  
        self.assertIsNone(fontname)

    @unittest.skipIf(not FONT, 'No font, skip')
    def test_sysfont_setNoStyles(self):
        fontname, bold, italic = pygame.sysfont.set_styles(self.FONT, 0, 0)  
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

    # def todo_test_initsysfonts_win32(self):
    #     self.fail()

################################################################################

if __name__ == '__main__':
    unittest.main()
