# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LarsRegression


class OWLarsRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "LARS Regression"
    description = "Implements the LARS regression method (a form of sparse linear regression). See also sklearn.linear_model.LarsCV."
    author = "Christian Kothe"
    icon = "icons/LarsRegression.svg"
    priority = 6
    category = "Machine_Learning"

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
    num_folds = Setting(None)
    num_alphas = Setting(None)
    max_iter = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    normalize_features = Setting(None)
    include_bias = Setting(None)
    precompute = Setting(None)
    epsilon = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LarsRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('num_alphas', self.node.num_alphas)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('normalize_features', self.node.normalize_features)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('precompute', self.node.precompute)
            super().__setattr__('epsilon', self.node.epsilon)
        else:
            self.node.num_folds = self.num_folds
            self.node.num_alphas = self.num_alphas
            self.node.max_iter = self.max_iter
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.normalize_features = self.normalize_features
            self.node.include_bias = self.include_bias
            self.node.precompute = self.precompute
            self.node.epsilon = self.epsilon

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.num_alphas_control = gui.lineEdit(box, self, 'num_alphas', 'Num alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_alphas'), tooltip="Number of alpha values to fit. This determines how densely the regularization path is explored.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations. Additional stopping criterion to limit compute time.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs. The value -1 means use all available CPU cores.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'), tooltip="Normalize features. Should only be disabled if the data comes in with a predictable scale (e.g., normalized in some other way).")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.precompute_control = gui.lineEdit(box, self, 'precompute', 'Precompute:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('precompute'), tooltip="Precompute shared data. Precompute some shared data that is reused during parameter search. Aside from 'auto', can be True, False, or the actual Gram matrix.")
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', 'Epsilon:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('epsilon'), tooltip="Degeneracy regularization. This parameter can be used to ensure that the underlying computation does not fail with singular results. Can be increased in cases where the number of features is very high compared to the number of observations.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data