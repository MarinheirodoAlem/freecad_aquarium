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

from math import pi, sqrt
from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part, Arch, ArchCommands, Draft
import FreeCAD as App


def measure(doc, page, type, name, proj, *geoms):
    # page.recompute()
    m = doc.addObject('TechDraw::DrawViewDimension', name)
    m.Type = type
    m.MeasureType = 'Projected'
    m.References2D = [(proj, (geoms))]
    # print(geoms)
    page.addView(m)
    return m


def add_tech_draw(doc, name, HardHidden, *objs):
    print(f"add_tech_draw: {objs}")
    page = doc.addObject('TechDraw::DrawPage', f'{name}BluePrint')
    tpl = doc.addObject('TechDraw::DrawSVGTemplate', f'{name}Template')
    tpl.Template = App.getResourceDir() + '/Mod/TechDraw/Templates/A4_Landscape_blank.svg'
    page.Template = tpl
    page.Visibility = False
    page.Visibility = True
    group = doc.addObject("TechDraw::DrawProjGroup", f'{name}Projection')
    page.addView(group)
    source_grp = []
    for o in objs:
        obj = doc.getObject(o)
        source_grp.append(obj)
    group.Source = source_grp
    group.ProjectionType = "First Angle"
    group.ScaleType = 'Custom'
    group.Scale = .05
    #group.ScaleType = 'Automatic'
    group.setExpression('X', f'{name}Template.Width/4*3')
    group.setExpression('Y', f'{name}Template.Height/4*3')
    front_view = group.addProjection("Front")
    front_view.Label = f"Front {name}"
    front_view.HardHidden = HardHidden
     # First projection will become the Anchor.
    group.Anchor.Direction = (0, -1, 0)
    group.Anchor.RotationVector = (1, 0, 0)
    top_view = group.addProjection("Top")
    top_view.Label = f"Top {name}"
    top_view.HardHidden = HardHidden
    right_view = group.addProjection("Right")
    right_view.Label = f"Right {name}"
    right_view.HardHidden = HardHidden
    ftr_view = group.addProjection("FrontTopRight")
    ftr_view.Label = f"Perspective {name}"
    ftr_view.HardHidden = HardHidden
    group.recompute()
    doc.recompute()
    # measure(doc,group, 'Angle', 'cut45', top_view, 'Edge9', 'Edge0')
    # measure(doc,page, 'DistanceY', 'sump_bottom_space', front_view, 'Edge8', 'Edge15')

def clear_log():
    from PySide import QtGui
    mw=Gui.getMainWindow()
    c=mw.findChild(QtGui.QPlainTextEdit, "Python console")
    c.clear()
    r=mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()

def draw_structure(doc):
    add_tech_draw(doc, 'Base', False, 'StandStructure')
def draw_base(doc):
    add_tech_draw(doc, 'LevelingBase', False, 'LevelingBase')
def draw_bottom_glass(doc):
    add_tech_draw(doc, 'GlassPanelBase', True, 'BottomGlassDrilled')
def draw_side_glass(doc):
    add_tech_draw(doc, 'GlassPanelsSides', True,'SidesGlass') # 'LeftGlass', 'RightGlass', 'BackGlass', 'FrontGlass')
def draw_braces_base(doc):
    add_tech_draw(doc, 'GlassEuroBraceWeirBase', True, 'GlassBracesWeirFrame')
def draw_braces_top(doc):
    add_tech_draw(doc, 'GlassEuroBraceSuperior', True, 'GlassBracesTop')
def draw_braces_bottom(doc):
    add_tech_draw(doc, 'GlassEuroBraceInferior', True, 'GlassBracesBottom')
