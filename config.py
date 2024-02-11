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

# import FreeCAD as App
from collections.abc import MutableMapping, Iterator


class InvalidConfigException(Exception):

    def __init__(self, val):
        Exception(self, val)


class ConfigValue():

    def __init__(self, name, descr):
        if not isinstance(name, str):
            raise InvalidConfigException('name')
        if not isinstance(descr, str):
            raise InvalidConfigException('descr')
        self.name = name
        self.descr = descr


class ConfigValueBool(ConfigValue):

    def __init__(self, name, descr, default):
        super().__init__(name, descr)
        if not isinstance(default, bool):
            raise InvalidConfigException('default should be bool')
        self.default = default


class ConfigValueNumeric(ConfigValue):

    def __init__(self, name, descr, default, min, max, step, type=None, unit=None):
        super().__init__(name, descr)
 
        def check_num(v, desc):
            if not isinstance(v, int) and not isinstance(v, float):
                raise InvalidConfigException(desc)

        check_num(default, 'default should be numeric')
        check_num(min, 'min')
        check_num(max, 'max')
        check_num(step, 'step')
        self.default = default
        self.min = min
        self.max = max
        self.step = step
        if not isinstance(type, str):
            self.type = 'Config'
        else:
            self.type = type
        self.unit = unit

    
class ConfigRepository(MutableMapping):

    def __init__(self, doc, name):
        self.__name = name
        self.__sheet = doc.getObject(name)
        if self.__sheet == None:
            # print(f"Adding sheel {name}")
            self.__sheet = doc.addObject('Spreadsheet::Sheet', name)
            
    def recompute(self):
        self.__sheet.recompute()

    def getCellAlias(self, cell):
        return self.__sheet.getAlias(cell)

    def getCell(self, cell):
        return self.__sheet.getContents(cell)

    def __getitem__(self, key):
        cell = self.__sheet.getCellFromAlias(key)
        if cell is None:
            raise KeyError(key)
        return self.__sheet.get(cell)

    def __setitem__(self, key, value):
        cell = self.__sheet.getCellFromAlias(key)
        if cell is None:
            line = self.__allocate_cell()
            cell = f'A{line}'
            self.__sheet.setAlias(cell, key)
        self.__sheet.set(cell, str(value))

    def __delitem__(self, key):
        cell = self.__sheet.getCellFromAlias(key)
        if cell is None:
            return
        self.__sheet.clear(cell)

    def __allocate_cell(self):
        index = 1
        while '' != self.getCell(f'A{index}'):
            index += 1
        return index

    def __len__(self):
        return len(self.__sheet.getUsedCells())
    
    def __iter__(self):

        class IterConfigRepository(Iterator):

            def __init__(self, cr, used):
                self.__index = 0
                self.__conf = cr
                self.__used = used

            def __next__(self):
                try:
                    if self.__index > len(self.__used):
                        raise StopIteration
                    cell = self.__used[self.__index]
                    val = self.__conf.getCellAlias(cell)
                except:
                    raise StopIteration
                self.__index += 1
                return val

        usedCells = self.__sheet.getUsedCells()
        return IterConfigRepository(self, usedCells)


class ConfDefs(dict):

    def __init__(self, type, category):
        self.__type = type
        self.__category = category

    def setCat(self, name, *cat):
        for c in cat:
            try:
                self.__category[c].append((self.__type, name))
            except KeyError:
                self.__category[c] = [(self.__type, name)]

    def addNum(self, name, default, min, max, step, descr, unit, *cat):
        self.setCat(name, *cat)
        return dict.__setitem__(self, name, ConfigValueNumeric(name, descr, default, min, max, step, self.__type, unit))

    def addBool(self, name, default, descr):
        self.setCat(name, *cat)
        return dict.__setitem__(self, name, ConfigValueBool(name, descr, default))

    def type(self):
        return self.__type


