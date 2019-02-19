# coding: ascii
# pygame - Python Game Library
# Copyright (C) 2000-2003  Pete Shinners
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Pete Shinners
# pete@shinners.org
"""sysfont, used in the font module to find system fonts"""

import os
import sys
from pygame.compat import xrange_, PY_MAJOR_VERSION
from os.path import basename, dirname, exists, join, splitext
import xml.etree.ElementTree as ET


OpenType_extensions = frozenset(('.ttf', '.ttc', '.otf'))
Sysfonts = {}
Sysalias = {}

# Python 3 compatibility
if PY_MAJOR_VERSION >= 3:
    def toascii(raw):
        """convert bytes to ASCII-only string"""
        return raw.decode('ascii', 'ignore')
    if os.name == 'nt':
        import winreg as _winreg
    else:
        import subprocess
else:
    def toascii(raw):
        """return ASCII characters of a given unicode or 8-bit string"""
        return raw.decode('ascii', 'ignore')
    if os.name == 'nt':
        import _winreg
    else:
        import subprocess


def _simplename(name):
    """create simple version of the font name"""
    # return alphanumeric characters of a string (converted to lowercase)
    return ''.join(c.lower() for c in name if c.isalnum())


def _addfont(name, bold, italic, font, fontdict):
    """insert a font and style into the font dictionary"""
    if name not in fontdict:
        fontdict[name] = {}
    fontdict[name][bold, italic] = font


def initsysfonts_win32():
    """initialize fonts dictionary on Windows"""

    fontdir = join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')

    TrueType_suffix = '(TrueType)'
    mods = ('demibold', 'narrow', 'light', 'unicode', 'bt', 'mt')

    fonts = {}

    # add fonts entered in the registry

    # find valid registry keys containing font information.
    # http://docs.python.org/lib/module-sys.html
    # 0 (VER_PLATFORM_WIN32s)          Win32s on Windows 3.1
    # 1 (VER_PLATFORM_WIN32_WINDOWS)   Windows 95/98/ME
    # 2 (VER_PLATFORM_WIN32_NT)        Windows NT/2000/XP
    # 3 (VER_PLATFORM_WIN32_CE)        Windows CE
    if sys.getwindowsversion()[0] == 1:
        key_name = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Fonts"
    else:
        key_name = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts"
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_name)

    # Could be split up
    for i in xrange_(_winreg.QueryInfoKey(key)[1]):
        try:
            # name is the font's name e.g. Times New Roman (TrueType)
            # font is the font's filename e.g. times.ttf
            name, font = _winreg.EnumValue(key, i)[0:2]
        except EnvironmentError:
            break

        # try to handle windows unicode strings for file names with
        # international characters
        if PY_MAJOR_VERSION < 3:
            # here are two documents with some information about it:
            # http://www.python.org/peps/pep-0277.html
            # https://www.microsoft.com/technet/archive/interopmigration/linux/mvc/lintowin.mspx#ECAA
            try:
                font = str(font)
            except UnicodeEncodeError:
                # MBCS is the windows encoding for unicode file names.
                try:
                    font = font.encode('MBCS')
                except:
                    # no success with str or MBCS encoding... skip this font.
                    continue

        if splitext(font)[1].lower() not in OpenType_extensions:
            continue
        if not dirname(font):
            font = join(fontdir, font)

        if name.endswith(TrueType_suffix):
            name = name.rstrip(TrueType_suffix).rstrip()
        name = name.lower().split()

        bold = italic = 0
        for m in mods:
            if m in name:
                name.remove(m)
        if 'bold' in name:
            name.remove('bold')
            bold = 1
        if 'italic' in name:
            name.remove('italic')
            italic = 1
        name = ''.join(name)

        name = _simplename(name)

        _addfont(name, bold, italic, font, fonts)

    return fonts


def _add_font_paths(sub_elements, fonts):
    """ Gets each element, checks its tag content,
        if wanted fetches the next value in the iterable
    """
    font_name = font_path = None
    for tag in sub_elements:
        if tag.text == "_name":
            font_name = next(sub_elements).text
            if splitext(font_name)[1] not in OpenType_extensions:
                break
            bold = "bold" in font_name
            italic = "italic" in font_name
        if tag.text == "path" and font_name is not None:
            font_path = next(sub_elements).text
            _addfont(_simplename(font_name),bold,italic,font_path,fonts)
            break


def _system_profiler_darwin():
    fonts = {}
    flout, flerr = subprocess.Popen(
        ' '.join(['system_profiler', '-xml','SPFontsDataType']),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True
    ).communicate()

    for font_node in ET.fromstring(flout).iterfind('./array/dict/array/dict'):
        _add_font_paths(font_node.iter("*"), fonts)

    return fonts



