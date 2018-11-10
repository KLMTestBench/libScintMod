from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import widgets,Layout

class printTextArea:
    def __init__(self, Name,BufferSize=10000,height='500px'): 
        l = Layout(flex='0 1 auto', height=height, min_height='40px', width='auto')
        self.BufferSize=BufferSize
        self.tba = widgets.Textarea(
        value='',
        placeholder='Type something',
        description=Name,
        disabled=False,
        layout=l
        )
        display(self.tba)
        
    def __call__(self, textUpdate):
        dummy = self.tba.value + textUpdate
        self.tba.value = dummy[-self.BufferSize:]
        