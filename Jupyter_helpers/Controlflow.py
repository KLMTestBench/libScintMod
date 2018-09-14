from IPython.display import Javascript, display
from ipywidgets import widgets


def run_all(ev):
    display(Javascript('IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, IPython.notebook.ncells())'))

def button_run_below(description="Run all below"):
    button = widgets.Button(description=description)
    button.on_click(run_all)
    display(button)
    return button