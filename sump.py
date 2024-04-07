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

def LastConstrainExp(obj, exp):
    n = len(obj.Constraints)-1
    print(str(obj.Constraints))
    print(f'SET Constraints[{n}] => {exp}')
    obj.setExpression(f'Constraints[{n}]', exp)

def sump_color(obj):
    obj.ViewObject.ShapeColor=(1.0, 1.0, 1.0)
    obj.ViewObject.Transparency=0
    return obj

def make_sump(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Sump')
    grp_bp = doc.addObject('App::DocumentObjectGroup','Bottom')
    grp.addObject(grp_bp)
    grp.Label = 'Sump'
    bg = make_panel(doc, grp_bp, 'BottomAcrylic','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight)','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)','Computed.SumpAcrylicLevel','Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpExtraSpaceForChiller','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)','Config.SumpAcrylicThickness')
    sump_color(bg)
    z_b = 'Computed.SumpAcrylicLevel+Config.SumpAcrylicThickness'
    grp_gs = doc.addObject('App::DocumentObjectGroup','SidesSump')
    grp.addObject(grp_gs)
    back = make_panel(doc, grp_gs, 'BackPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight)','+Computed.Length/2-(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)', z_b, 'Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(back)
    left = make_panel(doc, grp_gs, 'LeftPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.MetalProfileHeight)+Config.SumpExtraSpaceForChiller','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Config.SumpAcrylicThickness','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(left)
    placemnt = Placement(Vector(0, 0, 0), Rotation (90, 0, 90))
    right = make_panel(doc, grp_gs, 'RightPanel','Computed.RightCornerX-(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Config.SumpAcrylicThickness','Computed.Length-2*(Config.SumpExtraMargin+Config.MetalProfileHeight)-Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    sump_color(right)
    front = make_panel(doc, grp_gs, 'FrontPanel','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight+Config.SumpAcrylicThickness)','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    glass_color(front)
    fuge_spliter = make_panel(doc, grp_gs, 'RefugiumsSplitter','Computed.LeftCornerX+(Config.SumpExtraMargin+Config.SumpExtraSpaceForChiller+Config.MetalProfileHeight+Config.SumpAcrylicThickness)','-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight)', z_b, 'Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment-Config.SumpAcrylicThickness','Config.SumpAcrylicThickness','Config.SumpHeight-Config.SumpAcrylicThickness')
    fuge_spliters = Draft.make_ortho_array(fuge_spliter, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuge_spliters.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuge_spliters.setExpression('NumberY', 'Config.FugeCompartments')
    glass_color(fuge_spliters)
    fuge = doc.addObject('PartDesign::Body', 'RefugiumsWeir')
    fuge.Group = []
    fuge_wall_weir = doc.addObject('Sketcher::SketchObject', 'fuge_wall_weir')
    b = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (100.0, 0.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, -1, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', b))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, b, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Computed.SumpCompartmentLength')
    r = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (100.0, 0.0, 0.0), Vector (100.0, 50.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', r))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, r, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Config.SumpHeight-Config.SumpAcrylicThickness')
    l = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (0.0, 50.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', l))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, l, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', b, 2, r, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, r, 2))
    w1 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (0.0, 2.0, 0.0), Vector (1.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', w1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, w1, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Config.FugeBorder')
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', l, 2, w1, 1))
    w2 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (1.0, 2.0, 0.0), Vector (1.0, 1.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', w2))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w1, 2, w2, 1))
    w3 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (1.0, 1.0, 0.0), Vector (2.0, 1.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', w3))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w2, 2, w3, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, w3, 1, 1.0))
    LastConstrainExp(fuge_wall_weir, '(Config.SumpHeight-Config.SumpAcrylicThickness)/2+Config.FugeBorder')
    w4 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (2.0, 1.0, 0.0), Vector (2.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', w4))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w3, 2, w4, 1))
    w5 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (2.0, 2.0, 0.0), Vector (4.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, w5, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w4, 2, w5, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceX', w5, 1, w5, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Config.FugeBorder')
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', r, 2, w5, 2))
    fuge_wall_weir.MapMode = 'FlatFace'
    fuge_wall_weir.Placement = placemnt
    fuge_wall_weir.Visibility = False
    fuge_wall_weir.ViewObject.Visibility = False
    fuge.addObject(fuge_wall_weir)
    main_face = doc.addObject('PartDesign::Pad', 'main_face')
    main_face.Direction = Vector(0.00, -1.00, -0.00)
    main_face.setExpression('Length', 'Config.SumpAcrylicThickness')
    main_face.Length = 4.0
    main_face.Placement = placemnt
    main_face.Profile = (fuge_wall_weir, [])
    main_face.ReferenceAxis = (fuge_wall_weir, ['N_Axis'])
    main_face.Visibility = False
    fuge.addObject(main_face)
    main_face.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    main_face.ViewObject.Visibility = False
    fuge_rounded = fuge.newObject('PartDesign::Fillet','Fillet')
    fuge_rounded.Radius = 5.0
    fuge_rounded.setExpression('Radius', 'Config.FugeFillet/2')
    fuge_rounded.Base = (main_face, ["Edge17","Edge8","Edge11","Edge14",])
    fuges = Draft.make_ortho_array(fuge, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuges.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuges.setExpression('NumberY', 'Config.FugeCompartments')
    fuges.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+(Config.SumpExtraMargin+Config.MetalProfileHeight)+Config.SumpExtraSpaceForChiller+(Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment)')
    fuges.setExpression('.Placement.Base.y', '-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)')
    fuges.setExpression('.Placement.Base.z', z_b)
    fuges.Fuse=True
    glass_color(fuges)
    grp.addObject(fuges)
    fuge_door = doc.addObject('PartDesign::Body', 'RefugiumsDoor')
    fuge_door.Group = []
    fuge_door_weir = doc.addObject('Sketcher::SketchObject', 'fuge_door_weir')
    b = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (100.0, 0.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, -1, 1))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Horizontal', b))
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, b, 2, 1.0))
    LastConstrainExp(fuge_door_weir, 'Computed.SumpCompartmentLength')
    r = fuge_door_weir.addGeometry(Part.LineSegment(Vector (100.0, 0.0, 0.0), Vector (100.0, 50.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Vertical', r))
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, r, 2, 1.0))
    LastConstrainExp(fuge_door_weir, '(Config.SumpHeight-Config.SumpAcrylicThickness)/2+Config.FugeBorder')
    l = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (0.0, 50.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Vertical', l))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, l, 1))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', b, 2, r, 1))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, r, 2))
    t = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 2.0, 0.0), Vector (1.0, 2.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', t, 1, l, 2))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', t, 2, r, 2))
    fuge_door_weir.MapMode = 'FlatFace'
    fuge_door_weir.Placement = placemnt
    fuge_door_weir.Visibility = False
    fuge_door_weir.ViewObject.Visibility = False
    fuge_door.addObject(fuge_door_weir)
    main_door_face = doc.addObject('PartDesign::Pad', 'main_door_face')
    main_door_face.Direction = Vector(0.00, -1.00, -0.00)
    main_door_face.setExpression('Length', 'Config.SumpAcrylicThickness')
    main_door_face.Length = 4.0
    main_door_face.Placement = placemnt
    main_door_face.Profile = (fuge_door_weir, [])
    main_door_face.ReferenceAxis = (fuge_door_weir, ['N_Axis'])
    main_door_face.Visibility = False
    fuge_door.addObject(main_door_face)
    fuge_door_rounded = fuge_door.newObject('PartDesign::Fillet','DoorFilleted')
    fuge_door_rounded.Radius = 5.0
    fuge_door_rounded.setExpression('Radius', 'Config.FugeFillet/2')
    fuge_door_rounded.Base = (main_door_face, ["Edge1","Edge2","Edge5","Edge8",])
    fuge_doors = Draft.make_ortho_array(fuge_door, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuge_doors.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuge_doors.setExpression('NumberY', 'Config.FugeCompartments')
    fuge_doors.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+(Config.SumpExtraMargin+Config.MetalProfileHeight)+Config.SumpExtraSpaceForChiller+(Computed.Width-2*(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment)')
    fuge_doors.setExpression('.Placement.Base.y', '-Computed.Length/2+(Config.SumpExtraMargin+Config.MetalProfileHeight+Config.SumpAcrylicThickness)')
    fuge_doors.setExpression('.Placement.Base.z', z_b)
    return grp
