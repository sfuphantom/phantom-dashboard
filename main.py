import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button 
from kivy.uix.relativelayout import RelativeLayout  
#UMBER_OF_BUTTONS = 2

#class MainApp(App):
 #   
    #for i in range(NUMBER_OF_BUTTONS):
     #   button = Button(pos_hint={'x': 0.2, 'center_y': .2}, size_hint=(.1, .1),text= '0')
      #  layout.add_widget(button)
        
#MainApp().run()
temp = 10
class MainWidget(Widget):
    pass

class mainApp(App):
    
    #def __init__(self, **kwargs):
     #   super(MainWidget, self).__init__(**kwargs)
      #  Clock.schedule_interval(self.animate_the_button, 1)

    def animate_the_button(self, widget, *args):
       anim = Animation(opacity=0)
       if temp < 20:
           anim.start(widget)
    
    def build(self):
       return MainWidget()
       #rl = RelativeLayout(size =(300, 300)) 

       #Button1 = Button(size_hint =(.2, .2),  
        #            pos_hint ={'center_x':.7, 'center_y':.5},  
         #           text ="pos_hint")  
  
       #rl.add_widget(Button1) 

       #return rl
   
        
if __name__ == "__main__":
    mainApp().run()