# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import PruneFlatlineChannels


class OWPruneFlatlineChannels(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Prune Flatline Channels"
    description = "Prune data that has flat-line channels. This node updates its removal mask on non-incremental chunks and carries the mask over to incremental chunks."
    author = "Christian Kothe"
    icon = "icons/PruneFlatlineChannels.svg"
    priority = 11
    category = "Filters"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    max_duration = Setting(None)
    max_jitter_rel = Setting(None)
    max_jitter_abs = Setting(None)
    calib_seconds = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(PruneFlatlineChannels())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_duration', self.node.max_duration)
            super().__setattr__('max_jitter_rel', self.node.max_jitter_rel)
            super().__setattr__('max_jitter_abs', self.node.max_jitter_abs)
            super().__setattr__('calib_seconds', self.node.calib_seconds)
        else:
            self.node.max_duration = self.max_duration
            self.node.max_jitter_rel = self.max_jitter_rel
            self.node.max_jitter_abs = self.max_jitter_abs
            self.node.calib_seconds = self.calib_seconds

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_duration_control = gui.lineEdit(box, self, 'max_duration', 'Max duration:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_duration'), tooltip="Maximum flat-line duration. If a channel has a longer flatline than this, it will be removed. In seconds.")
        self.max_jitter_rel_control = gui.lineEdit(box, self, 'max_jitter_rel', 'Max jitter rel:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_jitter_rel'), tooltip="Allowed relative jitter. This is relative to the absolute signal value.")
        self.max_jitter_abs_control = gui.lineEdit(box, self, 'max_jitter_abs', 'Max jitter abs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_jitter_abs'), tooltip="Allowed absolute jitter.")
        self.calib_seconds_control = gui.lineEdit(box, self, 'calib_seconds', 'Calib seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('calib_seconds'), tooltip="Data length for calibration. In seconds. Default: 15.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data