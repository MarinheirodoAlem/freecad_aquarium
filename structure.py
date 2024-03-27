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
from utils import make_supports


def makeStandStructure(doc, cut45 = True):
    grp = doc.addObject('App::DocumentObjectGroup', 'StandStructure')
    grp_sup = doc.addObject('App::DocumentObjectGroup', 'PanelSupports')
    grp.addObject(grp_sup)
    w = grp.evalExpression('Config.MetalProfileWidth')
    h = grp.evalExpression('Config.MetalProfileHeight')
    t = grp.evalExpression('Config.MetalProfileWallThickness')
    profile = Arch.makeProfile([0, 'RHS', 'MetalProfile', 'RH', w, h, t])
    profile.setExpression('Width', 'Config.MetalProfileWidth')
    profile.setExpression('Height', 'Config.MetalProfileHeight')
    profile.setExpression('Thickness', 'Config.MetalProfileWallThickness')
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, 0))
    if cut45:
        s.setExpression('Height', 'Computed.BeamsSizeWidth45')
        s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
        cut = App.ActiveDocument.addObject("Part::Box", "CutTool")
        cut.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
        cut.setExpression('.Placement.Base.y', 'Computed.FrontCornerY')
        cut.setExpression('.Placement.Base.z', 'Computed.BeamsLevel-Config.MetalProfileWidth/2')
        cut.setExpression('Width', 'Config.MetalProfileWidth')
        cut.setExpression('Length', 'Computed.BeamsSizeWidth45/sqrt(2)')
        cut.setExpression('Height', 'Computed.BeamsSizeWidth45/sqrt(2)')
        cut.Placement.Rotation = Rotation(45, 0, 90)
        s_cut = App.ActiveDocument.addObject("Part::MultiCommon", "beam45cut")
        s_cut.Shapes = [s, cut]
        grp.addObject(s_cut)
    else:
        s.setExpression('Height', 'Computed.BeamsSizeWidth')
        s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileWidth/2')
        grp.addObject(s)
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.BeamsLevel')
    s.IfcType = "Beam"
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, 0))
    if cut45:
        s.setExpression('Height', 'Computed.BeamsSizeWidth45')
        s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
        cut = App.ActiveDocument.addObject("Part::Box", "CutTool")
        cut.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
        cut.setExpression('.Placement.Base.y', 'Computed.BackCornerY')
        cut.setExpression('.Placement.Base.z', 'Computed.BeamsLevel-Config.MetalProfileWidth/2')
        cut.setExpression('Width', 'Config.MetalProfileWidth')
        cut.setExpression('Length', 'Computed.BeamsSizeWidth45/sqrt(2)')
        cut.setExpression('Height', 'Computed.BeamsSizeWidth45/sqrt(2)')
        cut.Placement.Rotation = Rotation(45, 0, 90)
        s_cut = App.ActiveDocument.addObject("Part::MultiCommon", "beam45cut")
        s_cut.Shapes = [s, cut]
        grp.addObject(s_cut)
    else:
        s.setExpression('Height', 'Computed.BeamsSizeWidth')
        s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileWidth/2')
        grp.addObject(s)
    s.setExpression('.Placement.Base.y', 'Computed.BackCornerY-Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.BeamsLevel')
    s.IfcType = "Beam"
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, -90))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY')
    s.setExpression('.Placement.Base.z', 'Computed.BeamsLevel')
    s.setExpression('Height', 'Computed.BeamsSizeLength')
    if cut45:
        cut = App.ActiveDocument.addObject("Part::Box", "CutTool")
        cut.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
        cut.setExpression('.Placement.Base.y', 'Computed.BackCornerY')
        cut.setExpression('.Placement.Base.z', 'Computed.BeamsLevel-Config.MetalProfileWidth/2')
        cut.setExpression('Width', 'Config.MetalProfileWidth')
        cut.setExpression('Length', 'Computed.BeamsSizeLength/sqrt(2)')
        cut.setExpression('Height', 'Computed.BeamsSizeLength/sqrt(2)')
        cut.Placement.Rotation = Rotation(-45, 0, 90)
        s_cut = App.ActiveDocument.addObject("Part::MultiCommon", "beam45cut")
        s_cut.Shapes = [s, cut]
        grp.addObject(s_cut)
    else:
        grp.addObject(s)
    s.IfcType = "Beam"
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, -90))
    s.setExpression('.Placement.Base.x', 'Computed.RightCornerX-Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY')
    s.setExpression('.Placement.Base.z', 'Computed.BeamsLevel')
    s.setExpression('Height', 'Computed.BeamsSizeLength')
    if cut45:
        cut = App.ActiveDocument.addObject("Part::Box", "CutTool")
        cut.setExpression('.Placement.Base.x', 'Computed.RightCornerX')
        cut.setExpression('.Placement.Base.y', 'Computed.BackCornerY')
        cut.setExpression('.Placement.Base.z', 'Computed.BeamsLevel-Config.MetalProfileWidth/2')
        cut.setExpression('Width', 'Config.MetalProfileWidth')
        cut.setExpression('Length', 'Computed.BeamsSizeLength/sqrt(2)')
        cut.setExpression('Height', 'Computed.BeamsSizeLength/sqrt(2)')
        cut.Placement.Rotation = Rotation(-45, 0, 90)
        s_cut = App.ActiveDocument.addObject("Part::MultiCommon", "beam45cut")
        s_cut.Shapes = [s, cut]
        grp.addObject(s_cut)
    else:
        grp.addObject(s)
    s.IfcType = "Beam"

    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 0, 0), Rotation(0, 0, 0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileWidth/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.MetalProfileHeight/2')
    s.setExpression('Height', 'Computed.ColumnsSizeHeight')
    s.IfcType = "Column"
    sb = Draft.make_ortho_array(s, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=2, n_y=2, n_z=1, use_link=False)
    sb.setExpression('.IntervalX.x', '(Computed.Width-Config.MetalProfileWidth)/(Config.ColumnsStandWidthCount+1)')
    sb.setExpression('.IntervalY.y', 'Computed.Length-Config.MetalProfileHeight')
    sb.setExpression('NumberX', 'Config.ColumnsStandWidthCount + 2')
    sb.ViewObject.ShapeColor = s.ViewObject.ShapeColor
    grp.addObject(sb)
    # Fasteners
    make_supports(doc, False, grp_sup, 'Fastener')
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, 0))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileWidth')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.z', 'Computed.SumpBeamsLevel')
    s.setExpression('Height', 'Computed.BeamsSumpSizeWidth')
    s.IfcType = "Beam"
    sb = Draft.make_ortho_array(s, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=2, n_y=2, n_z=1, use_link=False)
    sb.setExpression('.IntervalX.x', '(Computed.Width-Config.MetalProfileWidth)/(Config.ColumnsStandWidthCount+1)')
    sb.setExpression('.IntervalY.y', 'Computed.Length-Config.MetalProfileHeight')
    sb.setExpression('NumberX', 'Config.ColumnsStandWidthCount + 1')
    sb.ViewObject.ShapeColor = s.ViewObject.ShapeColor
    grp.addObject(sb)
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, -90))
    s.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.MetalProfileHeight')
    s.setExpression('.Placement.Base.z', 'Computed.SumpBeamsLevel')
    s.setExpression('Height', 'Computed.BeamsSumpSizeLength')
    s.IfcType = "Beam"
    grp.addObject(s)
    s = Arch.makeStructure(profile, height=1)
    s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, -90))
    s.setExpression('.Placement.Base.x', 'Computed.RightCornerX-Config.MetalProfileHeight/2')
    s.setExpression('.Placement.Base.y', 'Computed.FrontCornerY+Config.MetalProfileHeight')
    s.setExpression('.Placement.Base.z', 'Computed.SumpBeamsLevel')
    s.setExpression('Height', 'Computed.BeamsSumpSizeLength')
    s.IfcType = "Beam"
    grp.addObject(s)
    def make_beam_support(name, posZ):
        s = Arch.makeStructure(profile, height=1, name=name)
        s.Placement = Placement(Vector(0, 1, 0), Rotation(0, 90, 0))
        s.setExpression('.Placement.Base.x','Computed.LeftCornerX+(Computed.BeamsDir>0?Config.MetalProfileHeight:Computed.StandBeamSpacing+Config.MetalProfileHeight/2)')
        s.setExpression('.Placement.Base.y','Computed.FrontCornerY+(Computed.BeamsDir>0?Computed.StandBeamSpacing+Config.MetalProfileHeight/2:Config.MetalProfileHeight)')
        s.setExpression('.Placement.Base.z', posZ)
        s.setExpression('.Placement.Rotation.Yaw', '(Computed.BeamsDir>0?0:90)')
        s.setExpression('.Placement.Rotation.Pitch', '90')
        s.setExpression('.Placement.Rotation.Roll', '0')
        s.setExpression('Height', 'Computed.BeamsSizeMiddle')
        s.IfcType = "Beam"
        sb = Draft.make_ortho_array(s, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
        sb.setExpression('.IntervalX.x', 'Computed.BeamsDir>0?0:Computed.StandBeamSpacing')
        sb.setExpression('.IntervalY.y', 'Computed.BeamsDir>0?Computed.StandBeamSpacing:0')
        sb.setExpression('NumberX', 'Computed.BeamsDir>0?1:Config.BeamsStandCount')
        sb.setExpression('NumberY', 'Computed.BeamsDir>0?Config.BeamsStandCount:1')
        sb.ViewObject.ShapeColor = s.ViewObject.ShapeColor
        grp.addObject(sb)
    make_beam_support('BaseReinforcement', 'Computed.BeamsLevel')
    make_beam_support('SumpReinforcement', 'Computed.SumpBeamsLevel')
    return grp
