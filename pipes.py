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
from holes import getHole

def set_XYZ(obj, x=None, y=None, z=None):
    if isinstance(x, str):
        obj.setExpression('.Placement.Base.x', x)
    elif isinstance(x, int):
        index = x
        obj.setExpression('.Placement.Base.x', f'Computed.StartPipes+{index}*Computed.WeirFlangeOffset')
    if isinstance(y, str):
        obj.setExpression('.Placement.Base.y', y)
    else:
        obj.setExpression('.Placement.Base.y', 'Computed.FlangesY')
    if isinstance(z, str):
        obj.setExpression('.Placement.Base.z', z)


def drill(doc, type, hole):
    getHole(doc, type).Group = [hole] + getHole(doc, type).Group

def extend_hole(hole):
    hole.setExpression('.Placement.Base.z', '0')
    hole.setExpression('Height', 'Computed.RealGlassHeight+Config.StandVisibleHeight')
    return hole


def make_flange(doc, grp, type, index=None, x=None, y=None):
    if index==None:
        index = int(doc.Computed.get('FlangeCount'))
        doc.Computed.set('FlangeCount', str(index+1))
        doc.Computed.recompute()
    if x==None:
        x=index
    red_glass = (0.67, 0.00, 0.00, 0.61)

    def make_tail():
        FlangeTail = doc.addObject('Part::Cylinder', f'Flange{type}Tail_{index}')
        set_XYZ(FlangeTail, x=x, y=y, z=f'-ConfigPipes{type}.FlangeFreeHeightBottom - Computed.FlangesNeckHeight')
        FlangeTail.setExpression('Height', f'ConfigPipes{type}.FlangeFreeHeightBottom')
        FlangeTail.setExpression('Radius', f'ConfigPipes{type}.FlangeFreeDiameterBottom / 2')
        FlangeTail.ViewObject.ShapeColor = red_glass
        FlangeTail.ViewObject.Transparency=90
        return FlangeTail
    FlangeTail = make_tail()
    FlangeHead = doc.addObject('Part::Cylinder', f'Flange{type}Head_{index}')
    set_XYZ(FlangeHead, x=x, y=y)
    FlangeHead.setExpression('Height', f'ConfigPipes{type}.FlangeFreeHeightTop')
    FlangeHead.setExpression('Radius', f'ConfigPipes{type}.FlangeFreeDiameterTop / 2')
    FlangeHead.ViewObject.ShapeColor = red_glass
    FlangeHead.ViewObject.Transparency=90
    def make_neck():
        FlangeNeck = doc.addObject('Part::Cylinder', f'Flange{type}Neck_{index}')
        set_XYZ(FlangeNeck, x=x, y=y, z='-Height')
        FlangeNeck.setExpression('Height', 'Computed.FlangesNeckHeight')
        FlangeNeck.setExpression('Radius', f'ConfigPipes{type}.FlangeDiameter / 2')
        FlangeNeck.Placement = Placement(Vector(0.00, 0.00, -14.00), Rotation (0.0, 0.0, 0.0, 1.0))
        return FlangeNeck
    FlangeNeck = make_neck();
    flange = doc.addObject('App::Part', f'Flange{type}_{index}')
    flange.Group = [FlangeNeck, FlangeHead, FlangeTail]
    if grp:
        grp.addObject(flange)
    flange.setExpression('.Placement.Base.z', 'Computed.FlangesZ')
    hole_glass = extend_hole(make_neck())
    hole_base = extend_hole(make_tail())
    drill(doc, 'Glass', hole_glass)
    drill(doc, 'Base', hole_base)
    return (flange, hole_glass, hole_base)


