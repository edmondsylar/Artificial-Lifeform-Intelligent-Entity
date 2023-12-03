# we are going to handle the configuration the later from here.
from layerdb import DatabaseManager
import pathlib

# get coredb file path located in the parent directory
db_file_path = pathlib.Path(__file__).parent.absolute().parent.absolute() / 'bus.db'

# get layer Db 
layerdb = "aspirationalLayer.db"

