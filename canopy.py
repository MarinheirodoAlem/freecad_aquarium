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

def make_canopy(doc):
    grp = doc.addObject('App::DocumentObjectGroup','CanopyStructure')
    w = grp.evalExpression('Config.CanopyProfileWidth')
    h = grp.evalExpression('Config.CanopyProfileHeight')
    profile = Arch.makeProfile([0, 'REC', 'CanopyProfile', 'R', w, h])
    profile.setExpression('Width', 'Config.CanopyProfileWidth')
    profile.setExpression('Height', 'Config.CanopyProfileHeight')
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,1,0),Rotation(0,90,0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.CanopyProfileWidth')
    s.setExpression('.Placement.Base.y', 'Computed.BackCornerY-Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyBeamsLevel')
    s.setExpression('Height', 'Computed.BeamCanopyLeft2RightLength')
    s.IfcType = "Beam"
    grp.addObject(s)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,1,0),Rotation(0,90,0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.CanopyProfileWidth')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyBeamsLevel')
    s.setExpression('Height', 'Computed.BeamCanopyLeft2RightLength')
    s.IfcType = "Beam"
    grp.addObject(s)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,1,0),Rotation(90,-90,0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.y', 'Computed.BackCornerY-Config.CanopyProfileHeight')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyBeamsLevel')
    s.setExpression('Height', 'Computed.BeamCanopyFront2BackLength')
    s.IfcType = "Beam"
    sb = Draft.make_ortho_array(s, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=1, n_z=1, use_link=False)
    sb.setExpression('.IntervalX.x', 'Computed.CanopySpacingX')
    sb.setExpression('NumberX', 'Computed.CanopyBeamsX')
    grp.addObject(sb)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,0,1),Rotation(0,0,0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.CanopyProfileWidth/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyLevel')
    s.setExpression('Height', 'Computed.CanopyColumnHeight')
    s.IfcType = "Column"
    grp.addObject(s)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,0,1),Rotation(0,0,0))
    s.setExpression('.Placement.Base.x', 'Computed.RightCornerX-Config.CanopyProfileWidth/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyLevel')
    s.setExpression('Height', 'Computed.CanopyColumnHeight')
    s.IfcType = "Column"
    grp.addObject(s)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,0,1),Rotation(0,0,0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.CanopyProfileWidth/2')
    s.setExpression('.Placement.Base.y', 'Computed.BackCornerY-Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyLevel')
    s.setExpression('Height', 'Computed.CanopyColumnHeight')
    s.IfcType = "Column"
    grp.addObject(s)
    s = Arch.makeStructure(profile,height=1)
    s.Placement = Placement(Vector(0,0,1),Rotation(0,0,0))
    s.setExpression('.Placement.Base.x', 'Computed.RightCornerX-Config.CanopyProfileWidth/2')
    s.setExpression('.Placement.Base.y', 'Computed.BackCornerY-Config.CanopyProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.CanopyLevel')
    s.setExpression('Height', 'Computed.CanopyColumnHeight')
    s.IfcType = "Column"
    grp.addObject(s)
    return grp


