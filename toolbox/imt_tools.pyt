import arcpy
import importlib

# Hacky dumb shit to get AGP to see updated code on reload. Before you ask: a reload in the catalog is not sufficient.
# Adapted from https://github.com/Wildsong/ArcGIS_Python_Template
# import _template
# importlib.reload(_template)
# from _template import _Template

import export_layouts
importlib.reload(export_layouts)
from export_layouts import ExportLayouts

import event_start
importlib.reload(event_start)
from event_start import EventStart

# Add tools here
tool_list = [
    #_Template
    ExportLayouts,
    EventStart
]

class Toolbox(object):
    def __init__(self):
        self.label = 'Incident Managent Toolbox'
        self.alias = 'IncidentManagentToolbox'
        self.tools = tool_list