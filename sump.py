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
from utils import glass_color, make_panel
from holes import getHole


def sump_color(obj):
    obj.ViewObject.ShapeColor=(1.0, 1.0, 1.0)
    obj.ViewObject.Transparency=0
    return obj

def make_sump(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Sump')
    grp_bp = doc.addObject('App::DocumentObjectGroup','Bottom')
    grp.addObject(grp_bp)
    grp.Label = 'Sump'
    bg = make_panel(doc, None, 'BottomAcrylic','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight)','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)','Computed.SumpAcrylicLevel','Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpExtraSpaceForChiller','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)','Config.SumpAcrylicThickness')
    sump_color(bg)
    z_b = 'Computed.SumpAcrylicLevel+Config.SumpAcrylicThickness'
    grp_gs = doc.addObject('App::DocumentObjectGroup','SidesSump')
    grp.addObject(grp_gs)
    back = make_panel(doc, grp_gs, 'BackPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight)','+Computed.Length/2-(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)', z_b, 'Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(back)
    left = make_panel(doc, grp_gs, 'LeftPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.MetalProfileHeight)+Config.SumpExtraSpaceForChiller','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Config.SumpAcrylicThickness','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(left)
    right = make_panel(doc, grp_gs, 'RightPanel','Computed.RightCornerX-(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Config.SumpAcrylicThickness','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(right)
    front = make_panel(doc, grp_gs, 'FrontPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight+Config.SumpAcrylicThickness)','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    glass_color(front)
    return grp
