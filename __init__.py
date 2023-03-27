from sys import path
from os.path import dirname as parent_directory
_CURRENTFILE: str = __file__
_CHIMERACAMPATH: str = parent_directory(_CURRENTFILE)
path.append(_CHIMERACAMPATH)