def make_flanges(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Flanges')
    grp.Visibility = False
    make_flange(doc,grp,'Return')
    make_flange(doc,grp,'Drain')
    make_flange(doc,grp,'Drain')
    make_flange(doc,grp,'Drain')
    make_flange(doc,grp,'Drain')
    make_flange(doc,grp,'Return')
    return grp

def make_pipe(doc, index, type, level, grp):
    name = f'PipesWeir{type}_{index}'
    o = doc.getObject(name)
    if o == None:
        o = doc.addObject('App::Part', name)
        o.setExpression('.Placement.Base.z', 'Computed.FlangesZ')
        grp.addObject(o)
    pipeBase = f'ConfigPipes{type}.FlangeFreeHeightTop-ConfigPipes{type}.FlangePipeLengthInside'
    pipeLength = f'Config.{level}+Computed.WaterLevelDeepest-({pipeBase}+Computed.FlangesZ)'
    p = Arch.makePipe()
    p.setExpression('Length',pipeLength)
    p.setExpression('Diameter',f'ConfigPipes{type}.PipeDiameter')
    set_XYZ(p, index)
    p.setExpression('.Placement.Base.z', pipeBase)
    o.Group = [ p ] + o.Group

def make_pipes(doc):
    g = doc.addObject('App::DocumentObjectGroup','Pipes')
    make_pipe(doc,0,'Return','ReturnWaterLevel', g)
    make_pipe(doc,1,'Drain','BeanAnimalMainDrainLevel',g)
    make_pipe(doc,2,'Drain','BeanAnimalEmergencyDrainLevel',g)
    make_pipe(doc,3,'Drain','BeanAnimalEmergencyDrainLevel',g)
    make_pipe(doc,4,'Drain','BeanAnimalAuxiliaryDrainLevel',g)
    make_pipe(doc,5,'Return','ReturnWaterLevel', g)
    return g

def make_nozzles(doc):
    grp = doc.addObject('App::DocumentObjectGroup','ClosedLoop')
    (nozzle, hole_glass, hole_base) = make_flange(doc,None,'NozzleClosedLoop', index=1, x=f'Computed.NozzlesBaseX', y=f'Computed.NozzlesBaseY')
    def create_array(doc, obj):
        sb = Draft.make_ortho_array(obj, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=2, n_y=2, n_z=1, use_link=False)
        sb.setExpression('.IntervalY.y', 'Computed.NozzlesSpacingY')
        sb.setExpression('.IntervalX.x', 'Computed.NozzlesSpacingX')
        sb.setExpression('NumberY', 'Computed.NozzlesNumberY')
        sb.setExpression('NumberX', 'Computed.NozzlesNumberX')
        #sb.ViewObject.ShapeColor = n.ViewObject.ShapeColor
        return sb
    sb = create_array(doc, nozzle)
    grp.addObject(sb)
    holes_glass = create_array(doc, hole_glass)
    drill(doc, 'Glass', holes_glass)
    holes_base = create_array(doc, hole_base)
    drill(doc, 'Base', holes_base)
    return grp

def make_water(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Water')
    waterMain = doc.addObject('Part::Box', 'WaterDisplayExtra')
    waterMain.setExpression('Length', 'Computed.Width - 2 * Config.SidesGlassThickness')
    waterMain.setExpression('Width', 'Computed.Length - 2 * Config.SidesGlassThickness')
    waterMain.setExpression('Height', 'Config.WaterHeightWeir')
    waterMain.setExpression('.Placement.Base.x', 'Computed.LeftCornerX + Config.SidesGlassThickness')
    waterMain.setExpression('.Placement.Base.y', 'Computed.Length / -2 + Config.SidesGlassThickness')
    waterMain.setExpression('.Placement.Base.z', 'Computed.GlassLevel + Config.BottomGlassThickness')
    waterWeirCut = doc.addObject('Part::Box', 'waterWeirCut')
    waterWeirCut.setExpression('Length', 'Computed.Width - 2 * Config.BraceWidth - 2 * Config.SidesGlassThickness')
    waterWeirCut.setExpression('Width', 'Computed.WeirDepth')
    waterWeirCut.setExpression('Height', 'Computed.RealGlassHeight + Config.StandVisibleHeight')
    waterWeirCut.setExpression('.Placement.Base.x', 'Computed.LeftCornerX + Config.SidesGlassThickness + Config.BraceWidth')
    waterWeirCut.setExpression('.Placement.Base.y', 'Computed.Length / 2 - Config.SidesGlassThickness - Computed.WeirDepth')
    waterMain.ViewObject.Transparency=80
    waterMain.ViewObject.ShapeColor=(2.0/3.0, 1.0, 1.0, 1.0)
    waterWeirCut.ViewObject.ShapeColor=(2.0/3.0, 1.0, 1.0, 1.0)
    waterWeirCut.ViewObject.Transparency=100
    water = doc.addObject("Part::Cut", 'WaterDisplay')
    water.Base = waterMain
    water.Tool = waterWeirCut
    grp.addObject(water)
    def make_level(doc, name, color, base, top):
        water = doc.addObject('Part::Box', f'Water{name}')
        water.setExpression('Length', 'Computed.Width - 2 * Config.BraceWidth - 2 * Config.SidesGlassThickness')
        water.setExpression('Width', 'Computed.WeirDepth')
        water.setExpression('Height', f'({top})-({base})')
        water.setExpression('.Placement.Base.x', 'Computed.LeftCornerX + Config.SidesGlassThickness + Config.BraceWidth')
        water.setExpression('.Placement.Base.y', 'Computed.Length / 2 - Config.SidesGlassThickness - Computed.WeirDepth')
        water.setExpression('.Placement.Base.z', f'Computed.GlassLevel + Config.BottomGlassThickness+{base}')
        water.ViewObject.Transparency=80
        water.ViewObject.ShapeColor=color
        grp.addObject(water)
    make_level(doc, "BeanAnimalMainDrainLevel", (0.0, 1.0, 0.0, 1.0), 0, 'Config.BeanAnimalMainDrainLevel')
    make_level(doc, "BeanAnimalAuxiliaryDrainLevel", (1.0, 1.0, 0.0, 1.0), 'Config.BeanAnimalMainDrainLevel', 'Config.BeanAnimalAuxiliaryDrainLevel')
    make_level(doc, "BeanAnimalEmergencyDrainLevel", (1.0, 0.0, 0.0, 1.0), 'Config.BeanAnimalAuxiliaryDrainLevel', 'Config.BeanAnimalEmergencyDrainLevel')
