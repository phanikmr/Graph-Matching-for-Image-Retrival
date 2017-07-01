import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class ImageSelector(object):

    image = None
    button_click_event = None
    press_key_event = None
    show_obj = None

    def __init__(self, Image,Button_Click_Event=None,Press_Key_Event=None):
        self.image = Image

        if Button_Click_Event is None:
            self.button_click_event = self.on_click_event
        else:
            self.button_click_event = Button_Click_Event

        if Press_Key_Event is None:
            self.press_key_event = self.on_press_event
        else:
            self.press_key_event = Press_Key_Event

        fig = plt.figure()
        plt.axis('off')
        axmain = plt.axes([0, 0, 1, 1])
        
        self.show_obj= plt.imshow(self.image)
        
        fig.canvas.mpl_connect('button_release_event',self.button_click_event)
        fig.canvas.mpl_connect('key_press_event', self.press_key_event)


    def showImage(self):                        
        plt.show()

    def updateImage(self,Image=None):
        if Image is not None:
            self.show_obj.set_data(Image)
            plt.draw()

    def on_press_event(self,event):
        return event.key

    def on_click_event(self,event):  
        return {"button":event.button,"X":event.x,"Y":event.y,"X_data":event.xdata,"Y_data":event.ydata}