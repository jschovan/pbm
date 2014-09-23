"""
    pbm.templatetags.pbm_extras
"""
import logging
from django import template
from django.template.loader import render_to_string
##from core.common.utils import getPrefix, getContextVariables
#from ...common.utils import getPrefix, getContextVariables, getAoColumnsList

_logger = logging.getLogger('bigpandamon-pbm')


register = template.Library()


@register.simple_tag
def pbm_plot_pie(data, title='', divid='plot', template='pbm/templatetags/pbm_plot_pie.html', *args, **kwargs):
    """
        Template tag to plot data in a higcharts pie plot.
        
    """
    returnData = { \
        'data': data, \
        'title': title, \
        'divid': divid, \
    }
    return render_to_string(template, returnData)

