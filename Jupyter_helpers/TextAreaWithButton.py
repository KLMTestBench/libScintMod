from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import widgets,Layout

class TextAreaWithButton:
    def __init__(self, Func=None,Name="textArea",FunctionName="Button", BufferSize=10000,height='500px'): 
        l = Layout(flex='0 1 auto', height=height, min_height='40px', width='auto')
        self.BufferSize=BufferSize
        self.tba = widgets.Textarea(
        value='',
        placeholder='Type something',
        description=Name,
        disabled=False,
        layout=l
        )
        self.button = widgets.Button(description=FunctionName)
        self.Func = Func
        
        self.button.on_click(self.pressButton)

        
    def __call__(self, textUpdate):
        dummy = self.tba.value + textUpdate
        self.tba.value = dummy[-self.BufferSize:]
        
    def setFunction(self,Func):
        self.Func = Func
        
    def Display(self):
        display(self.button)
        display(self.tba)
        
    def pressButton(self,x):
        self.tba.value = ""
        self.Func()
        
        