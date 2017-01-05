# Interactive Module to import from ipython notebooks

## Origin

This was started as an import module by [Adrian Price-Whelan][0], concatenated by [Robert Clewley][1], updated by [Doug Callaway][2], and finally recycled for an interactive console by me. 

[0]: http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Importing%20Notebooks.html
[1]: https://gist.github.com/robclewley/75b7719119892b99d73b
[2]: https://gist.github.com/DCAL12/1a872bd63bedfb7b12612c8a7ec0f52e

## Installation

```
git clone https://github.com/thejohnhoffer/ipynb.git
pip install -e ipynb
```

# Usage

## Importing

On an IPython shell,
For an example.ipynb:

```

import nbook
from example import *

```

## Interaction

After an `import *`, you will be prompted like so:

```

In [1]: print('this is an example')
print('The first cell has these two lines')

Say y/n to running: 

```

As you hit `y`, prompts will continue for each cell.

When you hit `n`, the last cell prompted will load as multiline input.

If you hit `n` at `In [2]` for a file of 8 code cells, you will see:

```
Say y/n to running: n                               
You can load lines 1-8                            
                                                    
In [8]: # %load 2                                   
      : DATA = 'this is the second code cell'
      :                                             
```

You can edit the input and execute (this will not affect the original file).

If you then run `%load 3`, the third cell will load as muliline input.

Or, you can run `%load 3-8` to load the rest of the ipynb code at once.