def DefaultsConfig(categories):
    defcon = ConfDefs('Config', categories)
    mm = 'mm'
    num = None
    defcon.addNum('Width', 1200, 20, 5000, 10, 'External width of aquarium', mm, 'structure', 'visual')
    defcon.addNum('Length', 580, 20, 5000, 10, 'External length of aquarium', mm, 'structure', 'visual')
    defcon.addNum('VisibleHeightGlass', 600, 20, 2000, 10, 'View Height of the glass', mm, 'structure', 'visual')
    defcon.addNum('StandVisibleHeight', 800, 500, 1500, 10, 'Height from the floor to the visible part of the aquarium', mm, 'structure', 'visual')
    defcon.addNum('Sump2FloorSpaceForBroom', 100, 0, 500, 10, 'Space free from bottom part of sump to floor', mm, 'structure')
    defcon.addNum('Panel2FloorSpace', 5, 0, 100, 1, 'Space free from cover of stand to floor', mm, 'visual', 'structure')
    defcon.addNum('BeamsStandCount', 5, 0, 10, 1, 'Number of beans in the middle of the stand', num, 'structure', 'plumbing')
    defcon.addNum('BeamsSumpCount', 5, 0, 10, 1, 'Number of beans in the middle of the sump', num, 'structure')
    defcon.addNum('PanelMountHoleSpacing', 30, 10, 50, 1, 'Spacing between center of holes used to fasten panels or doors into the structure', mm, 'structure')
    defcon.addNum('PanelMountHoleBorderSpacing', 10, 10, 50, 1, 'Spacing between holes used to fasten panels or doors into the structure and border/structure', mm, 'structure')
    defcon.addNum('PanelMountHoleDiameter', 5, 2, 10, 1, 'Diameter of holes used to fasten panels or doors into the structure', mm, 'structure')
    defcon.addNum('PanelMountHoleCountVertical', 2, 1, 6, 1, 'Number of vertical holes used to fasten panels or doors into the structure', num, 'structure')
    defcon.addNum('PanelMountHoleCountHorizontal', 2, 1, 6, 1, 'Number of horizontal holes used to fasten panels or doors into the structure', num, 'structure')
    defcon.addNum('PanelMountThickness', 3, 1, 6, 1, 'Thickness of support used to fasten panels or doors into the structure', mm, 'structure')
    defcon.addNum('PanelBlockThickness', 5, 5, 30, 1, 'Thickness of block glued inside the panels with screws to fix to the structure', mm, 'structure')
    defcon.addNum('PanelMountInset', 10, 0, 30, 1, 'Space between support and face of panel', mm, 'structure')
    defcon.addNum('SidesGlassThickness', 12, 2, 30, 1, 'Thickness of the glass panels from the side', mm, 'structure', 'glass')
    defcon.addNum('BottomGlassThickness', 19, 2, 30, 1, 'Thickness of the bottom glass', mm, 'structure', 'glass')
    defcon.addNum('BraceWidth', 50, 30, 100, 1, 'Size of bracing', mm, 'structure', 'glass')
    defcon.addNum('UnderGlassLevelingBaseThickness', 25, 1, 50, 1, 'Thickness of the base that support the weight of the aquarium', mm, 'structure', 'plumbing')
    defcon.addNum('HideExtraTop', 30, 0, 50, 1, 'Space to overlap panels to glass and try to hide euro braces and the water level', mm, 'visual')
    defcon.addNum('HideExtraBottom', 10, 0, 20, 1, 'Space to overlap panels to glass and hide bottom of euro braces and sand', mm, 'visual')
    defcon.addNum('WeirWallThickness', 4, 1, 10, 1, 'Thickness of the weir panel', mm, 'weir')
    defcon.addNum('WeirSlotWidth', 3, 1, 10, 1, 'Size of the slot in the weir that lets water in and keep snail out', mm, 'weir')
    defcon.addNum('WaterHeightWeir', 600, 20, 2000, 10, 'Level of water inside weir when pumps are working', mm, 'weir')
    defcon.addNum('BulkHeadDiameter', 33, 4, 300, 1, 'Diameter of the bulk head hole', mm, 'plumbing')
    defcon.addNum('BulkHeadNumber', 6, 2, 10, 1, 'Number of buld heads in weir', num, 'weir', 'plumbing')
    defcon.addNum('BeanAnimalMainDrainLevel', 450, 20, 2000, 10, 'Water level of the main pipe from Bean Animal style drain', mm, 'weir', 'plumbing')
    defcon.addNum('BeanAnimalAuxiliaryDrainLevel', 580, 20, 2000, 10, 'Level in the weir that water start to flow into the auxiliary pipe from Bean Animal style drain', mm, 'weir', 'plumbing')
    defcon.addNum('BeanAnimalEmergencyDrainLevel', 600, 20, 2000, 10, 'Level in the weir that water start to flow into the emergency pipe from Bean Animal style drain', mm, 'weir', 'plumbing')
    defcon.addNum('ReturnWaterLevel', 390, 20, 2000, 10, 'Level in the weir that the return line keeps water in order to avoid siphoning the aquarium water to the sump when the pump is off', mm, 'weir', 'plumbing')
    defcon.addNum('NozzlesEveryXBeamSpace', 1, 1, 10, 1, 'Put a nozzle every number of spaces (1->each beam space, 2->one nozzle one empty space, 3->one nozzle two spaces,...)', num, 'plumbing')
    defcon.addNum('NozzlesSkipBefore', 0, 0, 10, 1, 'Number of spaces between beams to skip before start distribution of nozzles', num, 'plumbing')
    defcon.addNum('NozzlesSkipAfter', 0, 0, 10, 1, 'Number of spaces between beams to keep clean of nozzles after distribution', num, 'plumbing')
    defcon.addNum('NozzlesRows', 1, 0, 6, 1, 'Number of rows of nozzels', num, 'plumbing')
    defcon.addNum('MetalProfileWidth', 60, 20, 200, 1, 'Width of profile (metal structure, external size, bigger dimension)', mm, 'structure')
    defcon.addNum('MetalProfileHeight', 30, 20, 200, 1, 'Height of profile (metal structure, external size, smaller dimension)', mm, 'structure')
    defcon.addNum('MetalProfileWallThickness', 3, 1, 20, 1, 'Thickness of profile wall (metal structure)', mm, 'structure')
    defcon.addNum('CanopyHeight', 200, 100, 600, 1, 'Height of canopy', mm, 'canopy')
    defcon.addNum('CanopyProfileWidth', 20, 5, 100, 1, 'Width of profile cross section', mm, 'canopy')
    defcon.addNum('CanopyProfileHeight', 20, 5, 100, 1, 'Width of profile cross section', mm, 'canopy')
    defcon.addNum('CanopyBeams2Top', 100, 0, 100, 1, 'Free space from top of canopy column to top of beams (slightly smaller than groove space)', mm, 'canopy')
    defcon.addNum('CanopyExtraBeams', 2, 0, 10, 1, 'Number of beams to hang lights and other stuff, zero to disable', num, 'canopy')
    defcon.addNum('PanelThickness', 15, 1, 30, 1, 'Thickness of external panel', mm, 'structure')
    return defcon


