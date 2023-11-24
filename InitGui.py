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


class AquariumWorkbench (Workbench):
    MenuText = "Aquarium"
    ToolTip = "Aquarium model generator"
    Icon = Icon = '''
/* XPM */
static char * aq_xpm[] = {
"64 64 11 1",
" 	c None",
".	c #244627",
"+	c #34423B",
"@	c #3C593C",
"#	c #5A616A",
"$	c #4D6B4B",
"%	c #767C7F",
"&	c #6D886B",
"*	c #8E9C8E",
"=	c #A3A7A7",
"-	c #A6BAA6",
"                                                                ",
"                                 =%*=                           ",
"                               =*-*-*=                          ",
"                             =*---*---*=                        ",
"                            *-----*-----*=                      ",
"                          =*------*-------*                     ",
"                        =*--------*--------*=                   ",
"                      =*----------*----------*=                 ",
"                     =*-----------*------------*=               ",
"                   =*-------------*--------------*              ",
"                 =*---------------*---------------*=            ",
"                *-----------------*-----------------*=          ",
"              =*------------------*-----------------%+          ",
"            =*--------------------*---------------*$&$          ",
"          =*----------------------*-------------*$&&&$          ",
"         *-----------------------&+%-----------&&&&&&$          ",
"        +*---------------------*@$@$@&-------*$&&&&&&$          ",
"        $&$*-----------------*$$@...@$@*---*$&&&&&&&&$          ",
"        $&&&%---------------&@@..@....@$$*&&&&&&&&&&&$          ",
"        $&&&&$*-----------*@$..@@$..@@..+.@&&&&&&&&&&$          ",
"        $&&&&&&$*-------*@$@....$&@.&$+...@@$&&&&&&&&$          ",
"        $&&&&&&&&&*---*%$@..@@@..@..$@$@....@@$&&&&&&$          ",
"        $&&&&&&&&&&%*&@$..@@&&$@@.+.@$$$$@....@@&&&&&$          ",
"        $&&&&&&&&&&$.+@...@&&&&&$+...@$$$$$....@@@&&&$          ",
"        $&&&&&&&&&@@...+@@..$&&$@@.....$$$$$@....@@$&$          ",
"        $&&&&&&&@@@....@@@@@.++$$$......@$$$$$@....@@@          ",
"        $&&&&&$@@.....$$$@@@+...$$..$@....@$$$$$.....+          ",
"        $&&&$@@........@$$$@$.......$$$@....@$$$$@..++          ",
"        $&&@@....@$$@....@$@$$@.....$$$$$@....$$$@++##          ",
"        @@@@....@$$$$$.....@$$$$@....@$$$$$.....++####          ",
"        +.........@$$$$@....@$$$$$.....$$$$$@.++###%##          ",
"        ++..@$$@....$$$$$@....@$$$......@$$$@++##=  ##          ",
"        ##++@$$$$....@$$$$$.....$@..$@.....++##%=   ##          ",
"        ####++@$$$@....@$$$@$........$$@.++###=     ##          ",
"        ##%##++@$$$$@....$$@$$.........++###=       ##          ",
"        ## =%##++@$$$$....@@@.........++##%         ##          ",
"        ##   =###++@$$$@........@$..++####=         ##          ",
"        ##     =##+++@$$$.........++###%###%        ##          ",
"        ##       %##++@@........++###=   %###=      ##          ",
"        ##        =%##++...@$..++####     =%###=    ##          ",
"        ##          ####++...++##%%###=     =###%   ##          ",
"        ##        =#######+++###=  =%###=     =###==##          ",
"        ##      =%###%  %##+###%     =###%=     %#####          ",
"        ##     %######%= =##%%###=     =###%     =%###          ",
"        ##   =###=  =###%=##  =%###=     %###=    =###          ",
"        ## =####=     %#####    =###%     =%###= %####          ",
"        #########%     =%###=     =###=     =######%##          ",
"        ####=  %###=     =###%      %###=    =###%  %#          ",
"        ###=    =%###=    #####=     =###%==%##%=               ",
"        ####=     =###%=  ##=%###=     =######=                 ",
"        ######=     =###%=##  =%###=    %###=                   ",
"        ## =%##%=     %#####    =###% =###%=                    ",
"        =#   =###%     =%###=     =######=                      ",
"               %###=     =###%     ####=                        ",
"                =%###=    #####= =###%                          ",
"                  =###%=  ##=%#####%=                           ",
"                    =###%=## =####=                             ",
"                      %#####%###=                               ",
"                       =%#####%                                 ",
"                         =###=                                  ",
"                          ##                                    ",
"                          ##                                    ",
"                          %#                                    ",
"                                                                "};
'''

    def Initialize(self):
        import configureGui
        configureGui.RegisterCommands()
        self.appendMenu("Aquarium Configuration", configureGui.AllCommands())
        import generateGui
        generateGui.RegisterCommands()
        self.appendMenu("Aquarium Generation", generateGui.AllCommands())
        self.appendMenu("Blue Print Generation", generateGui.AllBluePrintCommands())

    def Activated(self):
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        pass

    def GetClassName(self): 
        return "Gui::PythonWorkbench"


Gui.addWorkbench(AquariumWorkbench())
