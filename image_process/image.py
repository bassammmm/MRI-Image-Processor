from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from functools import partial
from kivy.uix.label import Label
import os
from kivy.uix.dropdown import DropDown

from kivy.lang.builder import Builder
Builder.load_file(os.path.abspath(os.path.join(os.path.dirname(__file__), 'imageprocess.kv')))



class ImageLabel(Label):
    color = (0,0,0,1)
    def __init__(self, **kwargs):
        super(ImageLabel, self).__init__(**kwargs)

        with self.canvas.before:
            Color(.5, .5, .5, 1)  # set the colour to red
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width/2.,
                                        self.height/2.))

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size






class ImageProcess(BoxLayout):
    selected_image_list = None
    touch_down_start = (0,0)
    touch_down_picture_select = (0,0)
    images_array = None
    image_1_scale = (.1942,.5307,.1052,.8987)
    image_2_scale = (.5968,.9526,.5545,.9488)
    image_3_scale = (.5968,.9520,0.0550,.4493)
    image_1_axis_length = (image_1_scale[1]-image_1_scale[0],image_1_scale[3]-image_1_scale[2])
    image_2_axis_length = (image_2_scale[1]-image_2_scale[0],image_2_scale[3]-image_2_scale[2])
    image_3_axis_length = (image_3_scale[1]-image_3_scale[0],image_3_scale[3]-image_3_scale[2])

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.image_1_left_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_left_scale.JPG'
        self.ids.image_1_bottom_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_bottom_scale.JPG'
        self.ids.image_2_left_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_left_scale2.JPG'
        self.ids.image_2_bottom_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_bottom_scale2.JPG'
        self.ids.image_3_left_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_left_scale2.JPG'
        self.ids.image_3_bottom_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__)) + '/final_images/view_2_bottom_scale2.JPG'
        dropdown = DropDown()
        for index in range(3):
            btn = Button(text='option %d' % index, size_hint_y=None, height=44, color=[0, 0, 0, 1],
                          background_normal='',
                          background_color=[1, 1, 1, 1])
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = self.ids.second_dropdown
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

    def load_images_in_window(self,images_structured_array):
        for image_array in images_structured_array:
            box = BoxLayout(orientation="vertical")
            box_image = AnchorLayout(size_hint_y=.8)
            box_image.anchor_x = "left"
            box_image.anchor_y = "top"
            box_image_name = BoxLayout(size_hint_y=.2)
            button = Button(background_normal=image_array[2][0])
            button.bind(on_press=self.click)

            box_image.add_widget(button)
            box_image.add_widget(Label(text="["+str(len(image_array[2]))+"]", color=(1, 1, 0, 1), size_hint=(.25, .16)))

            if len(image_array[1]) > 15:
                box_image_name.add_widget(ImageLabel(text=image_array[1][:15] + "..."))
            else:
                box_image_name.add_widget(ImageLabel(text=image_array[1]))
            box.add_widget(box_image)
            box.add_widget(box_image_name)
            self.ids.thumbnails.add_widget(box)

        self.images_array = images_structured_array


    def click(self,instance):
        for list_of_images in self.images_array:
            if instance.background_normal in list_of_images[2]:
                self.selected_image_list = list_of_images
        self.ids.image_1.canvas.before.children[-1].source = instance.background_normal

        if self.selected_image_list[3]!=[]:
            self.ids.image_2.canvas.before.children[-1].source = self.selected_image_list[3][0]
            self.ids.image_2_top_mid.text = "FRAME " + str(0) + "/" + str(len(self.selected_image_list[3]))
        else:
            self.ids.image_2.canvas.before.children[-1].source = ''
        if self.selected_image_list[4]!=[]:
            self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][0]
            self.ids.image_3_top_mid.text = "FRAME " + str(0) + "/" + str(len(self.selected_image_list[4]))
        else:
            self.ids.image_3.canvas.before.children[-1].source = ''

    def on_touch_down(self, touch):


        self.touch_down_start = touch.spos
        if touch.spos[0]>self.image_1_scale[0]  and touch.spos[0]<self.image_1_scale[1] and touch.spos[1]>self.image_1_scale[2] and touch.spos[1]<self.image_1_scale[3] and self.touch_down_start[0]>self.image_1_scale[0] and self.touch_down_start[0]<self.image_1_scale[1]:
            self.touch_down_picture_select = touch.spos
            self.ids.image_1_background.canvas.before.children[0].rgba = (1,1,0,1)
            #code for pointer
            win=self.ids.image_1
            ud=touch.ud
            ud['group'] = g = str(touch.uid)
            ud['color'] = 1
            xpos = self.image_1_scale[0]*Window.width
            ypos = self.image_1_scale[2]*Window.height
            with win.canvas.before:
                Color(ud['color'],1,1,mode='hsv',group=g)
                ud['lines']=[Rectangle(pos=(touch.x,ypos),size=(1,win.height),group=g),
                                Rectangle(pos=(xpos,touch.y),size=(win.width,1),group=g)]


        elif touch.spos[0]>self.image_2_scale[0] and touch.spos[0]<self.image_2_scale[1] and touch.spos[1]>self.image_2_scale[2] and touch.spos[1]<self.image_2_scale[3] and self.touch_down_start[0]>self.image_2_scale[0] and self.touch_down_start[0]<self.image_2_scale[1] and self.touch_down_start[1]>self.image_2_scale[2]:
            self.touch_down_picture_select = touch.spos
            self.ids.image_2_background.canvas.before.children[0].rgba = (1,1,0,1)
            # code for pointer
            win = self.ids.image_2
            ud = touch.ud
            ud['group'] = g = str(touch.uid)
            ud['color'] = 1
            xpos = self.image_2_scale[0] * Window.width
            ypos = self.image_2_scale[2] * Window.height
            with win.canvas.before:
                Color(ud['color'], 1, 1, mode='hsv', group=g)
                ud['lines'] = [Rectangle(pos=(touch.x, ypos), size=(1, win.height), group=g),
                               Rectangle(pos=(xpos, touch.y), size=(win.width, 1), group=g)]
        elif touch.spos[0]>self.image_3_scale[0] and touch.spos[0]<self.image_3_scale[1] and touch.spos[1]<self.image_3_scale[3] and touch.spos[1]>self.image_3_scale[2] and self.touch_down_start[0]<self.image_3_scale[1] and self.touch_down_start[0]>self.image_3_scale[0]  and self.touch_down_start[1]<self.image_3_scale[3]:
            self.touch_down_picture_select = touch.spos
            self.ids.image_3_background.canvas.before.children[0].rgba = (1,1,0,1)
            # code for pointer
            win = self.ids.image_3
            ud = touch.ud
            ud['group'] = g = str(touch.uid)
            ud['color'] = 1
            xpos = self.image_3_scale[0] * Window.width
            ypos = self.image_3_scale[2] * Window.height
            with win.canvas.before:
                Color(ud['color'], 1, 1, mode='hsv', group=g)
                ud['lines'] = [Rectangle(pos=(touch.x, ypos), size=(1, win.height), group=g),
                               Rectangle(pos=(xpos, touch.y), size=(win.width, 1), group=g)]

        return super(ImageProcess, self).on_touch_down(touch)





    def on_touch_up(self, touch):
        self.ids.image_1_background.canvas.before.children[0].rgba = (1, 0, 0, 1)
        self.ids.image_2_background.canvas.before.children[0].rgba = (1, 0, 0, 1)
        self.ids.image_3_background.canvas.before.children[0].rgba = (1, 0, 0, 1)
        try:
            ud = touch.ud
            self.ids.image_1.canvas.before.remove_group(ud['group'])
        except:
            pass
        try:
            ud = touch.ud
            self.ids.image_2.canvas.before.remove_group(ud['group'])
        except:
            pass
        try:
            ud = touch.ud
            self.ids.image_3.canvas.before.remove_group(ud['group'])
        except:
            pass


    def on_touch_move(self, touch):
        # print("Mouse x: ",touch.x)
        # print("Mouse y: ",touch.y)
        # print("Touch  :",touch)
        if touch.spos[0]>self.image_1_scale[0]  and touch.spos[0]<self.image_1_scale[1] and touch.spos[1]>self.image_1_scale[2] and touch.spos[1]<self.image_1_scale[3] and self.touch_down_start[0]>self.image_1_scale[0] and self.touch_down_start[0]<self.image_1_scale[1]:
            self.ids.image_1_background.canvas.before.children[0].rgba = (1,1,0,1)

            if self.ids.image_1.canvas.before.children[2].source != None:
                # self.ids.image_1_pos.text = "x:" + str(touch.spos[0])[:6] + " y:" + str(touch.spos[1])[:6]
                try:
                    #Logic for x axis:
                    max_x = self.image_1_axis_length[0]
                    num_x = len(self.selected_image_list[3])
                    input_num_x = touch.spos[0]-self.image_1_scale[0]

                    div_x = max_x / num_x
                    index_x = int((input_num_x / div_x))



                    # Logic for y axis:
                    max_y = self.image_1_axis_length[1]
                    num_y = len(self.selected_image_list[4])
                    input_num_y = touch.spos[1]-self.image_1_scale[2]
                    div_y = max_y / num_y
                    index_y = int(input_num_y / div_y)


                    self.ids.image_2.canvas.before.children[-1].source = self.selected_image_list[3][index_x]
                    self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][index_y]
                    self.ids.image_2_top_mid.text = "FRAME " + str(index_x) + "/" + str(len(self.selected_image_list[3]))
                    self.ids.image_3_top_mid.text = "FRAME " + str(index_y) + "/" + str(len(self.selected_image_list[4]))
                except:
                    pass

                ud = touch.ud
                xpos = self.image_1_scale[0] * Window.width
                ypos = self.image_1_scale[2] * Window.height
                ud['lines'][0].pos = touch.x,ypos
                ud['lines'][1].pos = xpos,touch.y






            else:
                pass





        elif touch.spos[0] > self.image_2_scale[0] and touch.spos[0] < self.image_2_scale[1] and touch.spos[1] > self.image_2_scale[2] and touch.spos[1] < self.image_2_scale[3] and self.touch_down_start[0] > self.image_2_scale[0] and self.touch_down_start[0] < self.image_2_scale[1] and self.touch_down_start[1] > self.image_2_scale[2]:
            self.ids.image_2_background.canvas.before.children[0].rgba = (1, 1, 0, 1)
            if self.ids.image_2.canvas.before.children[2].source != None:
                # self.ids.image_2_pos.text = "x:" + str(touch.spos[0])[:6] + " y:" + str(touch.spos[1])[:6]
                try:
                    # Logic for x axis:
                    max_x = self.image_2_axis_length[0]
                    num_x = len(self.selected_image_list[4])
                    input_num_x = touch.spos[0] - self.image_2_scale[0]

                    div_x = max_x / num_x
                    index_x = int((input_num_x / div_x))

                    # Logic for y axis:
                    max_y = self.image_2_axis_length[1]
                    num_y = len(self.selected_image_list[2])
                    input_num_y = touch.spos[1] - self.image_2_scale[2]
                    div_y = max_y / num_y
                    index_y = int(input_num_y / div_y)




                    self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][index_x]
                    self.ids.image_1.canvas.before.children[-1].source = self.selected_image_list[2][index_y]
                    self.ids.image_3_top_mid.text = "FRAME " + str(index_x) + "/" + str(len(self.selected_image_list[4]))
                    self.ids.image_1_top_mid.text = "FRAME " + str(index_y) + "/" + str(len(self.selected_image_list[2]))
                except:
                    pass

                ud = touch.ud
                xpos = self.image_2_scale[0] * Window.width
                ypos = self.image_2_scale[2] * Window.height
                ud['lines'][0].pos = touch.x, ypos
                ud['lines'][1].pos = xpos, touch.y
            else:
                pass






        elif touch.spos[0] > self.image_3_scale[0] and touch.spos[0] < self.image_3_scale[1] and touch.spos[1] < self.image_3_scale[3] and touch.spos[1] > self.image_3_scale[2] and self.touch_down_start[0] < self.image_3_scale[1] and self.touch_down_start[0] > self.image_3_scale[0] and self.touch_down_start[1]<self.image_3_scale[3]:
            self.ids.image_3_background.canvas.before.children[0].rgba = (1, 1, 0, 1)
            if self.ids.image_3.canvas.before.children[2].source != None:
                # self.ids.image_3_pos.text = "x:" + str(touch.spos[0])[:6] + " y:" + str(touch.spos[1])[:6]
                try:
                    # Logic for x axis:
                    max_x = self.image_3_axis_length[0]
                    num_x = len(self.selected_image_list[3])
                    input_num_x = touch.spos[0] - self.image_3_scale[0]
                    div_x = max_x / num_x
                    index_x = int((input_num_x / div_x))

                    # Logic for y axis:
                    max_y = self.image_3_axis_length[1]
                    num_y = len(self.selected_image_list[2])
                    input_num_y = touch.spos[1] - self.image_3_scale[2]
                    div_y = max_y / num_y
                    index_y = int(input_num_y / div_y)



                    self.ids.image_2.canvas.before.children[-1].source = self.selected_image_list[3][index_x]
                    self.ids.image_1.canvas.before.children[-1].source = self.selected_image_list[2][index_y]
                    self.ids.image_2_top_mid.text = "FRAME " + str(index_x) + "/" + str(len(self.selected_image_list[3]))
                    self.ids.image_1_top_mid.text = "FRAME " + str(index_y) + "/" + str(len(self.selected_image_list[2]))
                except:
                    pass

                ud = touch.ud
                xpos = self.image_3_scale[0] * Window.width
                ypos = self.image_3_scale[2] * Window.height
                ud['lines'][0].pos = touch.x, ypos
                ud['lines'][1].pos = xpos, touch.y
            else:
                pass

        else:
            pass



    def slider_image(self,*args):
        if self.selected_image_list!=None:
            if self.touch_down_picture_select[0] > self.image_1_scale[0] and self.touch_down_picture_select[0] < self.image_1_scale[1]:

                if self.selected_image_list != None:
                    max_slider = 1000
                    num_of_images_in_selected_list = len(self.selected_image_list[2])
                    input_number = args[1]
                    div = max_slider / num_of_images_in_selected_list
                    index = input_number / div
                    index = int(index)

                    if index > (len(self.selected_image_list[2]) - 1):
                        self.ids.image_1.canvas.before.children[-1].source = self.selected_image_list[2][index - 1]
                    else:
                        self.ids.image_1.canvas.before.children[-1].source = self.selected_image_list[2][index]

                    self.ids.image_1_top_mid.text = "FRAME "+str(index)+"/"+str(len(self.selected_image_list[2]))



            elif self.touch_down_picture_select[0] > self.image_2_scale[0] and self.touch_down_picture_select[0] < self.image_2_scale[1] and self.touch_down_picture_select[1] > self.image_2_scale[2]:

                if self.selected_image_list[3] != []:
                    max_slider = 1000
                    num_of_images_in_selected_list = len(self.selected_image_list[3])
                    input_number = args[1]
                    div = max_slider / num_of_images_in_selected_list
                    index = input_number / div
                    index = int(index)

                    if index > (len(self.selected_image_list[3]) - 1):
                        self.ids.image_2.canvas.before.children[-1].source = self.selected_image_list[3][index - 1]
                    else:
                        self.ids.image_2.canvas.before.children[-1].source =self.selected_image_list[3][index]

                    self.ids.image_2_top_mid.text = "FRAME " + str(index) + "/" + str(len(self.selected_image_list[3]))

            elif self.touch_down_picture_select[0] < self.image_3_scale[1] and self.touch_down_picture_select[0] > self.image_3_scale[0]  and self.touch_down_start[1]<self.image_3_scale[3]:

                if self.selected_image_list[4] != []:
                    max_slider = 1000
                    num_of_images_in_selected_list = len(self.selected_image_list[4])
                    input_number = args[1]
                    div = max_slider / num_of_images_in_selected_list
                    index = input_number / div
                    index = int(index)

                    if index > (len(self.selected_image_list[4]) - 1):
                        self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][index - 1]
                    else:
                        self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][index]
                    self.ids.image_3_top_mid.text = "FRAME " + str(index) + "/" + str(len(self.selected_image_list[3]))
            else:
                pass



    def from_previous_screen(self,selected_image_list):
        self.selected_image_list = selected_image_list
        self.ids.image_1.canvas.before.children[-1].source = self.selected_image_list[2][0]
        if self.selected_image_list[3]!=[]:
            self.ids.image_2.canvas.before.children[-1].source = self.selected_image_list[3][0]
        else:
            self.ids.image_2.canvas.before.children[-1].source = ''
        if self.selected_image_list[4]!=[]:
            self.ids.image_3.canvas.before.children[-1].source = self.selected_image_list[4][0]
        else:
            self.ids.image_3.canvas.before.children[-1].source = ''

    def back(self,instance):
        self.parent.parent.current='screen_image_first'
        self.parent.parent.transition.direction = "right"

class ImageProcessApp(App):
    def build(self):
        return ImageProcess()


if __name__ == '__main__':
    ImageProcessApp().run()