def DefaultsPipesDrain(categories):
    mm = 'mm'
    drain = ConfDefs('ConfigPipesDrain', categories)
    drain.addNum('PipeDiameter', 33, 5, 100, 1, 'External diameter of the drain pipe', mm, 'plumbing')
    drain.addNum('PipeThickness', 3.2, .1, 5, .1, 'Wall thickness of the drain pipe', mm, 'plumbing')
    drain.addNum('FlangeDiameter', 45, 5, 200, 1, 'External diameter of the drain pipe', mm, 'plumbing')
    drain.addNum('FlangeFreeHeightTop', 21, 0, 200, 1, 'Height to keep free for the drain flange, top side', mm, 'plumbing')
    drain.addNum('FlangeFreeDiameterTop', 90, 5, 200, 1, 'Diameter to keep free for the drain flange, top side', mm, 'plumbing')
    drain.addNum('FlangeFreeHeightBottom', 21, 0, 200, 1, 'Height to keep free for the drain flange, bottom side', mm, 'plumbing')
    drain.addNum('FlangeFreeDiameterBottom', 80, 5, 200, 1, 'Diameter to keep free for the drain flange, bottom side', mm, 'plumbing')
    drain.addNum('FlangePipeLengthInside', 22, 0, 100, 1, 'Length that the pipe bury inside the flange', mm, 'plumbing')
    return drain


