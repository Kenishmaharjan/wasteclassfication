import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image,AsyncImage
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.button import Button
from kivy.uix.camera import Camera
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import load_img
from keras.models import load_model

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (720, 720)
        size_hint_y: 2
        height: 50
        play: False
    GridLayout:
        cols: 1
        size_hint: (1,0.6)
        id: c
        Button:
            text: 'start/stop'
            size_hint_y: None
            height: '25dp'
            on_press:camera.play=not camera.play
            on_press:root.n()
            on_press:root.clear()
  
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '25dp'
            on_press: root.capture()
            on_press:camera.play=not camera.play
            on_press:root.n()
            
        Button:
            text: 'check'
            size_hint_y: None
            height: '25dp'
            on_press:root.model()     
        
        Button:
            text: "Upload Image"
            size_hint_y: None
            height: '25dp'
            play:False
            markup:False
            on_press: root.select_image()   
           
    Label:
        id:result
        text:"Message"
        size_hint_y: .15
        height: .001
<rButton@Button>
	background_color: (0,0,0,0)
	background_normal: ''
    border :(100, 100, 100, 160)
	canvas.before:
		Color:
			rgba: (48/255,84/255,150/255,1)
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: [15]
            
        
''')

class CameraClick(BoxLayout):
    i=0
    f=""
    t=True
    c=False
    def n(self):
        print(self.c)
        self.c=not self.c
        print('camera',self.c)
    def select_image(self):
        from kivy.core.window import Window
        from kivy.uix.filechooser import FileChooserIconView
        self.t=True
        print(self.t)

        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView(path=os.path.expanduser("~"))
        content.add_widget(file_chooser)
        popup = Popup(title="Choose an image file", content=content, size_hint=(0.9, 0.9))

        def load(instance):
            try:
                file_path = file_chooser.selection[0]
                self.ids.camera.source = file_path
       
                self.f=file_path
                print(file_path)
            
            except:
                self.ids.result.text="select first then press load"
                m="select first then press load"
                label=Label(text=m, size_hint_y=None, height=50)
            popup.dismiss()
        def dismiss(instance):
            popup.dismiss()

        
        if self.c==True:
             m="First press stop camera to upload image"
        else:
            m=''
        label=Label(text=m, size_hint_y=None, height=50)
        button = Button(text="Load", size_hint_y=None, height=50)
        button1 = Button(text="cancel", size_hint_y=None, height=50)
        button.bind(on_press=load)
        button1.bind(on_press=dismiss)
        content.add_widget(button)
        content.add_widget(button1)
        content.add_widget(label)
        
        if self.c==True:
            self.ids.result.text='First press stop camera to upload image'
        else:
             popup.open()
    def clear(self):
        if self.c==True:
            self.ids.result.text='                                '

    def capture(self):
        self.t=False
        print(self.t)
        self.i=str(self.i)
        print("for capture")
        print(self.i)
        camera = self.ids['camera']

        img=r"C:\Users\Dell\OneDrive\Desktop\waste_classfication\a"+self.i+".jpeg" # Change the loaction as per your pc where you want to save photo
        self.d=img
        print(img)
        camera.export_to_png(img)
        self.f=img
        self.ids.camera.source = img
        
        self.i=int(self.i)
        self.i=self.i+1
     
    def model(self):
        if self.t==True:
            image_path=self.f
        else:
            self.i=self.i-1
            self.i=str(self.i)
            image_path=r"C:\Users\Dell\OneDrive\Desktop\waste_classfication\a"+self.i+".jpeg" # Change the loaction as per your pc where the photo is save
        
        print("for model")
        print(self.i)
        print(image_path)
        model = load_model(r"C:\Users\Dell\OneDrive\Desktop\waste_classfication\final_model.h5")# Change the loaction as per your pc where the H5 model is save
        try:
            test_image = load_img(image_path,target_size = (150,150,3))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image,axis = 0)
            predictions=model.predict(test_image)
            scores=tensorflow.nn.softmax(predictions[0])
            scores=scores.numpy()
            print(scores)
            score=scores*100
            print(score)
            if score[0]>70:
              p="This is biodegradable"
            elif score[1]>70:
                p="This is Non-biodegradable"
            else:
                p="Can not verify please try again"
            print(p)
            self.ids.result.text=p
        except:
            self.ids.result.text='Capture or upload first'
        self.i=int(self.i)
class waste(App):

    def build(self):
       
        return CameraClick()

waste().run()