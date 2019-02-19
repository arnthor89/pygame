import unittest
import cursors_test
import draw_test
import sysfont_test
import sprite_test
import threads_test

# Coverage tool for measuring how much of a function is covered by tests
# Note: Is currently only supported by pytohn 3.x not python 2.x
class coverageTool():
    def __init__(self):
        self.TrueCount = 0
        self.totCount = 0
        self.branchArray = {}
        self.branchArray['load_xbm'] = [False] * 28
        self.branchArray['compile'] = [False] * 15
        self.branchArray['_draw_line'] = [False] * 18
        self.branchArray['clip_line'] = [False] * 23
        self.branchArray['draw'] = [False] * 49
        self.branchArray['sysfont'] = [False] * 27
        self.branchArray['match_font'] = [False] * 15
        self.branchArray['add'] = [False] * 24
        self.branchArray['tmap'] = [False] * 27
        self.branchArray['has'] = [False] * 25

    def run(self):
        # Test for load_xbm
        ct = cursors_test.CursorsModuleTest()
        ct.test_load_xbm(self.branchArray['load_xbm'])

        # Test for compile
        ct = cursors_test.CursorsModuleTest()
        ct.test_compile(self.branchArray['compile'])

        # Test for _draw_line and clip_line functions (the 2 are done at the same time becasue the belong to the same file)
        ct = draw_test.PythonDrawLineTest()
        ct.test_line_color(self.branchArray['_draw_line'], self.branchArray['clip_line'])
        ct.test_line_gaps(self.branchArray['_draw_line'], self.branchArray['clip_line'])
        ct.test_lines_color(self.branchArray['_draw_line'], self.branchArray['clip_line'])
        ct.test_lines_gaps(self.branchArray['_draw_line'], self.branchArray['clip_line'])
        # Test I added specifically for _draw_line funciton (so only one branchArray is needed)
        ct.test__draw_line_rather_horizontal_1(self.branchArray['_draw_line'])
        ct.test__draw_line_rather_horizontal_2(self.branchArray['_draw_line'])
        ct.test__draw_line_rather_vertical_1(self.branchArray['_draw_line'])
        ct.test__draw_line_rather_vertical_2(self.branchArray['_draw_line'])
        ct.test__draw_line_invalid_points(self.branchArray['_draw_line'])

        # Test for draw function
        ct = sprite_test.LayeredDirtyTypeTest__DirtySprite()
        ct.setUp(self.branchArray['draw'])
        ct.test_repaint_rect(self.branchArray['draw'])
        ct.test_repaint_rect_with_clip(self.branchArray['draw'])

        # New Tests for clip_line
        ct = draw_test.ClipLineTest()
        ct.test_clip_line1(self.branchArray['clip_line'])
        ct.test_clip_line2(self.branchArray['clip_line'])


        # Test for sysfont function
        ct = sysfont_test.SysfontModuleTest()
        ct.test_sysfont(self.branchArray['sysfont'])

        # Test for sysfont function
        ct = sysfont_test.SysfontModuleTest()
        ct.test_match_font_known(self.branchArray['match_font'])
        ct.test_match_font_unkown(self.branchArray['match_font'])
        ct.test_match_font_none(self.branchArray['match_font'])

        # Test for add, need new instances of the test bc they update the same attribute
        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])     
        ct.test_get_layer_of_sprite(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__sprite_with_layer_attribute(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__passing_layer_keyword(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__overriding_sprite_layer_attr(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__spritelist(self.branchArray['add'])
        
        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__spritelist_with_layer_attr(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__spritelist_passing_layer(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__spritelist_overriding_layer(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_remove__sprite(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_sprites(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_layers(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_add__layers_are_correct(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_change_layer(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_get_top_layer(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_get_bottom_layer(self.branchArray['add'])
        
        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_move_to_front(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_move_to_back(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_get_top_sprite(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_get_sprites_from_layer(self.branchArray['add'])

        ct = sprite_test.LayeredUpdatesTypeTest__SpriteTest()
        ct.setUp(self.branchArray['add'])
        ct.test_switch_layer(self.branchArray['add'])

        # Test for tmap function
        ct = threads_test.ThreadsModuleTest()
        ct.test_init()
        ct.test_tmap(self.branchArray['tmap'])
        ct.test_tmap__wait(self.branchArray['tmap'])
        ct.test_quit()

        # Test for has
        ct = sprite_test.AbstractGroupTypeTest()
        ct.setUp(self.branchArray['has'])
        ct.test_has(self.branchArray['has'])

        ct = sprite_test.AbstractGroupTypeTest()
        ct.setUp(self.branchArray['has'])
        ct.test_remove(self.branchArray['has'])

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
        self.present("pygame.sprite.draw", self.branchArray['draw'])
        self.present("pygame.sysfont.sysfont", self.branchArray['sysfont'])
        self.present("pygame.sysfont.match_font", self.branchArray['match_font'])
        self.present("pygame.sprite.add", self.branchArray['add'])
        self.present("pygame.threads.__init__.tmap", self.branchArray['tmap'])
        self.present("pygame.sprite.has", self.branchArray['has'])

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
