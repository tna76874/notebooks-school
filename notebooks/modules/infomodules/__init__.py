import os
import glob

current_dir = os.path.dirname(__file__)

module_files = glob.glob(os.path.join(current_dir, "*.py"))

for module_file in module_files:
    module_name = os.path.basename(module_file)[:-3]  # Entferne die ".py"-Endung
    __import__(f'infomodules.{module_name}', globals(), locals(), fromlist=["*"])
