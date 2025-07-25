from datetime import timedelta
from gettext import ngettext

from django.forms import MultiWidget
from django.forms.widgets import NumberInput
from django.utils.dateparse import parse_duration
from django.utils.translation import gettext_lazy as _


def get_time_factors(td):
    """
    Get different time factor such as days, hours, minutes and seconds
    :param td: timedelta
    :return: tuple(days, hours, minutes, seconds)
    """
    return (
        td.days,  # returns number of days
        td.seconds // 3600,  # returns number of hours
        (td.seconds // 60) % 60,  # returns number of minutes
        td.seconds % 60,  # returns number of seconds
    )


def get_human_readable_duration(value):
    format_list = []
    parsed_value = parse_duration(value)
    days, hours, minutes, seconds = get_time_factors(parsed_value)
    if days > 0:
        format_list.append('{0} {1}'.format(days, ngettext('Day', 'Days', days)))
    if hours > 0:
        format_list.append('{0} {1}'.format(hours, ngettext('Hour', _('Hours'), hours)))
    if minutes > 0:
        format_list.append('{0} {1}'.format(minutes, ngettext('Minute', 'Minutes', minutes)))
    if seconds > 0 or not format_list:
        format_list.append('{0} {1}'.format(seconds, ngettext('Second', 'Seconds', seconds)))
    return ' '.join(format_list)


class LabeledNumberInput(NumberInput):
    template_name = 'widgets/labeled_number_input.html'

    def __init__(self, label=None, attrs=None, type=None):
        self.widget_label = label
        self.type = type
        super(LabeledNumberInput, self).__init__(attrs)

    # ---------------------------------------------------------------------------------------------------------------------
    def get_context(self, name, value, attrs):
        context = super(LabeledNumberInput, self).get_context(name, value, attrs)
        context['widget']['widget_label'] = self.widget_label
        return context


class TimeDurationWidget(MultiWidget):
    """
    Time duration selector widget
    """

    template_name = 'widgets/duration_multiple_input.html'

    def get_context(self, name, value, attrs):
        context = super(TimeDurationWidget, self).get_context(name, value, attrs)
        duration_readable = ''
        if not isinstance(value, list) and value:
            duration_readable = get_human_readable_duration(value)
        context['duration_readable'] = duration_readable
        return context

    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, attrs=None, show_days=True, show_hours=True, show_minutes=True, show_seconds=True):
        self.show_days = show_days
        self.show_hours = show_hours
        self.show_minutes = show_minutes
        self.show_seconds = show_seconds
        _widgets = []
        _widgets.append(LabeledNumberInput(label=_('Days'), type='days')) if show_days else None,  # Day
        _widgets.append(LabeledNumberInput(label=_('Hours'), type='hours')) if show_hours else None,  # Hour
        _widgets.append(LabeledNumberInput(label=_('Minutes'), type='minutes')) if show_minutes else None,  # Minute
        _widgets.append(LabeledNumberInput(label=_('Seconds'), type='seconds')) if show_seconds else None,  # Seconds
        super(TimeDurationWidget, self).__init__(_widgets, attrs)

    # ---------------------------------------------------------------------------------------------------------------------
    def decompress(self, value):
        if value:
            parsed_value = parse_duration(value)
            days, hours, minutes, seconds = get_time_factors(parsed_value)
            return_list = []
            if self.show_days:
                return_list.append(days)
            else:
                # Add days to hours when days are not shown
                hours += days * 24
            return_list.append(hours) if self.show_hours else None
            return_list.append(minutes) if self.show_minutes else None
            return_list.append(seconds) if self.show_seconds else None
            return return_list
        else:
            return []

    # ---------------------------------------------------------------------------------------------------------------------
    def value_from_datadict(self, data, files, name):
        data_list = {
            widget.type: widget.value_from_datadict(data, files, name + '_{0}'.format(i))
            for i, widget in enumerate(self.widgets)
        }
        if not any(data_list.values()):
            # No data input
            return ''
        for key, val in data_list.items():
            try:
                data_list[key] = int(val)
            except ValueError:
                data_list[key] = 0

        days = 0 if not self.show_days else data_list.get('days')
        hours = 0 if not self.show_hours else data_list.get('hours')
        minutes = 0 if not self.show_minutes else data_list.get('minutes')
        seconds = 0 if not self.show_seconds else data_list.get('seconds')

        if self.is_required and days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            return ''

        try:
            D = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        except ValueError:
            return ''
        else:
            return str(D)
