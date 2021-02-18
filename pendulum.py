from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Ellipse, Color, Line

from kivy.core.window import Window
from kivy.clock import Clock
import numpy as np

from kivy.uix.screenmanager import Screen, ScreenManager

from random import random as rand

import threading

x_0, y_0 = Window.size
x0, y0 = x_0/2, y_0


z = 1

class mainApp(App):
    
    def build(self):
        global c, s, lengs
        self.pend_no = 0
        self.bobs = []
        c = ScreenManager()
        s = Screen()
        B = Button(pos=(Window.width*0.02, Window.height*0.8),size_hint=(None, None) ,size=(100, 50))
        
        B.bind(on_release=self.add_pendlum)
        #B_.bind(on_release=self.start)
        s.add_widget(B)
        B_ = Button(pos=(Window.width*0.02, Window.height*0.7),size_hint=(None, None) ,size=(100, 50))
        B_.bind(on_release=self.start)
        s.add_widget(B_)
        
        lengs = np.linspace(0.35, 1, 30)
        #for i in range(len(lengs)):
        #    s.add_widget()
        c.add_widget(s)
        return c
    
    def add_pendlum(self, obj):
        if self.pend_no == 30:
            print('done')
            return
        bob = Bob_( 1 , (lengs[len(lengs)- (self.pend_no+1)])**2)#, (self.pend_no+1))
        self.bobs.append(bob)
        s.add_widget(bob)
        self.pend_no += 1
        
    def start(self, obj):
        for i in self.bobs:
            i.animate()
#proper final Bob class  
class Bob_(Widget):
    def __init__(self, mass, length, **kwargs):
        
        super(Bob_, self).__init__(**kwargs)
        global z
        self.next_point = 2 * z #int(round((100000 / (2*np.pi*np.sqrt(length/9.8)))/160))
        z += 1
        #print(self.next_point) #2 * next_point #  
        self.M = mass
        self.L = Window.height * length
        #print(self.L)
        self.points = []
        
        self.X = [(x0 - (Window.width * 0.25)),  (y0 - self.L)]
        
        self.X1 = (x0 - (Window.width * 0.25))
        self.X2 = (x0 + (Window.width * 0.25))

        for i in np.linspace(self.X1, self.X2, 5000):
            try:
                self.points.append( (i,  y0 - np.sqrt((self.L**2) - ((i-x0)**2)) )   )
                #print(i,  y0 - np.sqrt((self.L**2) - ((i-x0)**2)) )
            except:
                continue

        #print(self.points)
        self.count = 0
        self.positive = True
        with self.canvas:
            Color(rand(), rand(), rand(), 1)
            self.line = Line(points=[x0, y0, self.points[0][0], self.points[0][1]+40])
            self.circle = Ellipse(pos=(self.points[0][0] - 20, self.points[0][1]), size= (50, 50))
            
        #print((2*np.pi*np.sqrt((length)/9.8))/200)
        #Clock.schedule_interval(self.update, (2*np.pi*np.sqrt((length)/9.8))/200)

        #self.B_ = Button(pos=(Window.width*0.02, Window.height*0.7),size_hint=(None, None) ,size=(100, 50))
        #self.B_.bind(on_release=self.animate)
        #self.add_widget(self.B_)
    def animate(self):
        #print('animate')
        Clock.schedule_interval(self.update, 1.0/160.0)

    def update(self, dt):
        #print(dt)
        if self.positive == True:
            self.count += self.next_point
            if self.count >= 4999:
                self.positive = False
                return
            self.circle.pos = (self.points[self.count][0] - 20, self.points[self.count][1])
            self.line.points = [x0, y0, self.points[self.count][0], self.points[self.count][1]+40]
            
        elif self.positive == False:
            self.count -= self.next_point
            if self.count <= 0:
                self.positive = True
                return
            self.circle.pos = (self.points[self.count][0] - 20, self.points[self.count][1])
            self.line.points = [x0, y0, self.points[self.count][0], self.points[self.count][1]+40]
            

