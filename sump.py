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
from utils import glass_color, make_panel, LastConstrainExp
from holes import getHole, drill

def sump_color(obj):
    obj.ViewObject.ShapeColor=(1.0, 1.0, 1.0)
    obj.ViewObject.Transparency=0
    return obj

def make_sump(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Sump')
    grp_bp = doc.addObject('App::DocumentObjectGroup','Bottom')
    grp.addObject(grp_bp)
    grp_gs = doc.addObject('App::DocumentObjectGroup','SidesSump')
    grp.addObject(grp_gs)
    grp_fg = doc.addObject('App::DocumentObjectGroup','Fuges')
    grp.addObject(grp_fg)
    grp_bs = doc.addObject('App::DocumentObjectGroup','BracesSumpPanel')
    grp.addObject(grp_bs)
    grp.Label = 'Sump'
    bg = make_panel(doc, grp_bp, 'BottomAcrylic','Computed.LeftCornerXSump','Computed.FrontCornerYSump','Computed.SumpAcrylicLevel','Computed.SumpWidth-Config.SumpExtraSpaceForChiller','Computed.SumpLength','Config.SumpAcrylicThickness')
    sump_color(bg)
    z_b = 'Computed.SumpAcrylicLevel+Config.SumpAcrylicThickness'
    bs = make_panel(doc, None, 'BracesAcrylic','Computed.LeftCornerXSump','Computed.FrontCornerYSump',z_b+'+Computed.SumpPanelsHeight','Computed.SumpWidth-Config.SumpExtraSpaceForChiller','Computed.SumpLength','Config.SumpAcrylicThickness')
    glass_color(bs)
    base = doc.addObject("Part::Cut", "SumpLid")
    base.Base = bs
    base.Tool = getHole(doc, 'Sump')
    grp_bs.addObject(base)
    def rounded(name, px, py, pz, length, width, height):
        b = doc.addObject('PartDesign::Body', name)
        b.Group = []
        box = b.newObject('PartDesign::AdditiveBox', name)
        b.setExpression('.Placement.Base.x', px)
        b.setExpression('.Placement.Base.y', py)
        b.setExpression('.Placement.Base.z', pz)
        box.setExpression('Length', length)
        box.setExpression('Width', width)
        box.setExpression('Height', height)
        rounded = b.newObject('PartDesign::Fillet', f'{name}Filleted')
        rounded.Radius = 5.0
        rounded.setExpression('Radius', 'Config.SumpBraceFillet/2')
        rounded.Base = (box, ['Edge1','Edge3','Edge5','Edge7'])
        rounded.Visibility = False
        return b
    m = rounded('MainHole', 'Computed.LeftCornerXSump+(Computed.SumpWetWidth-Config.SumpInternalSpaceForEquipment)+Config.SumpBraceWidth', 'Computed.FrontCornerYSump+Config.SumpBraceWidth', z_b+'+Computed.SumpPanelsHeight-Config.SumpAcrylicThickness', 'Config.SumpInternalSpaceForEquipment-2*Config.SumpBraceWidth', 'Computed.SumpLength-2*Config.SumpBraceWidth', '3*Config.SumpAcrylicThickness')
    drill(doc, 'Sump', m)
    back = make_panel(doc, grp_gs, 'BackPanel','Computed.LeftCornerXSump','Computed.BackCornerYSump-Config.SumpAcrylicThickness', z_b, 'Computed.SumpWidth-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Computed.SumpPanelsHeight')
    sump_color(back)
    left = make_panel(doc, grp_gs, 'LeftPanel','Computed.LeftCornerXSump','Computed.FrontCornerYSump', z_b, 'Config.SumpAcrylicThickness','Computed.SumpLength-Config.SumpAcrylicThickness','Computed.SumpPanelsHeight')
    sump_color(left)
    placemnt = Placement(Vector(0, 0, 0), Rotation (90, 0, 90))
    right = make_panel(doc, grp_gs, 'RightPanel','Computed.RightCornerXSump-Config.SumpAcrylicThickness','Computed.FrontCornerYSump', z_b, 'Config.SumpAcrylicThickness','Computed.SumpLength-Config.SumpAcrylicThickness','Computed.SumpPanelsHeight')
    sump_color(right)
    front = make_panel(doc, grp_gs, 'FrontPanel','Computed.LeftCornerXSump+Config.SumpAcrylicThickness','Computed.FrontCornerYSump', z_b, 'Computed.SumpWidth-2*Config.SumpAcrylicThickness-Config.SumpExtraSpaceForChiller','Config.SumpAcrylicThickness','Computed.SumpPanelsHeight')
    glass_color(front)
    fuge_spliter = make_panel(doc, grp_fg, 'RefugiumsSplitter','Computed.LeftCornerXSump+Config.SumpAcrylicThickness','Computed.FrontCornerYSump', z_b, 'Computed.Width-(Config.SumpMarginLeft+Config.SumpMarginRight+2*(Config.MetalProfileHeight+Config.SumpAcrylicThickness))-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment-Config.SumpAcrylicThickness','Config.SumpAcrylicThickness','Computed.SumpPanelsHeight')
    fuge_spliters = Draft.make_ortho_array(fuge_spliter, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuge_spliters.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuge_spliters.setExpression('NumberY', 'Config.FugeCompartments')
    fuge_spliters.Label = 'RefugiumsSplitters'
    grp_fg.addObject(fuge_spliters)
    glass_color(fuge_spliters)
    fuge_hatch = rounded('RefugiumsHatch','Computed.LeftCornerXSump+Config.SumpBraceWidth','Computed.FrontCornerYSump+Config.SumpBraceWidth', z_b+'+Computed.SumpPanelsHeight-Config.SumpAcrylicThickness', 'Computed.Width-(Config.SumpMarginLeft+Config.SumpMarginRight+2*(Config.MetalProfileHeight+Config.SumpAcrylicThickness))-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment-Config.SumpAcrylicThickness-2*Config.SumpBraceWidth','Computed.SumpCompartmentLength-2*Config.SumpBraceWidth','3*Config.SumpAcrylicThickness')
    fuge_hatchs = Draft.make_ortho_array(fuge_hatch, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuge_hatchs.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength+Config.SumpAcrylicThickness')
    fuge_hatchs.setExpression('NumberY', 'Config.FugeCompartments')
    fuge_hatchs.Label = 'RefugiumsHatchs'
    grp_bs.addObject(fuge_hatchs)
    drill(doc, 'Sump', fuge_hatchs)
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
    LastConstrainExp(fuge_wall_weir, 'Computed.SumpPanelsHeight')
    l = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (0.0, 50.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', l))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, l, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', b, 2, r, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, r, 2))
    w1 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (0.0, 2.0, 0.0), Vector (1.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', w1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, w1, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Config.FugeBorder+Config.FugeSlideSpacing')
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', l, 2, w1, 1))
    w2 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (1.0, 2.0, 0.0), Vector (1.0, 1.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', w2))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w1, 2, w2, 1))
    w3 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (1.0, 1.0, 0.0), Vector (2.0, 1.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', w3))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w2, 2, w3, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, w3, 1, 1.0))
    LastConstrainExp(fuge_wall_weir, '(Computed.SumpPanelsHeight)/2')
    w4 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (2.0, 1.0, 0.0), Vector (2.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Vertical', w4))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w3, 2, w4, 1))
    w5 = fuge_wall_weir.addGeometry(Part.LineSegment(Vector (2.0, 2.0, 0.0), Vector (4.0, 2.0, 0.0)))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, w5, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('Coincident', w4, 2, w5, 1))
    fuge_wall_weir.addConstraint(Sketcher.Constraint('DistanceX', w5, 1, w5, 2, 1.0))
    LastConstrainExp(fuge_wall_weir, 'Config.FugeBorder+Config.FugeSlideSpacing+Config.SumpAcrylicThickness')
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
    fuge_rounded.Base = (main_face, ["Edge11","Edge14"])
    fuge_rounded.Visibility = False
    fuge_slot = doc.addObject('Sketcher::SketchObject', 'fuge_slot')
    def make_slot(x_pos):
        arc_up = fuge_slot.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(1.00, 10.0, 0.0), Vector (0.0, 0.0, 1.0), 1.50), 0, pi))
        fuge_slot.addConstraint(Sketcher.Constraint('Diameter', arc_up, 1.0))
        LastConstrainExp(fuge_slot, 'Config.FugeWeirFastenerDiameter')
        arc_down = fuge_slot.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(1.00, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.50), pi, 2*pi))
        fuge_slot.addConstraint(Sketcher.Constraint('Diameter', arc_down, 1.0))
        LastConstrainExp(fuge_slot, 'Config.FugeWeirFastenerDiameter')
        fuge_slot.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, arc_up, 3, 1.0))
        LastConstrainExp(fuge_slot, 'Config.SumpHeight - Config.SumpAcrylicThickness - Computed.FugeWeirHoleMargin')
        fuge_slot.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, arc_down, 3, 1.0))
        LastConstrainExp(fuge_slot, 'Config.SumpHeight - Config.SumpAcrylicThickness - Computed.FugeWeirHoleMargin-Computed.FugeWeirSlotVerticalHeight')
        fuge_slot.addConstraint(Sketcher.Constraint('DistanceX', -1, 1, arc_up, 3, 1.0))
        LastConstrainExp(fuge_slot, x_pos)
        fuge_slot.addConstraint(Sketcher.Constraint('Vertical', arc_up, 3, arc_down, 3))
        fuge_slot.addConstraint(Sketcher.Constraint('Horizontal', arc_up, 3, arc_up, 1))
        fuge_slot.addConstraint(Sketcher.Constraint('Horizontal', arc_up, 3, arc_up, 2))
        fuge_slot.addConstraint(Sketcher.Constraint('Horizontal', arc_down, 3, arc_down, 1))
        fuge_slot.addConstraint(Sketcher.Constraint('Horizontal', arc_down, 3, arc_down, 2))
        line_left = fuge_slot.addGeometry(Part.LineSegment(Vector (0.0, 1.0, 0.0), Vector (0.0, 10.0, 0.0)))
        fuge_slot.addConstraint(Sketcher.Constraint('Coincident', arc_up, 2, line_left, 2))
        fuge_slot.addConstraint(Sketcher.Constraint('Coincident', arc_down, 1, line_left, 1))
        line_right = fuge_slot.addGeometry(Part.LineSegment(Vector (2.0, 1.0, 0.0), Vector (2.0, 10.0, 0.0)))
        fuge_slot.addConstraint(Sketcher.Constraint('Coincident', arc_up, 1, line_right, 2))
        fuge_slot.addConstraint(Sketcher.Constraint('Coincident', arc_down, 2, line_right, 1))
    make_slot('Config.FugeSlideSpacing+Computed.FugeWeirHoleMargin')
    make_slot('Computed.SumpCompartmentHoleSpacing')
    fuge_slot.MapMode = 'FlatFace'
    fuge_slot.Placement = placemnt
    fuge_slot.Visibility = False
    fuge_slot.ViewObject.Visibility = False
    fuge.addObject(fuge_slot)
    fuge_slide_slot = doc.addObject('PartDesign::Pocket', 'fuge_slide_slot')
    fuge_slide_slot.BaseFeature = fuge_rounded
    fuge_slide_slot.Direction = Vector(-0.00, 1.00, 0.00)
    fuge_slide_slot.Midplane = True
    fuge_slide_slot.Placement = placemnt
    fuge_slide_slot.Profile = (fuge_slot, [])
    fuge_slide_slot.ReferenceAxis = (fuge_slot, ['N_Axis'])
    fuge_slide_slot.Type = 'ThroughAll'
    fuge_slide_slot.Visibility = False
    fuge_slide_slot.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    fuge_slide_slot.ViewObject.Visibility = False
    fuge.addObject(fuge_slide_slot)
    fuge_slide_vert_slots = doc.addObject('PartDesign::LinearPattern', 'fuge_slide_vert_slots')
    fuge_slide_vert_slots.BaseFeature = fuge_slide_slot
    fuge_slide_vert_slots.Direction = (fuge_slot, ['V_Axis'])
    fuge_slide_vert_slots.Reversed = True
    fuge_slide_vert_slots.setExpression('Length', 'Computed.FugeWeirSlotVerticalOffset')
    fuge_slide_vert_slots.setExpression('Occurrences', 'Config.FugeWeirSlotsVerticalCount')
    fuge_slide_vert_slots.Occurrences = 2
    fuge_slide_vert_slots.Originals = [fuge_slide_slot]
    fuge_slide_vert_slots.Placement = placemnt
    fuge_slide_vert_slots.Visibility = False
    fuge_slide_vert_slots.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    fuge_slide_vert_slots.ViewObject.Visibility = False
    fuge.addObject(fuge_slide_vert_slots)

    fuges = Draft.make_ortho_array(fuge, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuges.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuges.setExpression('NumberY', 'Config.FugeCompartments')
    fuges.setExpression('.Placement.Base.x', 'Computed.LeftCornerXSump+(Computed.Width-(Config.SumpMarginLeft+Config.SumpMarginRight+2*(Config.MetalProfileHeight+Config.SumpAcrylicThickness))-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment)')
    fuges.setExpression('.Placement.Base.y', 'Computed.FrontCornerYSump+Config.SumpAcrylicThickness')
    fuges.setExpression('.Placement.Base.z', z_b)
    fuges.Fuse=True
    fuges.Label='RefugiumsWeir'
    fuges_panel = doc.addObject("Part::Cut", "RefugiumsWeirPanel")
    glass_color(fuges)
    fuges_panel.Base = fuges
    fuges_panel.Tool = back
    grp_fg.addObject(fuges_panel)
    back.Visibility = True
    glass_color(fuges_panel)
    fuge_door = doc.addObject('PartDesign::Body', 'RefugiumsDoor')
    fuge_door.Group = []
    fuge_door_weir = doc.addObject('Sketcher::SketchObject', 'fuge_door_weir')
    b = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (100.0, 0.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Horizontal', b))
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, b, 1, 1.0))
    LastConstrainExp(fuge_door_weir, 'Config.FugeSlideSpacing')
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, b, 2, 1.0))
    LastConstrainExp(fuge_door_weir, 'Computed.SumpCompartmentLength-(Config.FugeSlideSpacing+Config.SumpAcrylicThickness)')
    r = fuge_door_weir.addGeometry(Part.LineSegment(Vector (100.0, 0.0, 0.0), Vector (100.0, 50.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Vertical', r))
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, r, 1, 1.0))
    LastConstrainExp(fuge_door_weir, 'Computed.FugeWeirDoorHeight')
    l = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 0.0, 0.0), Vector (0.0, 50.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Vertical', l))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', b, 1, l, 1))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', b, 2, r, 1))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Horizontal', l, 2, r, 2))
    t = fuge_door_weir.addGeometry(Part.LineSegment(Vector (0.0, 2.0, 0.0), Vector (1.0, 2.0, 0.0)))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', t, 1, l, 2))
    fuge_door_weir.addConstraint(Sketcher.Constraint('Coincident', t, 2, r, 2))
    fuge_door_weir.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, t, 2, 1.0))
    LastConstrainExp(fuge_door_weir, 'Computed.SumpPanelsHeight')
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
    fuge_door_rounded.Visibility = False
    weir_door_fastener = doc.addObject('Sketcher::SketchObject', 'weir_door_fastener')
    geo0 = weir_door_fastener.addGeometry(Part.Circle(Vector(1.0, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.00))
    geo1 = weir_door_fastener.addGeometry(Part.Circle(Vector(1.0, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.00))
    weir_door_fastener.addConstraint(Sketcher.Constraint('Diameter', geo0, 1.0))
    LastConstrainExp(weir_door_fastener, 'Config.FugeMountHoleDiameter')
    weir_door_fastener.addConstraint(Sketcher.Constraint('Diameter', geo1, 1.0))
    LastConstrainExp(weir_door_fastener, 'Config.FugeMountHoleDiameter')
    weir_door_fastener.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo0, 3, 1.0))
    LastConstrainExp(weir_door_fastener, 'Config.SumpHeight - Config.SumpAcrylicThickness - Computed.FugeWeirHoleMargin')
    weir_door_fastener.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo1, 3, 1.0))
    LastConstrainExp(weir_door_fastener, 'Config.SumpHeight - Config.SumpAcrylicThickness - Computed.FugeWeirHoleMargin')
    weir_door_fastener.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 1.0))
    LastConstrainExp(weir_door_fastener, 'Config.FugeSlideSpacing+Computed.FugeWeirHoleMargin')
    weir_door_fastener.addConstraint(Sketcher.Constraint('DistanceX', geo1, 3, 1.0))
    LastConstrainExp(weir_door_fastener, 'Computed.SumpCompartmentLength-Config.SumpAcrylicThickness-(Config.FugeSlideSpacing+Computed.FugeWeirHoleMargin)')
    weir_door_fastener.MapMode = 'FlatFace'
    weir_door_fastener.Placement = placemnt
    weir_door_fastener.Visibility = False
    weir_door_fastener.ViewObject.Visibility = False
    fuge_door.addObject(weir_door_fastener)
    weir_vert_hole = doc.addObject('PartDesign::Pocket', 'weir_vert_hole')
    weir_vert_hole.BaseFeature = main_face
    weir_vert_hole.Direction = Vector(-0.00, 1.00, 0.00)
    weir_vert_hole.Midplane = True
    weir_vert_hole.Placement = placemnt
    weir_vert_hole.Profile = (weir_door_fastener, [])
    weir_vert_hole.ReferenceAxis = (weir_door_fastener, ['N_Axis'])
    weir_vert_hole.Type = 'ThroughAll'
    weir_vert_hole.Visibility = False
    weir_vert_hole.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    weir_vert_hole.ViewObject.Visibility = False
    fuge_door.addObject(weir_vert_hole)
    all_weir_door_vert_fasteners = doc.addObject('PartDesign::LinearPattern', 'all_weir_door_vert_fasteners')
    all_weir_door_vert_fasteners.BaseFeature = weir_vert_hole
    all_weir_door_vert_fasteners.Direction = (weir_door_fastener, ['V_Axis'])
    all_weir_door_vert_fasteners.Reversed = True
    all_weir_door_vert_fasteners.setExpression('Length', 'Computed.FugeWeirFastenerVerticalHeight')
    all_weir_door_vert_fasteners.setExpression('Occurrences', 'Config.FugeWeirFastenerVerticalCount')
    #all_weir_door_vert_fasteners.Length = 10.0
    all_weir_door_vert_fasteners.Occurrences = 2
    all_weir_door_vert_fasteners.Originals = [weir_vert_hole]
    all_weir_door_vert_fasteners.Placement = placemnt
    all_weir_door_vert_fasteners.Visibility = False
    all_weir_door_vert_fasteners.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_weir_door_vert_fasteners.ViewObject.Visibility = False
    fuge_door.addObject(all_weir_door_vert_fasteners)

    slot_profile_fuge = doc.addObject('Sketcher::SketchObject', 'slot_profile_fuge_fuge')
    geo0 = slot_profile_fuge.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(12.50, 445.00, 0.00), Vector (0.0, 0.0, 1.0), 1.50), 0, pi))
    geo1 = slot_profile_fuge.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(12.50, 400.00, 0.00), Vector (0.0, 0.0, 1.0), 1.50), pi, 2 * pi))
    geo2 = slot_profile_fuge.addGeometry(Part.LineSegment(Vector (11.0, 445.0, 0.0), Vector (11.0, 400.0, 0.0)))
    geo3 = slot_profile_fuge.addGeometry(Part.LineSegment(Vector (14.0, 400.0, 0.0), Vector (14.0, 445.0, 0.0)))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Tangent', geo0, 2, geo2, 1))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Tangent', geo2, 2, geo1, 1))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Tangent', geo1, 2, geo3, 1))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Tangent', geo3, 2, geo0, 1))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Equal', geo0, geo1))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Vertical', geo2))
    slot_profile_fuge.addConstraint(Sketcher.Constraint('Diameter', geo0, 3.0))
    LastConstrainExp(slot_profile_fuge, 'Config.FugeSlotWidth')
    slot_profile_fuge.addConstraint(Sketcher.Constraint('DistanceY', geo0, 3, 200))
    LastConstrainExp(slot_profile_fuge, 'Computed.SumpPanelsHeight-Config.FugeSlotWidth')
    slot_profile_fuge.addConstraint(Sketcher.Constraint('DistanceY', geo1, 3, 100))
    LastConstrainExp(slot_profile_fuge, 'Computed.SumpPanelsHeight-Config.FugeSlotWidth-Config.FugeSlotHeight')
    slot_profile_fuge.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 10))
    LastConstrainExp(slot_profile_fuge, 'Config.FugeBorder+Config.FugeSlideSpacing+Config.FugeSlotWidth/2')
    slot_profile_fuge.MapMode = 'FlatFace'
    slot_profile_fuge.Placement = placemnt
    slot_profile_fuge.Visibility = False
    slot_profile_fuge.ViewObject.Visibility = False
    fuge_door.addObject(slot_profile_fuge)
    one_slot = doc.addObject('PartDesign::Pocket', 'one_slot')
    one_slot.BaseFeature = all_weir_door_vert_fasteners
    one_slot.Direction = Vector(-0.00, 1.00, 0.00)
    one_slot.Midplane = True
    one_slot.Placement = placemnt
    one_slot.Profile = (slot_profile_fuge, [])
    one_slot.ReferenceAxis = (slot_profile_fuge, ['N_Axis'])
    one_slot.Type = 'ThroughAll'
    one_slot.Visibility = False
    one_slot.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    one_slot.ViewObject.Visibility = False
    fuge_door.addObject(one_slot)
    all_slots = doc.addObject('PartDesign::LinearPattern', 'all_slots')
    all_slots.BaseFeature = one_slot
    all_slots.Direction = (slot_profile_fuge, ['H_Axis'])
    all_len = 'Computed.SumpCompartmentLength-Config.SumpAcrylicThickness-2*(Config.FugeBorder+Config.FugeSlideSpacing)-Config.FugeSlotWidth'
    all_slots.setExpression('Length', all_len)
    all_slots.setExpression('Occurrences', '(' + all_len + ')/(2*Config.WeirSlotWidth)')
    all_slots.Length = 781.0
    all_slots.Occurrences = 130
    all_slots.Originals = [one_slot]
    all_slots.Placement = placemnt
    all_slots.Visibility = False
    all_slots.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_slots.ViewObject.Visibility = False
    fuge_door.addObject(all_slots)
    fuge_doors = Draft.make_ortho_array(fuge_door, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=2, n_z=1, use_link=False)
    fuge_doors.Label = 'RefugiumsDoors'
    fuge_doors.setExpression('.IntervalY.y', 'Computed.SumpCompartmentLength')
    fuge_doors.setExpression('NumberY', 'Config.FugeCompartments')
    fuge_doors.setExpression('.Placement.Base.x', 'Computed.LeftCornerX+(Config.SumpMarginLeft+Config.MetalProfileHeight)+Config.SumpExtraSpaceForChiller+(Computed.Width-(Config.SumpMarginLeft+Config.SumpMarginRight+2*(Config.MetalProfileHeight+Config.SumpAcrylicThickness))-Config.SumpExtraSpaceForChiller-Config.SumpInternalSpaceForEquipment)-+Config.SumpAcrylicThickness')
    fuge_doors.setExpression('.Placement.Base.y', 'Computed.FrontCornerYSump+Config.SumpAcrylicThickness')
    fuge_doors.setExpression('.Placement.Base.z', z_b)
    glass_color(fuge_doors)
    grp_fg.addObject(fuge_doors)
    return grp
