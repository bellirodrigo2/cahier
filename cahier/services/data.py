""""""

from enum import Enum

###############################################################################

class DataEndPoints(Enum):
    
    Interpolated= 'interpolated'
    Recorded = 'recorded'
    Plot = 'plot'
    Summary = 'summary'
    Value = 'value'
    EndValue = 'endvalue'
    
# OPTIONS
# startTime
# endTime
#interval
#filterexpression ????? para casos simples talvez... mais complexos fazer view