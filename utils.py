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
from FreeCAD import Vector, Placement, Rotation
import Part, Draft
import FreeCAD as App

def glass_color(obj):
    obj.ViewObject.ShapeColor=(0.0, 1/3, 0.0)
    obj.ViewObject.Transparency=80
    return obj

def make_panel(doc, grp, name, px, py, pz, l, w, h):
    g = doc.addObject('Part::Box', name)
    g.setExpression('.Placement.Base.x', px)
    g.setExpression('.Placement.Base.y', py)
    g.setExpression('.Placement.Base.z', pz)
    g.setExpression('Length', l)
    g.setExpression('Width', w)
    g.setExpression('Height', h)
    glass_color(g)
    if grp:
        grp.addObject(g)
    return g

def make_fastener(doc, baseOrPanel, grp, name, x, y, direction, upcorner=False):
    if direction==0:
        y+='+Config.PanelMountInset'
    elif direction==1:
        x+='-Config.PanelMountInset'
    elif direction==2:
        y+='-Config.PanelMountInset'
    elif direction==3:
        x+='+Config.PanelMountInset'
    elif direction==4:
        y+='-Config.PanelMountInset'
    elif direction==5:
        x+='+Config.PanelMountInset'
    elif direction==6:
        y+='+Config.PanelMountInset'
    else:
        x+='-Config.PanelMountInset'
    direction = direction % 4
    base = doc.addObject('App::Part', name)
    if direction==0:
        x+='+Config.MetalProfileWidth'
    elif direction==1:
        y+='+Config.MetalProfileHeight'
    elif direction==2:
        x+='-Config.MetalProfileWidth'
    else:
        y+='-Config.MetalProfileHeight'
    if upcorner:
        z = 'Computed.ColumnsSizeHeight-Computed.PanelFastenerSizeVertical'
        edge = 8
    else:
        z= 'Computed.SumpBeamsLevel+Config.MetalProfileWidth/2'
        edge = 6
    calcX = grp.evalExpression(x)
    calcY = grp.evalExpression(y)
    calcZ = grp.evalExpression(z)
    pos = Vector(calcX, calcY, calcZ)
    angle = direction*90
    rot = Rotation(angle, 0, 0)
    halfThick = grp.evalExpression('Config.PanelMountThickness') / 2
    pivot = Vector(0, halfThick, 0)
    base.Placement = Placement(pos, rot, pivot)
    base.setExpression('.Placement.Base.x', x)
    base.setExpression('.Placement.Base.y', y)
    base.setExpression('.Placement.Base.z', z)
    grp.addObject(base)
    if baseOrPanel:
        b = doc.addObject('Part::Box', f'{name}Square')
        b.setExpression('Length', 'Computed.PanelFastenerSizeHorizontal')
        b.setExpression('Width', 'Config.PanelBlockThickness')
        b.setExpression('Height', 'Computed.PanelFastenerSizeVertical')
        b.Visibility = False
        grp.addObject(b)
        chamfsize = 10
        edges = list(map(lambda x: (x, chamfsize, chamfsize), [6, 8]))
        c = doc.addObject('Part::Chamfer', f'{name}Chamfered')
        c.Base = b
        c.Edges = edges
        grp.addObject(c)
    else:
        b = doc.addObject('Part::Box', f'{name}Square')
        b.setExpression('Length', 'Computed.PanelFastenerSizeHorizontal')
        b.setExpression('Width', 'Config.PanelMountThickness')
        b.setExpression('Height', 'Computed.PanelFastenerSizeVertical')
        b.Visibility = False
        grp.addObject(b)
        chamfsize = 10
        edges = [(edge, chamfsize, chamfsize)]
        c = doc.addObject('Part::Chamfer', f'{name}Chamfered')
        c.Base = b
        c.Edges = edges
        grp.addObject(c)
        c.Visibility = False
        hole = doc.addObject('Part::Cylinder', f'{name}IndexHole')
        #holes = doc.addObject('App::Part', f'{name}Holes')
        holerot = Rotation(Vector(1,0,0), 90)
        holecenter = hole.Placement.Base
        hole.Placement = Placement(holecenter, holerot)
        hole.setExpression('.Placement.Base.x', 'Config.PanelMountHoleBorderSpacing')
        hole.setExpression('.Placement.Base.y', '2 * Config.PanelMountThickness')
        hole.setExpression('.Placement.Base.z', 'Config.PanelMountHoleBorderSpacing')
        hole.setExpression('Radius', 'Config.PanelMountHoleDiameter/2')
        hole.setExpression('Height', 'Config.PanelMountThickness*3')
        grp.addObject(hole)
        holes = Draft.make_ortho_array(hole, v_x=App.Vector(10, 0, 0), v_y=App.Vector(0, 10, 0), v_z=App.Vector(0, 0, 10), n_x=1, n_y=1, n_z=1, use_link=False)
        holes.setExpression('.IntervalX.x', 'Config.PanelMountHoleSpacing')
        holes.setExpression('.IntervalZ.z', 'Config.PanelMountHoleSpacing')
        holes.setExpression('NumberZ', 'Config.PanelMountHoleCountVertical')
        holes.setExpression('NumberX', 'Config.PanelMountHoleCountHorizontal')
        holes.Visibility = False
        grp.addObject(holes)
        drilled = doc.addObject("Part::Cut", f'{name}Drilled')
        drilled.Base = c
        drilled.Tool = holes
        grp.addObject(drilled)
        base.Group = [ drilled ]
    return base

def make_fasteners(doc, baseOrPanel, grp, name, x, y, direction):
    make_fastener(doc, baseOrPanel, grp, f'{name}{direction}Top', x, y, direction, True)
    make_fastener(doc, baseOrPanel, grp, f'{name}{direction}Bottom', x, y, direction, False)

def make_supports(doc, baseOrPanel, grp_sup, name):
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.LeftCornerX', 'Computed.FrontCornerY', 0)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.RightCornerX', 'Computed.FrontCornerY', 1)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.RightCornerX', 'Computed.BackCornerY', 2)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.LeftCornerX', 'Computed.BackCornerY', 3)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.LeftCornerX', 'Computed.BackCornerY-Config.PanelMountThickness', 4)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.LeftCornerX+Config.PanelMountThickness', 'Computed.FrontCornerY', 5)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.RightCornerX', 'Computed.FrontCornerY+Config.PanelMountThickness', 6)
    make_fasteners(doc, baseOrPanel, grp_sup, name, 'Computed.RightCornerX-Config.PanelMountThickness', 'Computed.BackCornerY', 7)