def initsysfonts_darwin():
    """ Read the fonts on MacOS, and OS X.
    """
    # if the X11 binary exists... try and use that.
    #  Not likely to be there on pre 10.4.x ... or MacOS 10.10+
    if exists('/usr/X11/bin/fc-list'):
        fonts = initsysfonts_unix('/usr/X11/bin/fc-list')
    # This fc-list path will work with the X11 from the OS X 10.3 installation
    # disc
    elif exists('/usr/X11R6/bin/fc-list'):
        fonts = initsysfonts_unix('/usr/X11R6/bin/fc-list')
    elif exists('/usr/sbin/system_profiler'):
        try:
            fonts = _system_profiler_darwin()
        except:
            fonts = {}
    else:
        fonts = {}

    return fonts


# read the fonts on unix
def initsysfonts_unix(path="fc-list"):
    """use the fc-list from fontconfig to get a list of fonts"""
    fonts = {}

    try:
        # note, we capture stderr so if fc-list isn't there to stop stderr
        # printing.
        flout, flerr = subprocess.Popen('%s : file family style' % path, shell=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        close_fds=True).communicate()
    except Exception:
        return fonts

    entries = toascii(flout)
    try:
        for line in entries.split('\n'):

            try:
                filename, family, style = line.split(':', 2)
                if splitext(filename)[1].lower() in OpenType_extensions:
                    bold = 'Bold' in style
                    italic = 'Italic' in style
                    oblique = 'Oblique' in style
                    for name in family.strip().split(','):
                        if name:
                            break
                    else:
                        name = splitext(basename(filename))[0]

                    _addfont(
                        _simplename(name), bold, italic or oblique, filename, fonts)

            except Exception:
                # try the next one.
                pass

    except Exception:
        pass

    return fonts


def create_aliases():
    """map common fonts that are absent from the system to similar fonts that are installed in the system"""
    alias_groups = (
        ('monospace', 'misc-fixed', 'courier', 'couriernew', 'console',
         'fixed', 'mono', 'freemono', 'bitstreamverasansmono',
         'verasansmono', 'monotype', 'lucidaconsole'),
        ('sans', 'arial', 'helvetica', 'swiss', 'freesans',
         'bitstreamverasans', 'verasans', 'verdana', 'tahoma'),
        ('serif', 'times', 'freeserif', 'bitstreamveraserif', 'roman',
         'timesroman', 'timesnewroman', 'dutch', 'veraserif',
         'georgia'),
        ('wingdings', 'wingbats'),
    )
    for alias_set in alias_groups:
        for name in alias_set:
            if name in Sysfonts:
                found = Sysfonts[name]
                break
        else:
            continue
        for name in alias_set:
            if name not in Sysfonts:
                Sysalias[name] = found


# initialize it all, called once
def initsysfonts():
    if sys.platform == 'win32':
        fonts = initsysfonts_win32()
    elif sys.platform == 'darwin':
        fonts = initsysfonts_darwin()
    else:
        fonts = initsysfonts_unix()
    Sysfonts.update(fonts)
    create_aliases()
    if not Sysfonts:  # dummy so we don't try to reinit
        Sysfonts[None] = None


# pygame.font specific declarations
def font_constructor(fontpath, size, bold, italic):
    import pygame.font

    font = pygame.font.Font(fontpath, size)
    if bold:
        font.set_bold(1)
    if italic:
        font.set_italic(1)

    return font


# the exported functions

def SysFont(name, size, branchArray, bold=False, italic=False, constructor=None):
    """pygame.font.SysFont(name, size, bold=False, italic=False, constructor=None) -> Font
       create a pygame Font from system font resources

       This will search the system fonts for the given font
       name. You can also enable bold or italic styles, and
       the appropriate system font will be selected if available.

       This will always return a valid Font object, and will
       fallback on the builtin pygame font if the given font
       is not found.

       Name can also be a comma separated list of names, in
       which case set of names will be searched in order. Pygame
       uses a small set of common font aliases, if the specific
       font you ask for is not available, a reasonable alternative
       may be used.

       if optional contructor is provided, it must be a function with
       signature constructor(fontpath, size, bold, italic) which returns
       a Font instance. If None, a pygame.font.Font object is created.
    """
    #0
    branchArray[0] = True
    if constructor is None:
        #1
        branchArray[1] = True
        constructor = font_constructor

    #2
    branchArray[2] = True
    if not Sysfonts:
        #3
        branchArray[3] = True
        initsysfonts()

    #4
    branchArray[4] = True
    gotbold = gotitalic = False
    fontname = None

    fontname, gotbold, gotitalic = get_font_name(name, branchArray, bold, italic)

    set_bold = set_italic = False
    if bold and not gotbold:
        #25
        branchArray[25] = True
        set_bold = True
    #26
    branchArray[26] = True
    if italic and not gotitalic:
        #27
        branchArray[27] = True
        set_italic = True

    #28
    branchArray[28] = True
    return constructor(fontname, size, set_bold, set_italic)

