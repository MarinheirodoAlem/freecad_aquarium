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

from collections import namedtuple

from FreeCAD import Units
import FreeCAD as App
import FreeCADGui
from PySide import QtCore
from PySide.QtGui import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QSpinBox, QCheckBox
from config import GetConfiguration, ConfigValueBool, ConfigValueNumeric


class Quantity(QWidget):

    def __init__(self, name, min, max, val, step=None, suffix=None):
        super(Quantity, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        if None != step and step < 1:
            self.quantityInput = QDoubleSpinBox()
        else:
            self.quantityInput = QSpinBox()
        self.quantityInput.setMinimum(min)
        self.quantityInput.setMaximum(max)
        if None != step:
            self.quantityInput.setSingleStep(step)
        if None != suffix:
            self.quantityInput.setSuffix(suffix)
        self.quantityInput.setValue(val)
        layout.addWidget(self.quantityInput)
        self.setLayout(layout)

    def value(self):
        return self.quantityInput.property('value')


class Option(QCheckBox):

    def __init__(self, name, value=False):
        super(Option, self).__init__(name)
        self.setChecked(value)

    def value(self):
        return self.isChecked()

           
class ConfigWidget(QWidget):

    def __init__(self, conf, category=None):
        if App.ActiveDocument is None:
            return
        super(ConfigWidget, self).__init__()
        layout = QVBoxLayout()
        self.config = conf
        self.form = []
        self.variable2widget = dict()
        if category is None:
            vars = []
            for type in self.config.defsConfigs:
                repo = self.config.defsConfigs[type]
                for name in repo:
                    vars.append((type, name))
        else:
            vars = self.config.categories[category]
        for c in vars:
            type = c[0]
            name = c[1]
            confDef = self.config.defsConfigs[type][name]
            value = self.config.configRepository[type][name]
            if isinstance(confDef, ConfigValueNumeric):
                suffix = confDef.unit
                if suffix is not None:
                    suffix = ' ' + suffix
                wid = Quantity(confDef.descr, confDef.min, confDef.max, value, confDef.step, suffix)
            elif isinstance(confDef, ConfigValueBool):
                wid = Option(confDef.descr, False)
            self.variable2widget[c] = wid
            self.form.append(wid)
            layout.addWidget(wid)
        self.variables = vars
        self.setLayout(layout)

    def value(self, type, name):
        return self.variable2widget[(type, name)].value()

class ConfigDialog():

    def __init__(self, category=None):
        if App.ActiveDocument is None:
            return
        self.config = GetConfiguration(App.ActiveDocument)
        self.form = ConfigWidget(self.config, category)

    def accept(self):
        updated = []
        for type, name in self.form.variables:
            currVal = self.config.configRepository[type][name]
            newVal = self.form.value(type, name)
            if(currVal != newVal):
                self.config.configRepository[type][name] = newVal
                updated.append((name, type, currVal, newVal))
                print(f"Updating {type}:{name} from {currVal} to {newVal}")
        if len(updated) > 0:
            App.ActiveDocument.recompute()
        FreeCADGui.Control.closeDialog()

    def reject(self):
        print("Cancel")
        FreeCADGui.Control.closeDialog()


class Configure:
    """Explanation of the command."""

    def __init__(self, name, caption, descr, category=None):
        """Initialize variables for the command that must exist at all times."""
        self.mw = FreeCADGui.getMainWindow()
        self.name = name
        self.caption = caption
        self.descr = descr
        self.category = category

    def GetResources(self):
        """Return a dictionary with data that will be used by the button or menu item."""
        # 'Pixmap': 'MyCommand.svg',
        return {
                'MenuText': QtCore.QT_TRANSLATE_NOOP(self.name, self.caption),
                'ToolTip': QtCore.QT_TRANSLATE_NOOP(self.name, self.descr)
                }

    def Activated(self):
        """Run the following code when the command is activated (button press)."""
        FreeCADGui.Control.showDialog(ConfigDialog(self.category))

    def IsActive(self):
        """Return True when the command should be active or False when it should be disabled (greyed)."""
        return App.ActiveDocument != None


def RegisterCommands():
    FreeCADGui.addCommand("Configure", Configure("Configure", "Everything", "Configure everything"))
    FreeCADGui.addCommand("ConfigureStructure", Configure("ConfigureStructure", "Structure", "Configure  the Structure", "structure"))
    FreeCADGui.addCommand("ConfigureVisual", Configure("ConfigureVisual", "External Visual", "Configure the External Visual", "visual"))
    FreeCADGui.addCommand("ConfigurePlumbing", Configure("ConfigurePlumbing", "Plumbing", "Configure the Plumbing", "plumbing"))
    FreeCADGui.addCommand("ConfigureGlass", Configure("ConfigureGlass", "Glass Panels", "Configure the Glass Parts", "glass"))
    FreeCADGui.addCommand("ConfigureWeir", Configure("ConfigureWeir", "Weir", "Configure the Weir", "weir"))
    FreeCADGui.addCommand("ConfigureCanopy", Configure("ConfigureCanopy", "Canopy", "Configure the Canopy", "canopy"))


def AllCommands():
    return [
        "Configure",
        "ConfigureStructure",
        "ConfigureVisual",
        "ConfigurePlumbing",
        "ConfigureGlass",
        "ConfigureWeir",
        "ConfigureCanopy"
    ]