def DefautsPipesReturn(categories):
    mm = 'mm'
    dpr = ConfDefs('ConfigPipesReturn', categories)
    dpr.addNum('PipeDiameter', 33, 5, 100, 1, 'External diameter of the return pipe', mm, 'plumbing')
    dpr.addNum('PipeThickness', 3.2, .1, 5, .1, 'Wall thickness of the return pipe', mm, 'plumbing')
    dpr.addNum('FlangeDiameter', 45, 5, 100, 1, 'External diameter of the drain pipe', mm, 'plumbing')
    dpr.addNum('FlangeFreeHeightTop', 21, 0, 200, 1, 'Height to keep free for the return flange, top side', mm, 'plumbing')
    dpr.addNum('FlangeFreeDiameterTop', 90, 5, 200, 1, 'Diameter to keep free for the return flange, top side', mm, 'plumbing')
    dpr.addNum('FlangeFreeHeightBottom', 21, 0, 200, 1, 'Height to keep free for the return flange, bottom side', mm, 'plumbing')
    dpr.addNum('FlangeFreeDiameterBottom', 80, 5, 200, 1, 'Diameter to keep free for the return flange, bottom side', mm, 'plumbing')
    dpr.addNum('FlangePipeLengthInside', 22, 0, 100, 1, 'Length that the pipe bury inside the flange', mm, 'plumbing')
    return dpr


def DefaultsClosedLoop(categories):
    mm = 'mm'
    bn = ConfDefs('ConfigPipesNozzleClosedLoop', categories)
    bn.addNum('PipeDiameter', 33, 5, 100, 1, 'External diameter of the pipe', mm, 'plumbing')
    bn.addNum('PipeThickness', 3.2, .1, 5, .1, 'Wall thickness of the pipe', mm, 'plumbing')
    bn.addNum('FlangeDiameter', 45, 5, 100, 1, 'External diameter of the pipe', mm, 'plumbing')
    bn.addNum('FlangeFreeHeightTop', 21, 0, 200, 1, 'Height to keep free for the flange, top side', mm, 'plumbing')
    bn.addNum('FlangeFreeDiameterTop', 90, 5, 200, 1, 'Diameter to keep free for the flange, top side', mm, 'plumbing')
    bn.addNum('FlangeFreeHeightBottom', 21, 0, 200, 1, 'Height to keep free for the flange, bottom side', mm, 'plumbing')
    bn.addNum('FlangeFreeDiameterBottom', 80, 5, 200, 1, 'Diameter to keep free for the flange, bottom side', mm, 'plumbing')
    bn.addNum('FlangePipeLengthInside', 22, 0, 100, 1, 'Length that the pipe bury inside the flange', mm, 'plumbing')
    return bn


class config_sheet():

    def __init__(self, doc, name):
        self._sheet = doc.getObject(name)
        if self._sheet == None:
             self._sheet = doc.addObject('Spreadsheet::Sheet', name)
        self._sheet.Label = name
        self._line = 1

    def add(self, name, value, descr=None):
        self._sheet.set(f"A{self._line}", str(value))
        self._sheet.setAlias(f"A{self._line}", name)
        if descr:
            self._sheet.set(f"B{self._line}", descr)
        self._line = self._line + 1

    def sep(self, name):
        self._sheet.set(f"A{self._line}", name)
        self._line = self._line + 1

    def recompute(self):
        self._sheet.recompute()


