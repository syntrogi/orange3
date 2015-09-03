# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import DictionaryLearning


class OWDictionaryLearning(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Dictionary Learning"
    description = "Perform sparse dictionary learning."
    author = "Christian Kothe"
    icon = "icons/DictionaryLearning.svg"
    priority = 2
    category = "Feature_Extraction"

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
    num_components = Setting(None)
    alpha = Setting(None)
    transform_alpha = Setting(None)
    max_iter = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)
    transform_nonzeroes = Setting(None)
    tolerance = Setting(None)
    fit_algorithm = Setting(None)
    transform_algorithm = Setting(None)
    split_sign = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(DictionaryLearning())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('alpha', self.node.alpha)
            super().__setattr__('transform_alpha', self.node.transform_alpha)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
            super().__setattr__('transform_nonzeroes', self.node.transform_nonzeroes)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('fit_algorithm', self.node.fit_algorithm)
            super().__setattr__('transform_algorithm', self.node.transform_algorithm)
            super().__setattr__('split_sign', self.node.split_sign)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.num_components = self.num_components
            self.node.alpha = self.alpha
            self.node.transform_alpha = self.transform_alpha
            self.node.max_iter = self.max_iter
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes
            self.node.transform_nonzeroes = self.transform_nonzeroes
            self.node.tolerance = self.tolerance
            self.node.fit_algorithm = self.fit_algorithm
            self.node.transform_algorithm = self.transform_algorithm
            self.node.split_sign = self.split_sign
            self.node.random_seed = self.random_seed

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'), tooltip="Number of components to keep. If left unset, all components are kept.")
        self.alpha_control = gui.lineEdit(box, self, 'alpha', 'Alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha'), tooltip="Sparsity level. Higher values yield sparser components.")
        self.transform_alpha_control = gui.lineEdit(box, self, 'transform_alpha', 'Transform alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_alpha'), tooltip="Sparsity level during transformation. Does not apply to 'lars' case.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs to run.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any chunk will be processed.")
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', 'Domain axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('domain_axes'), tooltip="Axes which form the input domain of the transformation (e.g., a spatial decomposition like PCA on channels would have this set to 'space'. This is a  comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', 'Aggregate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('aggregate_axes'), tooltip="Axes to aggregate statistics over. These are the axes that are treated as holding the statistical 'observations' or 'realizations'. For instance, a time-series model usually uses 'time' for this axis, and a method operating on trials/segments would use 'instance'. This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', 'Separate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('separate_axes'), tooltip="Axes along which to learn separate models. This method can learn multiple separate and independent models (e.g., one per frequency, or one per time slice) in parallel. This is not a very common use case and thus argument is usually left empty (meaning: no axis). This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.transform_nonzeroes_control = gui.lineEdit(box, self, 'transform_nonzeroes', 'Transform nonzeroes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_nonzeroes'), tooltip="Targeted number of non-zeroes per column in the solution. Only used by 'lars'.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Tolerance for optimization. Serves as a stopping criterion.")
        self.fit_algorithm_control = gui.lineEdit(box, self, 'fit_algorithm', 'Fit algorithm:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('fit_algorithm'), tooltip="Method used during fitting. The lars method is faster than coordinate descent if the components are sparse.")
        self.transform_algorithm_control = gui.lineEdit(box, self, 'transform_algorithm', 'Transform algorithm:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_algorithm'), tooltip="Method used during transform. lasso_lars is fastest when components are sparse.")
        self.split_sign_control = gui.checkBox(box, self, 'split_sign', 'Split sign', callback=lambda: self.property_changed('split_sign'), tooltip="Split the sparse feature vector into the concatenation of its negative and positive part.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data