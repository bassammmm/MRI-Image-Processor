from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.dropdown import DropDown
import os
from kivy.lang.builder import Builder
Builder.load_file(os.path.abspath(os.path.join(os.path.dirname(__file__), 'imagefirst.kv')))

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

class ImageFirst(BoxLayout):
    selected_image_list = None
    images_array = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.ids.left_scale.canvas.before.children[-1].source = os.path.dirname(os.path.dirname(__file__))+'/final_images/scale_1.JPG'

        dropdownx = DropDown()
        for index in range(3):
            btnx = Button(text='option %d' % index, size_hint_y=None, height=44, color=[0, 0, 0, 1],
                          background_normal='',
                          background_color=[1, 1, 1, 1])
            btnx.bind(on_release=lambda btnx: dropdownx.select(btnx.text))
            dropdownx.add_widget(btnx)
        mainbuttonx = self.ids.first_dropdown
        mainbuttonx.bind(on_release=dropdownx.open)
        dropdownx.bind(on_select=lambda instance, x: setattr(mainbuttonx, 'text', x))

        # new = DropDown()
        # btn = Button(text='option %d', size_hint_y=None, height=44, color=[0, 0, 0, 1],
        #                   background_normal='',
        #                   background_color=[1, 1, 1, 1])
        # btn.bind(on_release=lambda btn: new.select(btn.text))
        # new.add_widget(btn)
        # d = self.ids.wow
        # d.bind(on_release=new.open)



    def load_images_in_window(self,images_structured_array):
        for image_array in images_structured_array:
            box = BoxLayout(orientation="vertical")
            box_image = AnchorLayout(size_hint_y=.8)
            box_image.anchor_x = "left"
            box_image.anchor_y = "top"
            box_image_name = BoxLayout(size_hint_y=.2)
            button = Button(background_normal=image_array[2][0])
            button.bind(on_press=self.click_first)

            box_image.add_widget(button)
            box_image.add_widget(Label(text="["+str(len(image_array[2]))+"]", color=(1, 1, 0, 1), size_hint=(.25, .16)))
            if len(image_array[1])>15:
                box_image_name.add_widget(ImageLabel(text=image_array[1][:15]+"..."))
            else:
                box_image_name.add_widget(ImageLabel(text=image_array[1]))
            box.add_widget(box_image)
            box.add_widget(box_image_name)
            self.ids.thumbnails_first.add_widget(box)

        self.images_array = images_structured_array

    def slider_first(self,*args):

        if self.selected_image_list!=None:
            max_slider = 1000
            num_of_images_in_selected_list = len(self.selected_image_list[2])
            input_number = args[1]
            div= max_slider/num_of_images_in_selected_list
            index = input_number/div
            index=int(index)
            print("Slider :",args[1])
            print("Index  :",index)
            if index>(len(self.selected_image_list[2])-1):
                self.ids.first_main_image.canvas.before.children[-1].source = self.selected_image_list[2][index-1]
            else:
                self.ids.first_main_image.canvas.before.children[-1].source = self.selected_image_list[2][index]


    def click_first(self,instance):
        self.ids.first_main_image.canvas.before.children[-1].source = instance.background_normal
        self.ids.first_main_image.canvas.before.children[-3].rgba = (1,1,1,1)

        self.ids.left_button.clear_widgets()
        button_mpr = Button(text="MPR")
        button_mpr.bind(on_press=self.mpr_func)
        self.ids.left_button.add_widget(button_mpr)
        for list_of_images in self.images_array:
            if instance.background_normal in list_of_images[2]:
                self.selected_image_list = list_of_images
        self.ids.top_left_text.text = "Image Set:-\n"+self.selected_image_list[1]


    def mpr_func(self,instance):
        self.parent.parent.current = 'screen_image_process'
        self.parent.parent.transition.direction = "left"
        self.parent.parent.parent.image_process_widget.from_previous_screen(self.selected_image_list)

    def press(self,instance):
        print(self.ids.image_box_layout.size_hint_x)
class ImageFirstApp(App):
    def build(self):
        return ImageFirst()


if __name__ == '__main__':
    ImageFirstApp().run()