def MakeComputed(doc):
    if hasattr(doc, 'Computed'):
        return
    s = config_sheet(doc, 'Computed')
    s.add('Width', '=Config.Width-2*Config.PanelThickness')
    s.add('Length', '=Config.Length-2*Config.PanelThickness')
    s.add('BeamsDir', '=Computed.Width>Computed.Length?0:1')
    s.add('PanelFastenerSizeVertical', '=Config.PanelMountHoleBorderSpacing*2+Config.PanelMountHoleSpacing*(Config.PanelMountHoleCountVertical-1)')
    s.add('PanelFastenerSizeHorizontal', '=Config.PanelMountHoleBorderSpacing*2+Config.PanelMountHoleSpacing*(Config.PanelMountHoleCountHorizontal-1)')
    s.add('SumpBeamsLevel', '=Config.Sump2FloorSpaceForBroom+Config.MetalProfileWidth/2', 'Level of center of sump beams')
    s.add('WaterLevelDeepest', '=Config.StandVisibleHeight-Config.HideExtraBottom-Config.SidesGlassThickness', 'Level of the base glass')
    s.add('GlassLevel', '=WaterLevelDeepest-Config.BottomGlassThickness', 'Level of the deepest water inside glass (pipes can go deeper)')
    s.add('UnderGlassBaseLevel', '=GlassLevel-Config.UnderGlassLevelingBaseThickness', 'Level of the base that distribute que weigth to the structure')
    s.add('BeamsLevel', '=UnderGlassBaseLevel-Config.MetalProfileWidth/2', 'Level of center of sump beams')
    s.add('SumpBoardLevel', '=Config.Sump2FloorSpaceForBroom+Config.MetalProfileWidth', 'Level of sump base board')
    s.add('RealGlassHeight', '=Config.VisibleHeightGlass+Config.HideExtraTop+Config.HideExtraBottom+3*Config.SidesGlassThickness', 'Real height of glass panels')
    s.add('RightCornerX', '=+Computed.Width/2', 'Coordinate of corner')
    s.add('LeftCornerX', '=-Computed.Width/2', 'Coordinate of corner')
    s.add('FrontCornerY', '=-Computed.Length/2', 'Coordinate of corner')
    s.add('BackCornerY', '=+Computed.Length/2', 'Coordinate of corner')
    s.add('BeamsSumpSizeWidth', '=Computed.Width-2*Config.MetalProfileWidth', 'Length of beams in the width size')
    s.add('BeamsSumpSizeLength', '=Computed.Length-2*Config.MetalProfileHeight', 'Length of beams in the length size')
    s.add('BeamsSizeWidth', '=Computed.Width-Config.MetalProfileWidth', 'Length of beams in the width size')
    s.add('BeamsSizeWidth45', '=Computed.Width', 'Length of beams in the width size')
    s.add('BeamsSizeLength', '=Computed.Length', 'Length of beams in the length size')
    s.add('BeamsSizeMiddle', '=min(Computed.Width;Computed.Length)-Config.MetalProfileWidth', 'Length of beams in the width size')
    s.add('SumpBeamSpacing', '=((BeamsDir>0?Computed.Length:Computed.Width)-Config.MetalProfileHeight)/max(1;Config.BeamsSumpCount+1)')
    s.add('StandBeamSpacing', '=((BeamsDir>0?Computed.Length:Computed.Width)-Config.MetalProfileHeight)/max(1;Config.BeamsStandCount+1)')
    s.add('NozzlesStart', '=abs(StandBeamSpacing) * (Config.NozzlesSkipBefore + 0.5)+Config.MetalProfileHeight/2')
    s.add('NozzlesEnd', '=abs(StandBeamSpacing) * (Config.NozzlesSkipAfter + 0.5)')
    s.add('NozzlesCount', '=1+((BeamsDir>0?Computed.Length:Computed.Width) - NozzlesStart - NozzlesEnd) / max(1; abs(StandBeamSpacing*Config.NozzlesEveryXBeamSpace))')
    s.add('NozzlesSpacingRows', '=(BeamsDir>0?Computed.Width:Computed.Length-WeirDepth)/max(Config.NozzlesRows;1)')
    s.add('NozzlesSpacingY', '=BeamsDir>0?StandBeamSpacing*Config.NozzlesEveryXBeamSpace:NozzlesSpacingRows')
    s.add('NozzlesSpacingX', '=BeamsDir>0?NozzlesSpacingRows:StandBeamSpacing*Config.NozzlesEveryXBeamSpace')
    s.add('NozzlesNumberY', '=BeamsDir>0?NozzlesCount:Config.NozzlesRows')
    s.add('NozzlesNumberX', '=BeamsDir>0?Config.NozzlesRows:NozzlesCount')
    s.add('NozzlesBaseX', '=LeftCornerX+(BeamsDir>0?NozzlesSpacingRows:StandBeamSpacing)/2+(BeamsDir>0?0:Config.MetalProfileHeight/2)')
    s.add('NozzlesBaseY', '=FrontCornerY+(BeamsDir>0?StandBeamSpacing:NozzlesSpacingRows)/2+(BeamsDir>0?Config.MetalProfileHeight/2:0)')
    s.add('ColumnsSizeHeight', '=UnderGlassBaseLevel-Config.MetalProfileWidth', 'Length of columns')
    s.add('FlangesNeckHeight', '=Config.SidesGlassThickness+Config.BottomGlassThickness');
    s.add('FlangesFreeByHeadDrain', '=ConfigPipesDrain.FlangeFreeDiameterTop/2+Config.SidesGlassThickness');
    s.add('FlangesFreeByPipeDrain', '=ConfigPipesDrain.PipeDiameter/2+Config.MetalProfileHeight');
    s.add('FlangesFreeByTailDrain', '=ConfigPipesDrain.FlangeFreeDiameterBottom/2');
    s.add('FlangesFreeByHeadReturn', '=ConfigPipesReturn.FlangeFreeDiameterTop/2+Config.SidesGlassThickness');
    s.add('FlangesFreeByPipeReturn', '=ConfigPipesReturn.PipeDiameter/2+Config.MetalProfileHeight');
    s.add('FlangesFreeByTailReturn', '=ConfigPipesReturn.FlangeFreeDiameterBottom/2');
    s.add('WeirCenter', '=max(FlangesFreeByHeadDrain;FlangesFreeByPipeDrain;FlangesFreeByTailDrain;FlangesFreeByHeadReturn;FlangesFreeByPipeReturn;FlangesFreeByTailReturn)');
    s.add('FlangesMaxDiameter', '=max(ConfigPipesDrain.FlangeFreeDiameterTop;ConfigPipesDrain.FlangeFreeDiameterBottom;ConfigPipesReturn.FlangeFreeDiameterTop;ConfigPipesReturn.FlangeFreeDiameterBottom)');
    s.add('WeirDepth', '=2*(WeirCenter)');
    s.add('FlangesY', '=Computed.Length/2-WeirCenter-Config.SidesGlassThickness', 'Center of flanges, Y')
    s.add('FlangesZ', '=GlassLevel+FlangesNeckHeight', 'Center of flanges, Z')
    s.add('WeirMargin', '=Config.BraceWidth+Config.SidesGlassThickness')
    s.add('WeirWidth', '=Computed.Width-2*WeirMargin')
    s.add('WeirInsideWidth', '=WeirWidth-2*Config.SidesGlassThickness')
    s.add('StartPipes', '=LeftCornerX+(Config.BraceWidth+2*Config.SidesGlassThickness+FlangesMaxDiameter/2)')
    s.add('BulkHeadSpace', '=WeirInsideWidth/(Config.BulkHeadNumber)')
    s.add('FlangeCount', '0')
    s.add('WeirFlangeOffset', '=(WeirInsideWidth-FlangesMaxDiameter)/max(FlangeCount-1;1)')
    s.add('BeamCanopyFront2BackLength', '=Computed.Length-2*Config.CanopyProfileHeight')
    s.add('BeamCanopyLeft2RightLength', '=Computed.Width-2*Config.CanopyProfileWidth')
    s.add('CanopyPanelLevel', '=Config.StandVisibleHeight+Config.VisibleHeightGlass', 'Level of the canopy')
    s.add('CanopyPanelHeight', '=Config.CanopyHeight', 'Level of the canopy')
    s.add('CanopyLevel', '=CanopyPanelLevel+Config.HideExtraTop+2*Config.SidesGlassThickness', 'Level of the canopy')
    s.add('CanopyBeamsLevel', '=CanopyPanelLevel+Config.CanopyHeight-Config.CanopyBeams2Top', 'Level of the canopy beams')
    s.add('CanopySpacingX', '=(Computed.Width - Config.CanopyProfileHeight) / max(1; Config.CanopyExtraBeams + 1)')
    s.add('CanopyBeamsX', '=Config.CanopyExtraBeams+2')
    s.add('CanopyColumnHeight', '=Config.CanopyHeight-Config.HideExtraTop-2*Config.SidesGlassThickness');
    s.recompute()


class Configuration():

    def __init__(self, doc):
        self.defsConfigs = dict()
        categories = dict()
        for x in [ DefaultsConfig(categories), DefaultsPipesDrain(categories), DefautsPipesReturn(categories), DefaultsClosedLoop(categories) ]:
            self.defsConfigs[x.type()] = x
        self.categories = categories
        self.configRepository = dict()
        self.SetDefaults(doc)

    def SetDefaults(self, doc):
        for type in self.defsConfigs:
            c = ConfigRepository(doc, type)
            for k in self.defsConfigs[type]:
                c.setdefault(k, self.defsConfigs[type][k].default)
            self.configRepository[type] = c
        self.recompute()

    def recompute(self):
        for v in self.configRepository.values():
            v.recompute()


def GetConfiguration(doc):
    conf = Configuration(doc)
    MakeComputed(doc)
    return conf