def get_font_name(name, branchArray, bold=False, italic=False):
    """get_font_name(name, bold=False, italic=False) -> fontname, bold, italic
       Loops through list of comma separated font names. Returns the first 
       font name it finds in the system.
    """
    #5
    branchArray[5] = True
    if not name:
        #6
        branchArray[6] = True
        return None

    #7
    branchArray[7] = True
    gotbold = gotitalic = False
    fontname = None
    allnames = name
    for name in allnames.split(','):
        #8
        branchArray[8] = True
        name = _simplename(name)

        fontname, gotbold, gotitalic = get_styles(name, branchArray, bold, italic)
        if fontname:
            #22
            branchArray[22] = True
            break

        #23
        branchArray[23] = True
    #24
    branchArray[24] = True
    return fontname, gotbold, gotitalic

def get_styles(name, branchArray, bold=False, italic=False):
    """get_styles(name, bold=False, italic=False) -> fontname, bold, italic
       Tries to get styles for a specific font name, if the specific
       font you ask for is not available, a reasonable alternative
       may be used.
    """
    #9
    branchArray[9] = True
    styles = Sysfonts.get(name)
    if not styles:
        #10
        branchArray[10] = True
        styles = Sysalias.get(name)

    #11
    branchArray[11] = True
    gotbold = gotitalic = False
    fontname = None

    if not styles:
        #12
        branchArray[12] = True
        return fontname, gotbold, gotitalic
        
    #13
    branchArray[13] = True
    plainname = styles.get((False, False))
    fontname = styles.get((bold, italic))
    if not fontname and not plainname:
        #14
        branchArray[14] = True
        # Neither requested style, nor plain font exists, so
        # return a font with the name requested, but an
        # arbitrary style.
        (style, fontname) = list(styles.items())[0]
        # Attempt to style it as requested. This can't
        # unbold or unitalicize anything, but it can
        # fake bold and/or fake italicize.
        if bold and style[0]:
            #15
            branchArray[15] = True
            gotbold = True
        #16
        branchArray[16] = True
        if italic and style[1]:
            #17
            branchArray[17] = True
            gotitalic = True
        #18
        branchArray[18] = True
    elif not fontname:
        #19
        branchArray[19] = True
        fontname = plainname
    elif plainname != fontname:
        #20
        branchArray[20] = True
        gotbold = bold
        gotitalic = italic
    #21
    branchArray[21] = True
    return fontname, gotbold, gotitalic

def get_fonts():
    """pygame.font.get_fonts() -> list
       get a list of system font names

       Returns the list of all found system fonts. Note that
       the names of the fonts will be all lowercase with spaces
       removed. This is how pygame internally stores the font
       names for matching.
    """
    if not Sysfonts:
        initsysfonts()
    return list(Sysfonts)


def match_font(name, branchArray, bold=0, italic=0):
    """pygame.font.match_font(name, bold=0, italic=0) -> name
       find the filename for the named system font

       This performs the same font search as the SysFont()
       function, only it returns the path to the TTF file
       that would be loaded. The font name can be a comma
       separated list of font names to try.

       If no match is found, None is returned.
    """
    #0
    branchArray[0] = True
    if not Sysfonts:
        #1
        branchArray[1] = True
        initsysfonts()

    #2
    branchArray[2] = True
    fontname = None
    allnames = name
    for name in allnames.split(','):
        #3
        branchArray[3] = True
        name = _simplename(name)
        styles = Sysfonts.get(name)
        if not styles:
            #4
            branchArray[4] = True
            styles = Sysalias.get(name)
        #5
        branchArray[5] = True
        if styles:
            #6
            branchArray[6] = True
            while not fontname:
                #7
                branchArray[7] = True
                fontname = styles.get((bold, italic))
                if italic:
                    #8
                    branchArray[8] = True
                    italic = 0
                elif bold:
                    #9
                    branchArray[9] = True
                    bold = 0
                elif not fontname:
                    #10
                    branchArray[10] = True
                    fontname = list(styles.values())[0]
            #11
            branchArray[11] = True
        #12
        branchArray[12] = True
        if fontname:
            #13
            branchArray[13] = True
            break
        #13
        branchArray[13] = True
    #14
    branchArray[14] = True
    return fontname