class Bob__(Widget):
    def __init__(self, mass, length,**kwargs):
        
        super(Bob__, self).__init__(**kwargs)
        #self.next_point = 2 * next_point #  int(round((5000 / (2*np.pi*np.sqrt(length/9.8) * 30))))
        self.M = mass
        self.L = Window.height * length
        self.length = length
        self.points = []
        
        self.X = [(x0 - (Window.width * 0.25)),  (y0 - self.L)]
        
        self.X1 = (x0 - (Window.width * 0.25))
        self.X2 = (x0 + (Window.width * 0.25))

        for i in np.linspace(self.X1, self.X2, 5000):
            try:
                self.points.append( (i,  y0 - np.sqrt((self.L**2) - ((i-x0)**2)) )   )
                #print(i,  y0 - np.sqrt((self.L**2) - ((i-x0)**2)) )
            except:
                continue

        #print(self.points)
        self.count = 0
        self.positive = True
        with self.canvas:
            Color(rand(), rand(), rand(), 1)
            self.line = Line(points=[x0, y0, self.points[0][0], self.points[0][1]+40])
            self.circle = Ellipse(pos=(self.points[0][0] - 20, self.points[0][1]), size= (40, 40))
            
        print((2*np.pi*np.sqrt((length)/9.8))/5000)
        #Clock.schedule_interval(self.update, (2*np.pi*np.sqrt((length)/9.8))/5000)
        #self.B_ = Button(pos=(Window.width*0.02, Window.height*0.7),size_hint=(None, None) ,size=(100, 50))
        #self.B_.bind(on_release=self.animate)
        #self.add_widget(self.B_)
        self.threadobj = threading.Thread(target=self.animate)

    def thread_start(self):
        self.threadobj.start()
    
    def animate(self):
        #print('animate')
        Clock.schedule_interval(self.update, (2*np.pi*np.sqrt((self.length)/9.8))/5000)

    def update(self, dt):
        #print(dt)
        if self.positive == True:
            self.count += 1
            if self.count >= 4999:
                self.positive = False
                return
            self.circle.pos = (self.points[self.count][0] - 20, self.points[self.count][1])
            self.line.points = [x0, y0, self.points[self.count][0], self.points[self.count][1]+40]
            
        elif self.positive == False:
            self.count -= 1
            if self.count <= 0:
                self.positive = True
                return
            self.circle.pos = (self.points[self.count][0] - 20, self.points[self.count][1])
            self.line.points = [x0, y0, self.points[self.count][0], self.points[self.count][1]+40]            

#ine with proper physics
class Bob(Widget):
    def __init__(self,y,m, **kwargs):
        super(Bob, self).__init__(*kwargs)
        self.m = m
        self.R = np.zeros(2)
        self.V = np.zeros(2)
        self.T = np.zeros(2)
        self.W = np.array([0.0, 9.8*self.m])
        self.R[0], self.R[1] = (x0 - (Window.width * 0.25)),  (y0 - (Window.height * (1 - y)))
        
        with self.canvas:
            Color(.234, .456, .678, .8)
            self.circle = Ellipse(pos=(self.R[0], self.R[1]), size= (50, 50))

        Clock.schedule_interval(self.update, 1.0/(60.0))


    def update(self, dt):

        self.T[0] = self.m*(9.8)*((np.absolute(x0-self.R[0]))/np.sqrt((x0 - self.R[0])**2  + (y0 - self.R[1])**2 ))
        self.T[1] = self.m*(9.8)*((np.absolute(y0-self.R[1]))/np.sqrt((x0 - self.R[0])**2  + (y0 - self.R[1])**2 ))
        print(self.T)
        print(self.R, self.V)
        self.R = self.R + self.V * dt
        self.V[0] = self.V[0] + (((self.T[0])/self.m)*dt)
        self.V[1] = self.V[1] + ((self.T[1] - (self.m*9.8))/self.m ) * dt
        
        self.circle.pos = self.R


mainApp().run()
