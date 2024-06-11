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

def make_glass(doc):
    grp = doc.addObject('App::DocumentObjectGroup','Glasses')
    grp_bp = doc.addObject('App::DocumentObjectGroup','BottomGlass')
    grp.addObject(grp_bp)
    grp.Label = 'Glasses'
    bg = make_panel(doc, None, 'BottomGlass','Computed.LeftCornerX','-Computed.Length/2','Computed.GlassLevel','Computed.Width','Computed.Length','Config.BottomGlassThickness')
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
    make_panel(doc, grp_gs, 'LeftGlass','Computed.LeftCornerX','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Config.SidesGlassThickness','Computed.Length-2*(Config.SidesGlassThickness++Config.JunctionThickness)','Computed.RealGlassHeight-Config.JunctionThickness')
    make_panel(doc, grp_gs, 'RightGlass','Computed.RightCornerX-Config.SidesGlassThickness','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Config.SidesGlassThickness','Computed.Length-2*(Config.SidesGlassThickness++Config.JunctionThickness)','Computed.RealGlassHeight-Config.JunctionThickness')
    make_panel(doc, grp_gs, 'BackGlass','Computed.LeftCornerX','Computed.Length/2-Config.SidesGlassThickness', z_b+'+Config.JunctionThickness', 'Computed.Width','Config.SidesGlassThickness','Computed.RealGlassHeight-Config.JunctionThickness')
    make_panel(doc, grp_gs, 'FrontGlass','Computed.LeftCornerX','-Computed.Length/2', z_b+'+Config.JunctionThickness', 'Computed.Width','Config.SidesGlassThickness','Computed.RealGlassHeight-Config.JunctionThickness')

    # Euro bracing
    eb = doc.addObject('App::DocumentObjectGroup','GlassBraces')
    eb.Label = 'EuroBraces'
    grp.addObject(eb)
    ebb = doc.addObject('App::DocumentObjectGroup','GlassBracesBottom')
    ebb.Label = 'EuroBraces Bottom'
    eb.addObject(ebb)
    make_panel(doc, ebb, 'LeftBottomBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.JunctionThickness','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Config.BraceWidth-2*Config.JunctionThickness','Computed.Length-2*(Config.SidesGlassThickness+Config.JunctionThickness)','Config.SidesGlassThickness')
    make_panel(doc, ebb, 'RightBottomBrace','Computed.RightCornerX-Config.BraceWidth-Config.SidesGlassThickness+Config.JunctionThickness','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Config.BraceWidth-2*Config.JunctionThickness','Computed.Length-2*(Config.SidesGlassThickness+Config.JunctionThickness)','Config.SidesGlassThickness')
    make_panel(doc, ebb, 'FrontBottomBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.BraceWidth','-Computed.Length/2+Config.SidesGlassThickness+Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Computed.Width-2*Config.BraceWidth-2*Config.SidesGlassThickness','Config.BraceWidth-Config.JunctionThickness','Config.SidesGlassThickness')
    bbb = make_panel(doc, ebb, 'BackBottomBrace','Computed.LeftCornerX+2*Config.SidesGlassThickness+Config.BraceWidth+Config.JunctionThickness','Computed.Length/2-2*Config.SidesGlassThickness-Config.JunctionThickness', z_b+'+Config.JunctionThickness', 'Computed.Width-2*(Config.BraceWidth+Config.JunctionThickness)-4*Config.SidesGlassThickness','Config.SidesGlassThickness','Config.BraceWidth')
    bbbsup = make_panel(doc, ebb, 'BackBottomWeirSupport','Computed.LeftCornerX+2*Config.SidesGlassThickness+Config.BraceWidth+Config.JunctionThickness','Computed.Length/2-Config.SidesGlassThickness-Computed.WeirDepth', z_b+'+Config.JunctionThickness', 'Computed.Width-2*(Config.BraceWidth+Config.JunctionThickness)-4*Config.SidesGlassThickness','Config.SidesGlassThickness','Config.BraceWidth')

    ebt = doc.addObject('App::DocumentObjectGroup','GlassBracesTop')
    ebt.Label = 'EuroBraces Top'
    eb.addObject(ebt)
    top = z_t+'- Config.SidesGlassThickness'
    make_panel(doc, ebt, 'LeftTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.JunctionThickness','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness+Config.BraceWidth', top, 'Config.BraceWidth-2*Config.JunctionThickness','Computed.Length-2*(Config.SidesGlassThickness+Config.JunctionThickness)-Computed.WeirDepth-Config.BraceWidth','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'RightTopBrace','Computed.RightCornerX-Config.BraceWidth-Config.SidesGlassThickness+Config.JunctionThickness','Computed.Length/-2+Config.SidesGlassThickness+Config.JunctionThickness+Config.BraceWidth', top, 'Config.BraceWidth-2*Config.JunctionThickness','Computed.Length-2*(Config.SidesGlassThickness+Config.JunctionThickness)-Computed.WeirDepth-Config.BraceWidth','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'FrontTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.JunctionThickness','-Computed.Length/2+Config.SidesGlassThickness+Config.JunctionThickness', top, 'Computed.Width-2*(Config.SidesGlassThickness+Config.JunctionThickness)','Config.BraceWidth-Config.JunctionThickness','Config.SidesGlassThickness')
    make_panel(doc, ebt, 'BackTopBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.JunctionThickness','Computed.Length/2-Config.SidesGlassThickness-Computed.WeirDepth', top, 'Computed.Width-2*(Config.SidesGlassThickness+Config.JunctionThickness)','Computed.WeirDepth-Config.JunctionThickness','Config.SidesGlassThickness')
    gwf = doc.addObject('App::DocumentObjectGroup','GlassBracesWeirFrame')
    gwf.Label = 'Weir Frame'
    eb.addObject(gwf)
    make_panel(doc, gwf, 'WeirFrameLeftBrace','Computed.LeftCornerX+Config.SidesGlassThickness+Config.BraceWidth','Computed.Length/2-Config.SidesGlassThickness -Computed.WeirDepth', z_b+'+Config.JunctionThickness','Config.SidesGlassThickness','Computed.WeirDepth-Config.JunctionThickness','Computed.RealGlassHeight-Config.SidesGlassThickness-2*Config.JunctionThickness')
    make_panel(doc, gwf, 'WeirFrameRightBrace','Computed.RightCornerX-2*Config.SidesGlassThickness-Config.BraceWidth','Computed.Length/2-Config.SidesGlassThickness-Computed.WeirDepth', z_b+'+Config.JunctionThickness','Config.SidesGlassThickness','Computed.WeirDepth-Config.JunctionThickness','Computed.RealGlassHeight-Config.SidesGlassThickness-2*Config.JunctionThickness')
    return grp
