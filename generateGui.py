#****************************************************************************
# *                                                                          *
# *   Aquarium                                                               *
# *   Copyright (c) 2023 LGPL                                                *
# *                                                                          *
# *   This program is free software; you can redistribute it and/or modify   *
# *   it under the terms of the GNU Lesser General Public License (LGPL)     *
# *   as published by the Free Software Foundation; either version 2 of      *
# *   the License, or (at your option) any later version.                    *
# *   for detail see the LICENCE text file.                                  *
# *                                                                          *
# *   This program is distributed in the hope that it will be useful,        *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
# *   GNU Library General Public License for more details.                   *
# *                                                                          *
# *   You should have received a copy of the GNU Library General Public      *
# *   License along with this program; if not, write to the Free Software    *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
# *   USA                                                                    *
# *                                                                          *
#****************************************************************************

import FreeCADGui
from PySide import QtCore
from PySide import QtGui
from FreeCAD import Units
import FreeCAD as App
from collections import namedtuple
from structure import makeStandStructure
from panelsdoors import make_stand_cover, make_canopy_cover
from canopy import make_canopy
from pipes import make_pipes, make_nozzles, make_flanges
from glass import make_glass
from base import make_leveling_base
from weir import create_weir
from config import GetConfiguration
import techdraw

class Generate:
    """Explanation of the command."""

    def __init__(self, name, caption, descr, objectGenerated = None):
        """Initialize variables for the command that must exist at all times."""
        self.app = QtGui.QApplication
        self.mw = FreeCADGui.getMainWindow()
        self.name = name
        self.caption = caption
        self.descr = descr
        self.objectGenerated = objectGenerated

    def GetResources(self):
        """Return a dictionary with data that will be used by the button or menu item."""
        # 'Pixmap': 'MyCommand.svg',
        return {
                'MenuText': QtCore.QT_TRANSLATE_NOOP(self.name, self.caption),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP(self.name, self.descr)
                }

    def UpdateDoc(self):
        doc = App.activeDocument()
        doc.recompute()
        try:
            FreeCADGui.activeDocument().activeView().viewIsometric()
            FreeCADGui.SendMsgToActiveView("ViewFit")
        except Exception:
            print("Unable to fit view")

    def Activated(self):
        """Run the following code when the command is activated (button press)."""
        if App.ActiveDocument.getObject('Config') is None:
            config = GetConfiguration(App.ActiveDocument)
            config.recompute()
        if isinstance(self.objectGenerated, tuple):
            if callable(self.objectGenerated[1]):
                nobj = self.objectGenerated[1](App.ActiveDocument)
        elif isinstance(self.objectGenerated, list):
            for o in self.objectGenerated:
                if isinstance(o, tuple) and callable(o[1]):
                    nobj = o[1](App.ActiveDocument)
        self.UpdateDoc()

    def MissingObject(self):
        if self.objectGenerated == None:
            return True
        elif isinstance(self.objectGenerated, list):
            for o in self.objectGenerated:
                if isinstance(o, tuple) and App.ActiveDocument.getObject(o[0]) == None:
                    return True
            return False
        elif isinstance(self.objectGenerated, tuple) and isinstance(self.objectGenerated[0], str):
            if App.ActiveDocument.getObject(self.objectGenerated[0]) == None:
                return True
        else:
            return True

    def IsActive(self):
        """Return True when the command should be active or False when it should be disabled (greyed)."""
        return App.ActiveDocument != None and self.MissingObject()

