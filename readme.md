# Module to import from ipython notebooks

## Origin

This module is entirely the work of Adrian Price-Whelan, and was directly collated from his notebook
http://nbviewer.ipython.org/github/adrn/ipython/blob/1.x/examples/notebooks/Importing%20Notebooks.ipynb

## Usage

Place this module in a location on your python path, then add a config instruction to your `.ipython/profile_default/ipython_notebook_config.py`:

   c.InteractiveShellApp.exec_lines = [
    'import notebook_importing'
   ]
   
You will then be able to import directly from other ipython notebooks in every notebook session.