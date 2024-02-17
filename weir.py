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


def create_weir(doc):
    placemnt = Placement(Vector(0, 0, 0), Rotation (0.7071067811865476, 0, 0, 0.7071067811865475))
    Weir = doc.addObject('PartDesign::Body', 'Weir')
    Weir.Group = []
    Weir.setExpression('.Placement.Base.x', 'Computed.LeftCornerX')
    Weir.setExpression('.Placement.Base.y', 'Computed.Length/2-Config.SidesGlassThickness-Computed.WeirDepth')
    Weir.setExpression('.Placement.Base.z', '(Computed.GlassLevel+Config.BottomGlassThickness)*1 mm')
    main_face_profile = doc.addObject('Sketcher::SketchObject', 'main_face_profile')
    b = main_face_profile.addGeometry(Part.LineSegment(Vector (100.0, 0.0, 0.0), Vector (700.0, 0.0, 0.0)))
    r = main_face_profile.addGeometry(Part.LineSegment(Vector (700.0, 0.0, 0.0), Vector (700.0, 400.0, 0.0)))
    t = main_face_profile.addGeometry(Part.LineSegment(Vector (700.0, 400.0, 0.0), Vector (100.0, 400.0, 0.0)))
    l = main_face_profile.addGeometry(Part.LineSegment(Vector (100.0, 400.0, 0.0), Vector (100.0, 0.0, 0.0)))
    main_face_profile.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, l, 1, 100.00))
    main_face_profile.setExpression('Constraints[0]', 'Computed.WeirMargin')
    main_face_profile.addConstraint(Sketcher.Constraint('DistanceX', -2, 1, r, 2, 700.00))
    main_face_profile.setExpression('Constraints[1]', 'Computed.WeirWidth+Computed.WeirMargin')
    main_face_profile.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, r, 2, 400.00))
    main_face_profile.setExpression('Constraints[2]', 'Computed.RealGlassHeight')
    main_face_profile.addConstraint(Sketcher.Constraint('Coincident', b, 2, r, 1))
    main_face_profile.addConstraint(Sketcher.Constraint('Coincident', r, 2, t, 1))
    main_face_profile.addConstraint(Sketcher.Constraint('Coincident', t, 2, l, 1))
    main_face_profile.addConstraint(Sketcher.Constraint('Coincident', l, 2, b, 1))
    main_face_profile.addConstraint(Sketcher.Constraint('Horizontal', b))
    main_face_profile.addConstraint(Sketcher.Constraint('Horizontal', t))
    main_face_profile.addConstraint(Sketcher.Constraint('Vertical', l))
    main_face_profile.addConstraint(Sketcher.Constraint('Vertical', r))
    main_face_profile.addConstraint(Sketcher.Constraint('PointOnObject', b, 1, -1))
    main_face_profile.MapMode = 'FlatFace'
    main_face_profile.Placement = placemnt
    main_face_profile.Visibility = False
    main_face_profile.ViewObject.Visibility = False
    Weir.addObject(main_face_profile)
    main_face = doc.addObject('PartDesign::Pad', 'main_face')
    main_face.Direction = Vector(0.00, -1.00, -0.00)
    main_face.setExpression('Length', 'Config.WeirWallThickness')
    main_face.Length = 4.0
    main_face.Placement = placemnt
    main_face.Profile = (main_face_profile, [])
    main_face.ReferenceAxis = (main_face_profile, ['N_Axis'])
    main_face.Visibility = False
    Weir.addObject(main_face)
    main_face.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    main_face.ViewObject.Visibility = False
    slot_profile = doc.addObject('Sketcher::SketchObject', 'slot_profile')
    geo0 = slot_profile.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(12.50, 445.00, 0.00), Vector (0.0, 0.0, 1.0), 1.50), 0, pi))
    geo1 = slot_profile.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(12.50, 400.00, 0.00), Vector (0.0, 0.0, 1.0), 1.50), pi, 2 * pi))
    geo2 = slot_profile.addGeometry(Part.LineSegment(Vector (11.0, 445.0, 0.0), Vector (11.0, 400.0, 0.0)))
    geo3 = slot_profile.addGeometry(Part.LineSegment(Vector (14.0, 400.0, 0.0), Vector (14.0, 445.0, 0.0)))
    slot_profile.addConstraint(Sketcher.Constraint('Tangent', geo0, 2, geo2, 1))
    slot_profile.addConstraint(Sketcher.Constraint('Tangent', geo2, 2, geo1, 1))
    slot_profile.addConstraint(Sketcher.Constraint('Tangent', geo1, 2, geo3, 1))
    slot_profile.addConstraint(Sketcher.Constraint('Tangent', geo3, 2, geo0, 1))
    slot_profile.addConstraint(Sketcher.Constraint('Equal', geo0, geo1))
    slot_profile.addConstraint(Sketcher.Constraint('Vertical', geo2))
    slot_profile.addConstraint(Sketcher.Constraint('Diameter', geo0, 3.0))
    slot_profile.addConstraint(Sketcher.Constraint('DistanceY', geo1, 3, 400.00))
    slot_profile.addConstraint(Sketcher.Constraint('DistanceY', geo0, 3, 445.00))
    slot_profile.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 12.50))
    slot_profile.setExpression('Constraints[6]', 'Config.WeirSlotWidth')
    slot_profile.setExpression('Constraints[7]', 'Config.WaterHeightWeir')
    slot_profile.setExpression('Constraints[8]', 'Computed.RealGlassHeight-Config.SidesGlassThickness-Config.WeirSlotWidth*0.5')
    slot_profile.setExpression('Constraints[9]', '2*Config.SidesGlassThickness+Config.BraceWidth+Config.WeirSlotWidth*0.5')
    slot_profile.MapMode = 'FlatFace'
    slot_profile.Placement = placemnt
    slot_profile.Visibility = False
    slot_profile.ViewObject.Visibility = False
    Weir.addObject(slot_profile)
    one_slot = doc.addObject('PartDesign::Pocket', 'one_slot')
    one_slot.BaseFeature = main_face
    one_slot.Direction = Vector(-0.00, 1.00, 0.00)
    one_slot.Midplane = True
    one_slot.Placement = placemnt
    one_slot.Profile = (slot_profile, [])
    one_slot.ReferenceAxis = (slot_profile, ['N_Axis'])
    one_slot.Type = 'ThroughAll'
    one_slot.Visibility = False
    one_slot.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    one_slot.ViewObject.Visibility = False
    Weir.addObject(one_slot)
    all_slots = doc.addObject('PartDesign::LinearPattern', 'all_slots')
    all_slots.BaseFeature = one_slot
    all_slots.Direction = (slot_profile, ['H_Axis'])
    all_len = 'Computed.WeirInsideWidth-Config.WeirSlotWidth'
    all_slots.setExpression('Length', all_len)
    all_slots.setExpression('Occurrences', '(' + all_len + ')/(2*Config.WeirSlotWidth)')
    all_slots.Length = 781.0
    all_slots.Occurrences = 130
    all_slots.Originals = [one_slot]
    all_slots.Placement = placemnt
    all_slots.Visibility = False
    all_slots.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_slots.ViewObject.Visibility = False
    Weir.addObject(all_slots)
    fasteners_reinforcement_profile = doc.addObject('Sketcher::SketchObject', 'fastener_reinforcement')
    geo0 = fasteners_reinforcement_profile.addGeometry(Part.Circle(Vector(1.0, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.00))
    fasteners_reinforcement_profile.addConstraint(Sketcher.Constraint('Diameter', geo0, 1.0))
    fasteners_reinforcement_profile.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo0, 3, 1.0))
    fasteners_reinforcement_profile.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 1.0))
    fasteners_reinforcement_profile.setExpression('Constraints[0]', '2*Config.WeirFastenerDiameter')
    fasteners_reinforcement_profile.setExpression('Constraints[1]', 'Computed.RealGlassHeight-Config.SidesGlassThickness-Config.WeirFastenerOffset')
    fasteners_reinforcement_profile.setExpression('Constraints[2]', 'Computed.WeirMargin+Config.SidesGlassThickness+Config.WeirFastenerOffset')
    fasteners_reinforcement_profile.MapMode = 'FlatFace'
    fasteners_reinforcement_profile.Placement = placemnt
    fasteners_reinforcement_profile.Visibility = False
    fasteners_reinforcement_profile.ViewObject.Visibility = False
    Weir.addObject(fasteners_reinforcement_profile)
    fasteners_reinforcement = doc.addObject('PartDesign::Pad', 'fasteners_reinforcement')
    fasteners_reinforcement.BaseFeature = all_slots
    fasteners_reinforcement.Direction = Vector(0.00, -1.00, -0.00)
    fasteners_reinforcement.setExpression('Length', 'Config.WeirWallThickness')
    fasteners_reinforcement.Length = 4.0
    fasteners_reinforcement.Placement = placemnt
    fasteners_reinforcement.Profile = (fasteners_reinforcement_profile, [])
    fasteners_reinforcement.ReferenceAxis = (fasteners_reinforcement_profile, ['N_Axis'])
    fasteners_reinforcement.Visibility = False
    fasteners_reinforcement.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    fasteners_reinforcement.ViewObject.Visibility = False
    Weir.addObject(fasteners_reinforcement)
    all_hor_reinforcements = doc.addObject('PartDesign::LinearPattern', 'all_hor_reinforcements')
    all_hor_reinforcements.BaseFeature = fasteners_reinforcement_profile
    all_hor_reinforcements.Direction = (fasteners_reinforcement_profile, ['H_Axis'])
    all_len = 'Computed.WeirHorizontalFastenerHidth'
    all_hor_reinforcements.setExpression('Length', all_len)
    all_hor_reinforcements.setExpression('Occurrences', 'Config.WeirFastenerHorizontalCount')
    all_hor_reinforcements.Length = 10.0
    all_hor_reinforcements.Occurrences = 2
    all_hor_reinforcements.Originals = [fasteners_reinforcement]
    all_hor_reinforcements.Placement = placemnt
    all_hor_reinforcements.Visibility = False
    all_hor_reinforcements.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_hor_reinforcements.ViewObject.Visibility = False
    Weir.addObject(all_hor_reinforcements)
    fastener_profile = doc.addObject('Sketcher::SketchObject', 'fastener_profile')
    geo0 = fastener_profile.addGeometry(Part.Circle(Vector(1.0, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.00))
    geo1 = fastener_profile.addGeometry(Part.Circle(Vector(1.0, 1.0, 0.0), Vector (0.0, 0.0, 1.0), 1.00))
    fastener_profile.addConstraint(Sketcher.Constraint('Diameter', geo0, 1.0))
    fastener_profile.addConstraint(Sketcher.Constraint('Diameter', geo1, 1.0))
    fastener_profile.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo0, 3, 1.0))
    fastener_profile.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo1, 3, 1.0))
    fastener_profile.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 1.0))
    fastener_profile.addConstraint(Sketcher.Constraint('DistanceX', geo1, 3, 1.0))
    fastener_profile.setExpression('Constraints[0]', 'Config.WeirFastenerDiameter')
    fastener_profile.setExpression('Constraints[1]', 'Config.WeirFastenerDiameter')
    fastener_profile.setExpression('Constraints[2]', 'Computed.RealGlassHeight-Config.SidesGlassThickness-Config.WeirFastenerOffset')
    fastener_profile.setExpression('Constraints[3]', 'Config.BraceWidth+Config.WeirFastenerOffset')
    fastener_profile.setExpression('Constraints[4]', 'Computed.WeirMargin+Config.SidesGlassThickness+Config.WeirFastenerOffset')
    fastener_profile.setExpression('Constraints[5]', 'Computed.WeirMargin+Config.SidesGlassThickness+Config.WeirFastenerOffset')
    fastener_profile.MapMode = 'FlatFace'
    fastener_profile.Placement = placemnt
    fastener_profile.Visibility = False
    fastener_profile.ViewObject.Visibility = False
    Weir.addObject(fastener_profile)
    fastener_hole = doc.addObject('PartDesign::Pocket', 'fastener_hole')
    fastener_hole.BaseFeature = all_slots
    fastener_hole.Direction = Vector(-0.00, 1.00, 0.00)
    fastener_hole.Midplane = True
    fastener_hole.Placement = placemnt
    fastener_hole.Profile = (fastener_profile, [])
    fastener_hole.ReferenceAxis = (fastener_profile, ['N_Axis'])
    fastener_hole.Type = 'ThroughAll'
    fastener_hole.Visibility = False
    fastener_hole.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    fastener_hole.ViewObject.Visibility = False
    Weir.addObject(fastener_hole)
    all_hor_fasteners = doc.addObject('PartDesign::LinearPattern', 'all_hor_fasteners')
    all_hor_fasteners.BaseFeature = fastener_hole
    all_hor_fasteners.Direction = (fastener_profile, ['H_Axis'])
    all_len = 'Computed.WeirHorizontalFastenerHidth'
    all_hor_fasteners.setExpression('Length', all_len)
    all_hor_fasteners.setExpression('Occurrences', 'Config.WeirFastenerHorizontalCount')
    #all_hor_fasteners.Length = 10.0
    all_hor_fasteners.Occurrences = 2
    all_hor_fasteners.Originals = [fastener_hole]
    all_hor_fasteners.Placement = placemnt
    all_hor_fasteners.Visibility = False
    all_hor_fasteners.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_hor_fasteners.ViewObject.Visibility = False
    Weir.addObject(all_hor_fasteners)
    hole_reinforcement = doc.addObject('Sketcher::SketchObject', 'hole_reinforcement')
    geo0 = hole_reinforcement.addGeometry(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 19.00))
    geo1 = hole_reinforcement.addGeometry(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 14.00))
    hole_reinforcement.addConstraint(Sketcher.Constraint('Diameter', geo0, 38.0))
    hole_reinforcement.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo0, 3, 428.50))
    hole_reinforcement.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 112.00))
    hole_reinforcement.addConstraint(Sketcher.Constraint('Coincident', geo1, 3, geo0, 3))
    hole_reinforcement.addConstraint(Sketcher.Constraint('Diameter', geo1, 28.0))
    hole_reinforcement.setExpression('Constraints[0]', 'Config.BulkHeadDiameter+5')
    center_bh = 'Computed.RealGlassHeight-Config.BulkHeadDiameter/2-Config.SidesGlassThickness-Config.WeirSlotWidth*1.5'
    hole_reinforcement.setExpression('Constraints[1]', center_bh)
    hole_reinforcement.setExpression('Constraints[2]', 'Computed.BulkHeadSpace/2+Config.BraceWidth+2*Config.SidesGlassThickness')
    hole_reinforcement.setExpression('Constraints[4]', 'Config.BulkHeadDiameter-5')
    hole_reinforcement.MapMode = 'FlatFace'
    hole_reinforcement.Placement = placemnt
    hole_reinforcement.Visibility = False
    hole_reinforcement.ViewObject.Visibility = False
    Weir.addObject(hole_reinforcement)
    Bulk_Head_Reinforced = doc.addObject('PartDesign::Pad', 'Bulk_Head_Reinforced')
    Bulk_Head_Reinforced.BaseFeature = all_hor_fasteners
    Bulk_Head_Reinforced.Direction = Vector(0.00, -1.00, -0.00)
    Bulk_Head_Reinforced.setExpression('Length', 'Config.WeirWallThickness')
    Bulk_Head_Reinforced.Length = 4.0
    Bulk_Head_Reinforced.Placement = placemnt
    Bulk_Head_Reinforced.Profile = (hole_reinforcement, [])
    Bulk_Head_Reinforced.ReferenceAxis = (hole_reinforcement, ['N_Axis'])
    Bulk_Head_Reinforced.Visibility = False
    Bulk_Head_Reinforced.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    Bulk_Head_Reinforced.ViewObject.Visibility = False
    Weir.addObject(Bulk_Head_Reinforced)
    all_holes_reinforced = doc.addObject('PartDesign::LinearPattern', 'all_holes_reinforced')
    all_holes_reinforced.BaseFeature = Bulk_Head_Reinforced
    all_holes_reinforced.Direction = (hole_reinforcement, ['H_Axis'])
    all_holes_reinforced.setExpression('Length', '(Config.BulkHeadNumber-1)*Computed.BulkHeadSpace')
    all_holes_reinforced.setExpression('Occurrences', 'Config.BulkHeadNumber')
    all_holes_reinforced.Length = 428.57142857142856
    all_holes_reinforced.Occurrences = 6
    all_holes_reinforced.Originals = [Bulk_Head_Reinforced]
    all_holes_reinforced.Placement = placemnt
    all_holes_reinforced.Visibility = False
    all_holes_reinforced.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    all_holes_reinforced.ViewObject.Visibility = False
    Weir.addObject(all_holes_reinforced)
    bulk_head_hole = doc.addObject('Sketcher::SketchObject', 'bulk_head_hole')
    geo0 = bulk_head_hole.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 16.50), 4.742696650350782, 7.823673964008179))
    geo1 = bulk_head_hole.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 15.50), 4.744651624150203, 7.821718990208744))
    geo2 = bulk_head_hole.addGeometry(Part.LineSegment(Vector (112.5, 412.0075774975293, 0.0), Vector (112.5, 413.00757749752927, 0.0)))
    geo3 = bulk_head_hole.addGeometry(Part.LineSegment(Vector (111.5, 444.99242250247073, 0.0), Vector (111.5, 443.99242250247073, 0.0)))
    geo4 = bulk_head_hole.addGeometry(Part.Point(Vector(112.00, 428.50, 0.00)))
    bulk_head_hole.toggleConstruction(geo4)
    geo5 = bulk_head_hole.addGeometry(Part.LineSegment(Vector (112.5, 443.99242250247056, 0.0), Vector (112.5, 444.99242250247056, 0.0)))
    geo6 = bulk_head_hole.addGeometry(Part.LineSegment(Vector (111.49999999999845, 413.0075774975294, 0.0), Vector (111.49999999999845, 412.0075774975294, 0.0)))
    geo7 = bulk_head_hole.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 16.50), 1.601103996761398, 4.682081310418408))
    geo8 = bulk_head_hole.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(112.00, 428.50, 0.00), Vector (0.0, 0.0, 1.0), 15.50), 1.6030589705603855, 4.680126336618976))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Diameter', geo0, 33.0))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Vertical', geo2))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Vertical', geo3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Symmetric', geo3, 1, geo2, 1, geo4, 1))
    bulk_head_hole.addConstraint(Sketcher.Constraint('DistanceX', geo3, 1, geo5, 2, 1.00))
    bulk_head_hole.addConstraint(Sketcher.Constraint('PointOnObject', geo7, 2, geo3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo2, 2, geo1, 1))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo6, 1, geo8, 2))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Equal', geo0, geo7))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo0, 3, geo7, 3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('PointOnObject', geo7, 1, geo3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Equal', geo1, geo8))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo1, 2, geo5, 1))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo8, 1, geo3, 2))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo1, 3, geo8, 3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Vertical', geo5))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Vertical', geo6))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo7, 2, geo6, 2))
    bulk_head_hole.addConstraint(Sketcher.Constraint('DistanceX', geo6, 1, geo1, 1, 1.00))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo0, 1, geo2, 1))
    bulk_head_hole.addConstraint(Sketcher.Constraint('DistanceX', geo0, 3, 112.00))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo5, 2, geo0, 2))
    bulk_head_hole.addConstraint(Sketcher.Constraint('DistanceY', geo5, 1, geo5, 2, 1.00))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo4, 1, geo1, 3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('Coincident', geo1, 3, geo0, 3))
    bulk_head_hole.addConstraint(Sketcher.Constraint('DistanceY', -1, 1, geo4, 1, 428.50))
    bulk_head_hole.setExpression('Constraints[0]', 'Config.BulkHeadDiameter')
    bulk_head_hole.setExpression('Constraints[20]', 'Computed.BulkHeadSpace/2+Config.BraceWidth+2*Config.SidesGlassThickness')
    bulk_head_hole.setExpression('Constraints[25]', center_bh)
    bulk_head_hole.MapMode = 'FlatFace'
    bulk_head_hole.Placement = placemnt
    bulk_head_hole.Visibility = False
    bulk_head_hole.ViewObject.Visibility = False
    Weir.addObject(bulk_head_hole)
    detachable_hole = doc.addObject('PartDesign::Pocket', 'detachable_hole')
    detachable_hole.BaseFeature = all_holes_reinforced
    detachable_hole.Direction = Vector(-0.00, 1.00, 0.00)
    detachable_hole.Midplane = True
    detachable_hole.Placement = placemnt
    detachable_hole.Profile = (bulk_head_hole, [])
    detachable_hole.ReferenceAxis = (bulk_head_hole, ['N_Axis'])
    detachable_hole.Type = 'ThroughAll'
    detachable_hole.Visibility = False
    detachable_hole.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    detachable_hole.ViewObject.Visibility = False
    Weir.addObject(detachable_hole)
    bulk_heads_detachable = doc.addObject('PartDesign::LinearPattern', 'bulk_heads_detachable')
    bulk_heads_detachable.BaseFeature = detachable_hole
    bulk_heads_detachable.Direction = (bulk_head_hole, ['H_Axis'])
    bulk_heads_detachable.setExpression('Length', '(Config.BulkHeadNumber-1)*Computed.BulkHeadSpace')
    bulk_heads_detachable.setExpression('Occurrences', 'Config.BulkHeadNumber')
    bulk_heads_detachable.Length = 428
    bulk_heads_detachable.Occurrences = 6
    bulk_heads_detachable.Originals = [detachable_hole]
    bulk_heads_detachable.Placement = placemnt
    bulk_heads_detachable.Refine = True
    bulk_heads_detachable.ViewObject.ShapeColor = (0.20, 0.20, 0.20, 0.00)
    Weir.addObject(bulk_heads_detachable)
    return Weir