def RegisterCommands():

    objs = [
        ('StandStructure', makeStandStructure),
        ('StandPanels', make_stand_cover),
        ('LevelingBase', make_leveling_base),
        ('Glasses', make_glass),
        ('Weir', create_weir),
        ('Flanges', make_flanges),
        ('Pipes', make_pipes),
        ('ClosedLoop', make_nozzles),
        ('CanopyStructure', make_canopy),
        ('CanopyPanels',  make_canopy_cover),
        ]
    FreeCADGui.addCommand("GenerateAll",            Generate("GenerateAll",         "Everything",      "Generate everything",                     objs))
    FreeCADGui.addCommand("GenerateStructure",      Generate("GenerateStructure",   "Structure",       "Generate the Sump Structure",             objs[0]))
    FreeCADGui.addCommand("GenerateStructurePanels",Generate("GeneratePanels",      "Structure Panels","Generate Sump Panels and Doors",          objs[1]))
    FreeCADGui.addCommand("GenerateBase",           Generate("GenerateBase",        "Leveling Base",   "Generate the leveling base for the glass",objs[2]))
    FreeCADGui.addCommand("GenerateGlass",          Generate("GenerateGlass",       "Glass Panels",    "Generate Glass Panels",                   objs[3]))
    FreeCADGui.addCommand("GenerateWeir",           Generate("GenerateWeir",        "Weir",            "Generate the Weir",                       objs[4]))
    FreeCADGui.addCommand("GenerateFlanges",        Generate("GenerateFlanges",     "Flanges/Pipes",   "Generate Flanges and Pipes",              [objs[5],objs[6]]))
    FreeCADGui.addCommand("GenerateClosedLoop",     Generate("GenerateClosedLoop",  "ClosedLoop",      "Generate the ClosedLoop",                 objs[7]))
    FreeCADGui.addCommand("GenerateCanopy",         Generate("GenerateCanopy",      "Canopy",          "Generate the Canopy",                     objs[8]))
    FreeCADGui.addCommand("GenerateCanopyPanels",   Generate("GenerateCanopyPanels","Canopy Panels",   "Generate the Canopy Panels",              objs[9]))
    tech_draw = [
        ('BaseBluePrint',                   techdraw.draw_structure),
        ('LevelingBaseBluePrint',           techdraw.draw_base),
        ('GlassPanelBaseBluePrint',         techdraw.draw_bottom_glass),
        ('GlassPanelsSidesBluePrint',       techdraw.draw_side_glass),
        ('GlassEuroBraceWeirBaseBluePrint', techdraw.draw_braces_base),
        ('GlassEuroBraceSuperiorBluePrint', techdraw.draw_braces_top),
        ('GlassEuroBraceInferiorBluePrint', techdraw.draw_braces_bottom),
        ]
    FreeCADGui.addCommand("GenerateBaseBluePrint",                  Generate("GenerateBaseBluePrint",                  "BaseBluePrint",                  "Generate BaseBluePrint",                  tech_draw[0]))
    FreeCADGui.addCommand("GenerateLevelingBaseBluePrint",          Generate("GenerateLevelingBaseBluePrint",          "LevelingBaseBluePrint",          "Generate LevelingBaseBluePrint",          tech_draw[1]))
    FreeCADGui.addCommand("GenerateGlassPanelBaseBluePrint",        Generate("GenerateGlassPanelBaseBluePrint",        "GlassPanelBaseBluePrint",        "Generate GlassPanelBaseBluePrint",        tech_draw[2]))
    FreeCADGui.addCommand("GenerateGlassPanelsSidesBluePrint",      Generate("GenerateGlassPanelsSidesBluePrint",      "GlassPanelsSidesBluePrint",      "Generate GlassPanelsSidesBluePrint",      tech_draw[3]))
    FreeCADGui.addCommand("GenerateGlassEuroBraceWeirBaseBluePrint",Generate("GenerateGlassEuroBraceWeirBaseBluePrint","GlassEuroBraceWeirBaseBluePrint","Generate GlassEuroBraceWeirBaseBluePrint",tech_draw[4]))
    FreeCADGui.addCommand("GenerateGlassEuroBraceSuperiorBluePrint",Generate("GenerateGlassEuroBraceSuperiorBluePrint","GlassEuroBraceSuperiorBluePrint","Generate GlassEuroBraceSuperiorBluePrint",tech_draw[5]))
    FreeCADGui.addCommand("GenerateGlassEuroBraceInferiorBluePrint",Generate("GenerateGlassEuroBraceInferiorBluePrint","GlassEuroBraceInferiorBluePrint","Generate GlassEuroBraceInferiorBluePrint",tech_draw[6]))


def AllCommands():
    return [
        "GenerateAll",
        "GenerateStructure",
        "GenerateStructurePanels",
        "GenerateBase",
        "GenerateGlass",
        "GenerateWeir",
        "GenerateFlanges",
        "GenerateClosedLoop",
        "GenerateCanopy",
        "GenerateCanopyPanels",
    ]
def AllBluePrintCommands():
    return [
        "GenerateBaseBluePrint",                  
        "GenerateLevelingBaseBluePrint",                  
        "GenerateGlassPanelBaseBluePrint",        
        "GenerateGlassPanelsSidesBluePrint",      
        "GenerateGlassEuroBraceWeirBaseBluePrint",
        "GenerateGlassEuroBraceSuperiorBluePrint",
        "GenerateGlassEuroBraceInferiorBluePrint",
    ]
