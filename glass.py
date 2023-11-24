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

def cut_box(panel, name, origin_x, origin_y, origin_z, length, height, rot):
    cut = App.ActiveDocument.addObject("Part::Box","CutTool")
    cut.setExpression('.Placement.Base.x', origin_x)
    cut.setExpression('.Placement.Base.y', origin_y)
    cut.setExpression('.Placement.Base.z', origin_z)
    cut.setExpression('Width', height)
    cut.setExpression('Length', f'{length}/sqrt(2)')
    cut.setExpression('Height', f'{length}/sqrt(2)')
    cut.Placement.Rotation=Rotation(rot,0,90)
    s_cut = App.ActiveDocument.addObject("Part::MultiCommon",f"cut45{name}")
    s_cut.Shapes = [panel,cut]
    return s_cut;

def cut_glass(panel, name, origin_x, origin_y, origin_z, length, rot):
    cg = cut_box(panel, name, origin_x, origin_y, origin_z, length, 'Computed.RealGlassHeight', rot)
    glass_color(cg)
    return cg

def make_glass(doc, cut45 = False):
    grp = doc.addObject('App::DocumentObjectGroup','Glasses')
    grp_bp = doc.addObject('App::DocumentObjectGroup','BottomGlass')
    grp.addObject(grp_bp)
    grp.Label = 'Glasses'
    bg = make_panel(doc, None, 'BottomGlass','Computed.LeftCornerX','-Config.Length/2','Computed.GlassLevel','Config.Width','Config.Length','Config.BottomGlassThickness')
    bbd = doc.addObject("Part::Cut", "BottomGlassDrilled")
    bbd.Base = bg
    holes_glass = getHole(doc, 'Glass')
    bbd.Tool = holes_glass
    glass_color(bbd)
    grp.removeObject(bg)
    grp_bp.addObject(bbd)

    z_b = 'Computed.GlassLevel+Config.BottomGlassThickness'
    z_t = z_b+'+Computed.RealGlassHeight'
    grp_gs = doc.addObject('App::DocumentObjectGroup','SidesGlass')
    grp.addObject(grp_gs)
    if cut45:
        left = make_panel(doc, None, 'LeftGlass','Computed.LeftCornerX','Config.Length/-2', z_b, 'Config.SidesGlassThickness','Config.Length','Computed.RealGlassHeight')
        grp_gs.addObject(cut_glass(left, 'LeftGlass', 'Computed.LeftCornerX','Config.Length/2', z_b, 'Config.Length', -45))
        right = make_panel(doc, None, 'RightGlass','Computed.RightCornerX-Config.SidesGlassThickness','Config.Length/-2', z_b, 'Config.SidesGlassThickness','Config.Length','Computed.RealGlassHeight')
        grp_gs.addObject(cut_glass(right, 'RightGlass', 'Computed.RightCornerX','Config.Length/2', z_b, 'Config.Length', -45))
        back = make_panel(doc, None, 'BackGlass','Computed.LeftCornerX','Config.Length/2-Config.SidesGlassThickness', z_b, 'Config.Width','Config.SidesGlassThickness','Computed.RealGlassHeight')
        grp_gs.addObject(cut_glass(back, 'BackGlass', 'Computed.LeftCornerX','Config.Length/2', z_b, 'Config.Width', 45))
        front = make_panel(doc, None, 'FrontGlass','Computed.LeftCornerX','-Config.Length/2', z_b, 'Config.Width','Config.SidesGlassThickness','Computed.RealGlassHeight')
        grp_gs.addObject(cut_glass(front, 'FrontGlass', 'Computed.LeftCornerX','-Config.Length/2', z_b, 'Config.Width', 45))
    else:
        make_panel(doc, grp_gs, 'LeftGlass','Computed.LeftCornerX','Config.Length/-2+Config.SidesGlassThickness', z_b, 'Config.SidesGlassThickness','Config.Length-2*Config.SidesGlassThickness','Computed.RealGlassHeight')
        make_panel(doc, grp_gs, 'RightGlass','Computed.RightCornerX-Config.SidesGlassThickness','Config.Length/-2+Config.SidesGlassThickness', z_b, 'Config.SidesGlassThickness','Config.Length-2*Config.SidesGlassThickness','Computed.RealGlassHeight')
        make_panel(doc, grp_gs, 'BackGlass','Computed.LeftCornerX','Config.Length/2-Config.SidesGlassThickness', z_b, 'Config.Width','Config.SidesGlassThickness','Computed.RealGlassHeight')
        make_panel(doc, grp_gs, 'FrontGlass','Computed.LeftCornerX','-Config.Length/2', z_b, 'Config.Width','Config.SidesGlassThickness','Computed.RealGlassHeight')

    # Euro bracing
    eb = doc.addObject('App::DocumentObjectGroup','GlassBraces')
    eb.Label = 'EuroBraces'
    grp.addObject(eb)
    ebb = doc.addObject('App::DocumentObjectGroup','GlassBracesBottom')
    ebb.Label = 'EuroBraces Bottom'
    eb.addObject(ebb)
    make_panel(doc, ebb, 'LeftBottomBrace','Computed.LeftCornerX+Config.SidesGlassThickness','Config.Length/-2+Config.SidesGlassThickness', z_b, 'Config.BraceWidth','Config.Length-2*Config.SidesGlassThickness','Config.SidesGlassThickness')
    make_panel(doc, ebb, 'RightBottomBrace','Computed.RightCornerX-Config.BraceWidth-Config.SidesGlassThickness','Config.Length/-2+Config.SidesGlassThickness', z_b, 'Config.BraceWidth','Config.Length-2*Config.SidesGlassThickness','Config.SidesGlassThickness')
    make_panel(doc, ebb, 'FrontBottomBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.BraceWidth','-Config.Length/2+Config.SidesGlassThickness', z_b, 'Config.Width-2*Config.BraceWidth-2*Config.SidesGlassThickness','Config.BraceWidth','Config.SidesGlassThickness')
    bbb = make_panel(doc, ebb, 'BackBottomBrace','Computed.LeftCornerX+2*Config.SidesGlassThickness+Config.BraceWidth','Config.Length/2-2*Config.SidesGlassThickness', z_b, 'Config.Width-2*Config.BraceWidth-4*Config.SidesGlassThickness','Config.SidesGlassThickness','Config.BraceWidth')
    bbbsup = make_panel(doc, ebb, 'BackBottomWeirSupport','Computed.LeftCornerX+2*Config.SidesGlassThickness+Config.BraceWidth','Config.Length/2-Config.SidesGlassThickness-Computed.WeirDepth', z_b, 'Config.Width-2*Config.BraceWidth-4*Config.SidesGlassThickness','Config.SidesGlassThickness','Config.BraceWidth')

    ebt = doc.addObject('App::DocumentObjectGroup','GlassBracesTop')
    ebt.Label = 'EuroBraces Top'
    eb.addObject(ebt)
    top_1 = z_t+'- Config.SidesGlassThickness'
    top_2 = z_t+'- 2*Config.SidesGlassThickness'
    make_panel(doc, ebt, 'LeftTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness','Config.Length/-2+Config.SidesGlassThickness', top_2, 'Config.BraceWidth','Config.Length-2*Config.SidesGlassThickness','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'RightTopBrace','Computed.RightCornerX-Config.BraceWidth-Config.SidesGlassThickness','Config.Length/-2+Config.SidesGlassThickness', top_2, 'Config.BraceWidth','Config.Length-2*Config.SidesGlassThickness','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'FrontTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness','-Config.Length/2+Config.SidesGlassThickness', top_1, 'Config.Width-2*Config.SidesGlassThickness','Config.BraceWidth','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'BackTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness','Config.Length/2-Config.SidesGlassThickness -Computed.WeirDepth', top_1, 'Config.Width-2*Config.SidesGlassThickness','Computed.WeirDepth','Config.SidesGlassThickness')
    gwf = doc.addObject('App::DocumentObjectGroup','GlassBracesWeirFrame')
    gwf.Label = 'Weir Frame'
    eb.addObject(gwf)
    make_panel(doc, gwf, 'WeirFrameLeftBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.BraceWidth','Config.Length/2-Config.SidesGlassThickness -Computed.WeirDepth', z_b,'Config.SidesGlassThickness','Computed.WeirDepth','Computed.RealGlassHeight-Config.SidesGlassThickness')
    make_panel(doc, gwf, 'WeirFrameRightBrace','Computed.RightCornerX-2*Config.SidesGlassThickness-Config.BraceWidth','Config.Length/2-Config.SidesGlassThickness -Computed.WeirDepth', z_b,'Config.SidesGlassThickness','Computed.WeirDepth','Computed.RealGlassHeight-Config.SidesGlassThickness')
    return grp
