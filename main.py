from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os

from image_first.imagefirst import ImageFirst
from image_process.image import ImageProcess
from kivy.core.window import Window


class MainWindow(BoxLayout):

    image_first_widget = ImageFirst()
    image_process_widget = ImageProcess()

    initial_center = None

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.initial_center = Window.center

        Window.size = (1350, 700)

        variation_x = Window.center[0] - self.initial_center[0]
        variation_y = Window.center[1] - self.initial_center[1]

        Window.left -= variation_x
        Window.top -= variation_y



        #Path for view 1 folder
        path_view_1 = os.path.dirname(__file__)+'/final_images/view_1'
        view_1_images = []
        # Path for view 2 folder
        path_view_2 = os.path.dirname(__file__)+'/final_images/view_2'
        for r,d,f in os.walk(path_view_1):
            for filee in f:
                view_1_images.append(filee)

        #Create a structurized array of all the images in view 1
        view_1_images_structure_array = []
        view_1_images_structure_dict = {}
        for x in view_1_images:
            splitted = x.split('_')

            try:
                view_1_images_structure_dict[int(splitted[1])].append("_".join(splitted))
            except:
                view_1_images_structure_dict[int(splitted[1])] = ["_".join(splitted)]


        for key in sorted(view_1_images_structure_dict.keys()):
            list_images = view_1_images_structure_dict[key]
            list_images.sort(key = lambda x: int(x.split('_')[-1].split('.')[0]))
            list_images_name = list_images[0]
            list_images_name = " ".join(list_images_name.split('_')[2:-1])
            view_1_images_structure_array.append([key,list_images_name,[path_view_1+'/'+x for x in list_images]])


        #gets all ortho-x and ortho-y images
        #images must be in view_2 folder in final_images and they must be within a main folder of the image series
        #for example final_images/view_2/12/...
        #12 is the number of series from view 1
        print(__file__)
        list_of_view_2_folders = os.walk(path_view_2).__next__()[1]
        print("List of folders:",list_of_view_2_folders)
        list_of_view_2_orthos = []
        for x in list_of_view_2_folders:
            ortho_x = []
            try:
                for r,d,f in os.walk(path_view_2+"/"+x+"/ortho_x"):
                    for filee in f:
                        ortho_x.append(path_view_2+"/"+x+"/ortho_x/"+filee)
                ortho_x.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
            except:
                pass
            ortho_y = []
            try:
                for r,d,f in os.walk(path_view_2+"/"+x+"/ortho_y"):
                    for filee in f:
                        ortho_y.append(path_view_2+"/"+x+"/ortho_y/"+filee)
                ortho_y.sort(key= lambda x: int(x.split("_")[-1].split(".")[0]))
            except:
                pass

            list_of_view_2_orthos.append([x,ortho_x,ortho_y])



        for x in view_1_images_structure_array:
            for y in list_of_view_2_orthos:
                if str(x[0])==str(y[0]):
                    x.append(y[1])
                    x.append(y[2])




        for x in view_1_images_structure_array:
            try:
                print(x[3])
            except:
                x.append([])
                x.append([])

        #prints the array for you to see the implementation of it
        # the format is as following
        # [[seriesNum,seriesName,[first view],[ortho-x],[ortho-y]],......]
        # for x in view_1_images_structure_array:
        #     print(x[0])
        #     print(x[1])
        #     print(x[2])
        #     print(x[3])
        #     print(x[4])


        self.image_first_widget.load_images_in_window(view_1_images_structure_array)



        self.image_process_widget.load_images_in_window(view_1_images_structure_array)
        self.ids.screen_image_first.add_widget(self.image_first_widget)
        self.ids.screen_image_process.add_widget(self.image_process_widget)


class MainApp(App):

    def build(self):

        return MainWindow()

if __name__ == '__main__':
    MainApp().run()