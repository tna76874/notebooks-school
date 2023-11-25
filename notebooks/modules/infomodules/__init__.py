import os
import glob
import time
from numpy import random
from num2words import num2words

current_dir = os.path.dirname(__file__)

module_files = glob.glob(os.path.join(current_dir, "*.py"))

for module_file in module_files:
    module_name = os.path.basename(module_file)[:-3] 
    __import__(f'infomodules.{module_name}', globals(), locals(), fromlist=["*"])
