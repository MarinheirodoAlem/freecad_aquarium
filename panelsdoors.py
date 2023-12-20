#****************************************************************************
#*                                                                          *
#*   Aquarium                                                               *
#*   Copyright (c) 2023 LGPL                                                *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*   USA                                                                    *
#*                                                                          *
#****************************************************************************

from math import pi, sqrt
from FreeCAD import Vector, Placement, Rotation
import Sketcher
import Part, Arch, ArchCommands, Draft
import FreeCAD as App
from utils import make_supports

def panel_color(obj):
    obj.ViewObject.ShapeColor=(0.1, 0.1, 0.1)
    return obj

def mkpc(doc, grp, name, px, py, pz, l, w, h):
    g = doc.addObject('Part::Box', name)
    g.setExpression('.Placement.Base.x', px)
    g.setExpression('.Placement.Base.y', py)
    g.setExpression('.Placement.Base.z', pz)
    g.setExpression('Length', l)
    g.setExpression('Width', w)
    g.setExpression('Height', h)
    panel_color(g)
    if grp:
        grp.addObject(g)
    return g

def make_stand_cover(doc):
    z_b = 'Config.Panel2FloorSpace'
    h = f'Config.StandVisibleHeight-{z_b}'
    g = doc.addObject('App::DocumentObjectGroup','StandPanels')
    mkpc(doc,g,'LeftStandCover','Computed.LeftCornerX-Config.PanelThickness','Computed.FrontCornerY', z_b, 'Config.PanelThickness','Config.Length+Config.PanelThickness',h)
    mkpc(doc,g,'RightStandCover','Computed.RightCornerX','Computed.FrontCornerY', z_b, 'Config.PanelThickness','Config.Length+Config.PanelThickness',h)
    mkpc(doc,g,'BackStandCover','Computed.LeftCornerX','Computed.BackCornerY', z_b, 'Config.Width','Config.PanelThickness',h)
    mkpc(doc,g,'FrontStandCover','Computed.LeftCornerX-Config.PanelThickness','Computed.FrontCornerY-Config.PanelThickness', z_b, 'Config.Width+2*Config.PanelThickness','Config.PanelThickness',h)
    make_supports(doc, True, g, 'ScrewBlock')
    return g

def make_canopy_cover(doc):
    z_b = 'Computed.CanopyPanelLevel'
    h = 'Computed.CanopyPanelHeight'
    g = doc.addObject('App::DocumentObjectGroup','CanopyPanels')
    mkpc(doc,g,'LeftCanopyCover','Computed.LeftCornerX-Config.PanelThickness','Computed.FrontCornerY', z_b, 'Config.PanelThickness','Config.Length+Config.PanelThickness',h)
    mkpc(doc,g,'RightCanopyCover','Computed.RightCornerX','Computed.FrontCornerY', z_b, 'Config.PanelThickness','Config.Length+Config.PanelThickness',h)
    mkpc(doc,g,'BackCanopyCover','Computed.LeftCornerX','Computed.BackCornerY', z_b, 'Config.Width','Config.PanelThickness',h)
    mkpc(doc,g,'FrontCanopyCover','Computed.LeftCornerX-Config.PanelThickness','Computed.FrontCornerY-Config.PanelThickness', z_b, 'Config.Width+2*Config.PanelThickness','Config.PanelThickness',h)
    return g
