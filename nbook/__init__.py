import sys
import nbook
import nbooklite

load = nbooklite.load_nbook
sys.meta_path.append(nbook.NotebookFinder())
