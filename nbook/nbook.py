"""
Module directly collated from
http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Importing%20Notebooks.html
"""
import io, os, sys, types
from nbformat import read
from pygments import highlight
from IPython import get_ipython
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from IPython.core.interactiveshell import InteractiveShell

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path

class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        #self.shell = InteractiveShell.instance()
        self.shell = get_ipython()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print ("importing Jupyter notebook from %s" % path)

        formatter = TerminalFormatter()
        lexer = PythonLexer()

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            broken = False
            hsm = self.shell.history_manager
            hsm.reset(new_session=True)
            self.shell.execution_count = 0
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(cell.source)

                    if broken:
                        # save the code to history, but don't run it
                        hsm.store_inputs(self.shell.execution_count, code)
                        self.shell.execution_count += 1
                        continue

                    # ask to execute the code
                    runcount = self.shell.execution_count
                    hcode = highlight(code,lexer,formatter)
                    preface = '\nIn ['+str(runcount+1)+']: '
                    more = self.shell.ask_yes_no(preface+hcode+'\nSay y/n to running:')
                    if more:
                        # run the code in the module
                        self.shell.run_cell(code, store_history=True)
                    else:
                        # open the code in the module
                        preface = '# %load '+str(runcount+1)+'\n'
                        self.shell.set_next_input(preface+code)
                        hsm.store_inputs(runcount, code)
                        self.shell.execution_count += 1
                        broken = True
            print('You can load lines 1-'+str(self.shell.execution_count))
        finally:
            self.shell.user_ns = save_user_ns
        return mod

class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]

