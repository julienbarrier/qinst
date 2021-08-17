"""
Class for precision current source.
This is a manual instrument
"""

from typing import Tuple, Dict, Optional
from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import Parameter, ManualParameter, \
    MultiParameter, ParamRawDataType
from qcodes.utils.validators import Enum


class CurrentParameter(MultiParameter):
    """
    sourcing voltage through lock-in and precision current source will convert
    a voltage into a current.

    Args:
        measured_param: gettable parameter, returning the current sourced from
        the source output

        c_source_ins: an instance where you manually maintain the present
        settings to the real current source.

        name: name of the current output. Default: 'curr'.
        Also used as the name of the whole parameter
    """

    def __init__(self,
                 measured_param: Parameter,
                 c_source_ins: "CurrentSource",
                 name: str = 'curr'):
        p_name = measured_param.name

        super().__init__(name=name,
                         names=(p_name+'_raw', name),
                         shapes=((), ()),
                         setpoints=((), ()),
                         instrument=c_source_ins,
                         snapshot_value=True)

        self._measured_param = measured_param

        p_label = getattr(measured_param, 'label', None)
        p_unit = getattr(measured_param, 'unit', None)

        self.labels = (p_label, 'Current')
        self.units = (p_unit, 'A')

    def get_raw_dc(self) -> Tuple[ParamRawDataType, ...]:
        assert isinstance(self.instrument, CurrentSource)
        volt = self._measured_param.get()
        current = self.instrument.range_dc.get() * volt

        value = (volt, current)
        return value

    def get_raw_ac(self) -> Tuple[ParamRawDataType, ...]:
        assert isinstance(self.instrument, CurrentSource)
        volt = self._measured_param.get()
        current = self.instrument.range_ac.get() * volt

        value = (volt, current)
        return value


class CurrentSource(Instrument):
    """
    This is the qcodes driver for the Precision Current Source.

    It is a virtual driver, it does not talk to the instrument; please adjust
    the parameters manually.
    """
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

        self.add_parameter('selector',
                           parameter_class=ManualParameter,
                           initial_value=2,
                           label='select',
                           units=None,
                           vals=Enum(1, 2, 3))

        self.add_parameter('range_dc',
                           parameter_class=ManualParameter,
                           initial_value=10e-6,
                           label='DC range',
                           units='A/V',
                           vals=Enum(100e-6, 10e-6, 1e-6))

        self.add_parameter('range_ac',
                           parameter_class=ManualParameter,
                           initial_value=10e-9,
                           label='AC range',
                           units='A/V',
                           vals=Enum(100e-9, 10e-9, 1e-9))

    def get_idn(self) -> Dict[str, Optional[str]]:
        vendor = 'Manchester Group'
        model = 'Precision Current Source'
        serial = None
        firmware = None
        return {'vendor': vendor, 'model': model,
                'serial': serial, 'firmware': firmware}
