from dataclasses import dataclass

from ezdxf.document import Drawing
from ezdxf.layouts.layout import Modelspace
import units 
import ezdxf

MODEL_UNITS: dict[str, str]={
     "LENGTH": "mm",
     "MASS": "kg",
     "FORCE": "N"
     }

@dataclass 
class Beam: 
     width: float
     height: float

     def __post_init__(self): 
          return 0 
     
     def __convert_to_SI_units__(self) -> None: 
          self.width: float =      self.width * units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
          self.base: float =       self.width * units.INPUT_LENGTH_FACTOR[MODEL_UNITS["LENGTH"]]
     

     def to_dxf(self, name: str ):
          doc: Drawing = ezdxf.new()
          msp: Modelspace = doc.modelspace()
          msp.add_line(start=(0,0), end=(10,0), dxfattribs={
               "layer": "Concrete"
          })
          doc.saveas("new_name.dxf")