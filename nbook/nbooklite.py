import io
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

def load_nbook(path):

    print ("importing Jupyter notebook from %s" % path)
    shell = InteractiveShell.instance()

    # load the notebook object
    with io.open(path, 'r', encoding='utf-8') as f:
        nb = read(f, 4)

    for cell in nb.cells:
        if cell.cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(cell.source)

            # load the code in the module
            with open('tmp.py','w') as f:
                f.write(code)
            try:
                shell.magic('run tmp.py')
            except:
                print('woops')
                continue
