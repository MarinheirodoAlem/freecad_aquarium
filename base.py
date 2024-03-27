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
from utils import make_panel
from holes import getHole

def make_leveling_base(doc):
    grp = doc.addObject('App::DocumentObjectGroup', 'LevelingBase')
    grp.Label = 'LevelingBase'
    b = make_panel(doc, grp, 'BottomBase', 'Computed.LeftCornerX', '-Computed.Length/2', 'Computed.UnderGlassBaseLevel', 'Computed.Width', 'Computed.Length', 'Config.UnderGlassLevelingBaseThickness')
    base = doc.addObject("Part::Cut", "BaseDrilled")
    base.Base = b
    base.Tool = getHole(doc, 'Base')
    grp.removeObject(b)
    grp.addObject(base)
    base.ViewObject.ShapeColor = (1 / 3, 1 / 3, 0.0)
    sb = make_panel(doc, grp, 'BottomBaseSump', 'Computed.LeftCornerX+Config.MetalProfileHeight', '-Computed.Length/2+Config.MetalProfileHeight', 'Computed.UnderBaseLevelSump', 'Computed.Width-2*Config.MetalProfileHeight', 'Computed.Length-2*Config.MetalProfileHeight', 'Config.UnderGlassLevelingBaseThickness')
    grp.addObject(sb)
    return grp
