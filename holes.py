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

def getHole(doc, type):
    name=f'Holes{type}'
    o = doc.getObject(name)
    if o == None:
        o = doc.addObject("Part::Cut", name)
        o.Base = doc.addObject('App::Part', f'{name}Base')
        o.Base.setExpression('.Placement.Base.z', '0 m')
        o.Tool = doc.addObject('App::Part',f'{name}Exclusion')
        mock_hole = doc.addObject("Part::Box","MockHole")
        mock_hole.setExpression('.Placement.Base.z', '-1.1 m')
        o.Base.Group = mock_hole
        mock_excl = doc.addObject("Part::Box","MockExcl")
        mock_excl.setExpression('.Placement.Base.z', '-1.101 m')
        o.Tool.Group = mock_excl
        o.Visibility = False
    return o
