# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import Spectrogram


class OWSpectrogram(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Spectrogram"
    description = "Calculate a spectrogram (time/frequency representation)."
    author = "Christian Kothe"
    icon = "icons/Spectrogram.svg"
    priority = 6
    category = "Spectral"

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
    segment_samples = Setting(None)
    overlap_samples = Setting(None)
    scaling = Setting(None)
    window = Setting(None)
    fft_size = Setting(None)
    detrend = Setting(None)
    onesided = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Spectrogram())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('segment_samples', self.node.segment_samples)
            super().__setattr__('overlap_samples', self.node.overlap_samples)
            super().__setattr__('scaling', self.node.scaling)
            super().__setattr__('window', self.node.window)
            super().__setattr__('fft_size', self.node.fft_size)
            super().__setattr__('detrend', self.node.detrend)
            super().__setattr__('onesided', self.node.onesided)
        else:
            self.node.segment_samples = self.segment_samples
            self.node.overlap_samples = self.overlap_samples
            self.node.scaling = self.scaling
            self.node.window = self.window
            self.node.fft_size = self.fft_size
            self.node.detrend = self.detrend
            self.node.onesided = self.onesided

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.segment_samples_control = gui.lineEdit(box, self, 'segment_samples', 'Segment samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('segment_samples'), tooltip="Segment length. In samples.")
        self.overlap_samples_control = gui.lineEdit(box, self, 'overlap_samples', 'Overlap samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('overlap_samples'), tooltip="Number of overlapped samples. If None, defaults to segment_samples//8.")
        self.scaling_control = gui.lineEdit(box, self, 'scaling', 'Scaling:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('scaling'), tooltip="Scaling of the spectrum. Density is 1/f normalized.")
        self.window_control = gui.lineEdit(box, self, 'window', 'Window:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window'), tooltip="Type of window function to use. Can be a string (see scipy.signal.windows.get_window) or a tuple of window name and parameter.")
        self.fft_size_control = gui.lineEdit(box, self, 'fft_size', 'Fft size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('fft_size'), tooltip="Length of the FFT used, if a zero-padded FFT is desired. If none, defaults to segment_samples.")
        self.detrend_control = gui.lineEdit(box, self, 'detrend', 'Detrend:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('detrend'), tooltip="Detrending method.")
        self.onesided_control = gui.checkBox(box, self, 'onesided', 'Onesided', callback=lambda: self.property_changed('onesided'), tooltip="Return one-sided spectrum. For complex data, the spectrum is always two-sided.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data