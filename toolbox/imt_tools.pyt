import arcpy
import importlib

# TODO: do we still need todo this with the debug/test pattern?
# Hacky dumb shit to get AGP to see updated code on reload. Before you ask: a reload in the catalog is not sufficient.
# Adapted from https://github.com/Wildsong/ArcGIS_Python_Template
# import _template
# importlib.reload(_template)
# from _template import _Template

import export_layouts
importlib.reload(export_layouts)
from export_layouts import ExportLayouts

import cv_update
importlib.reload(cv_update)
from cv_update import CVUpdate

# import update_domains
# importlib.reload(update_domains)
# from update_domains import UpdateDomains

# Add tools here
tool_list = [
    #_Template
    ExportLayouts,
    CVUpdate
]

class Toolbox(object):
    def __init__(self):
        self.label = 'Incident Managent Toolbox'
        self.alias = 'IncidentManagentToolbox'
        self.tools = tool_list