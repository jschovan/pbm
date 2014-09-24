"""
    pbm.utils
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum

from .models import DailyLog
from .ADC_colors import ADC_COLOR

_logger = logging.getLogger('bigpandamon-pbm')


defaultDatetimeFormat = '%Y-%m-%d'


CATEGORY_LABELS = {
    'A': 'User selected a site', \
    'B': 'User selected a cloud', \
    'C': 'PanDA decides destination', \
    'D': 'Skip by Panda', \
    'E': 'User excluded a site', \
    'E+': 'With exclude', \
    'E-': 'Without exclude', \

}


PLOT_TITLES = {
    'title01': 'User selected a site/User selected a cloud/PanDA Brokerage decision on Jobs', \
    'title02': 'User selected a site/User selected a cloud/PanDA Brokerage decision on jobDef', \
    'title03': 'User selected a site/User selected a cloud/PanDA Brokerage decision on jobSet', \

    'title04': 'User selected a site on Jobs - Top sites with share > 1 %', \
    'title05': 'User selected a site on jobDef - Top sites with share > 1 %', \
    'title06': 'User selected a site on jobSet - Top sites with share > 1 %', \
    'title07': 'User selected a site on Jobs - Per cloud', \
    'title08': 'User selected a site on JobDef - Per cloud', \
    'title09': 'User selected a site on JobSet - Per cloud', \

    ### plots 10 .. 12 are not used, we don't have data for them, since site==cloud for them
    'title10': 'User selected a cloud on Jobs - Top sites with share > 1 %', \
    'title11': 'User selected a cloud on jobDef - Top sites with share > 1 %', \
    'title12': 'User selected a cloud on jobSet - Top sites with share > 1 %', \
    'title13': 'User selected a cloud on Jobs - Per cloud', \
    'title14': 'User selected a cloud on JobDef - Per cloud', \
    'title15': 'User selected a cloud on JobSet - Per cloud', \

    'title16': 'PanDA Brokerage decision on Jobs - Top sites with share > 1 %', \
    'title17': 'PanDA Brokerage decision on JobDef - Top sites with share > 1 %', \

    'title18': 'PanDA Brokerage decision on Jobs - Per cloud', \
    'title19': 'PanDA Brokerage decision on JobDef - Per cloud', \

    'title20': 'User excluded a site on distinct jobSet - With exclude / Without exclude', \

    'title21': 'User excluded a site on jobSet - Top sites with share > 1 %', \
    'title22': 'User excluded a site on distinct DnUser - Top sites with share > 1 %', \
    'title23': 'User excluded a site on jobSet - Per cloud', \
    'title24': 'User excluded a site on distinct DnUser - Per cloud', \

    'title25': 'Jobs submitted by Country', \
    'title26': 'JobDefs submitted by Country', \
    'title27': 'JobSets submitted by Country', \
}


PLOT_UNITS = {
    '01': 'jobs', \
    '02': 'jobDefs', \
    '03': 'jobSets', \

    '04': 'jobs', \
    '05': 'jobDefs', \
    '06': 'jobSets', \
    '07': 'jobs', \
    '08': 'jobDefs', \
    '09': 'jobSets', \

    ### plots 10 .. 12 are not used, we don't have data for them, since site==cloud for them
    '10': 'jobs', \
    '11': 'jobDefs', \
    '12': 'jobSets', \

    '13': 'jobs', \
    '14': 'jobDefs', \
    '15': 'jobSets', \

    '16': 'jobs', \
    '17': 'jobDefs', \

    '18': 'jobs', \
    '19': 'jobDefs', \

    '20': 'jobSets', \

    '21': 'jobSets', \
    '22': 'UserDNs', \
    '23': 'jobSets', \
    '24': 'UserDNs', \

    '25': 'jobs', \
    '26': 'JobDefs', \
    '27': 'JobSets', \
}


COLORS = {
    '01': ['#FF0000', '#50B432', '#0000FF'],
    '02': ['#FF0000', '#50B432', '#0000FF'],
    '03': ['#FF0000', '#50B432', '#0000FF'],
    '20': ['#FF0000', '#0000FF'],
    '25': ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    '26': ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
    '27': ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],

}


def get_colors_dictionary(data, cutoff=None):
    colors = {}
    counter = {}
    ### init cloud item counters
    for cloud in ADC_COLOR.keys():
        counter[cloud] = 0
    ### loop over data, increment cloud counters -> get predefined colors for sites/clouds
    for item in data:
        append = True
        if cutoff is not None:
            if cutoff < float(item['percent'][:-1]):
                append = True
            else:
                append = False
        if append:
            try:
                cloud = item['cloud']
                if cloud in counter:
                    item_color = ADC_COLOR[cloud][counter[cloud]]
                    if 'site' in item:
                        counter[cloud] += 1
                    if 'country' in item:
                        counter[cloud] += 1
                else:
                    item_color = '#FFFFFF'
            except:
                item_color = '#FFFFFF'
            if 'site' in item:
                colors[item['site']] = item_color
            else:
                colors[item['cloud']] = item_color
    return colors


def prepare_data_for_piechart(data, unit='jobs', cutoff=None):
    """
        prepare_data_for_piechart
        
        
        data ... result of a queryset
        unit ... 'jobs', or 'jobDefs', or 'jobSets'
        cutoff ... anything with share smaller than cutoff percent will be grouped into 'Other' 
        
        example input:
            data = [{'category': u'A', 'sum': 13046, 'percent': '7.90%', 'label': 'User selected a site'}, 
                    {'category': u'B', 'sum': 157, 'percent': '0.10%', 'label': 'User selected a cloud'}, 
                    {'category': u'C', 'sum': 151990, 'percent': '92.01%', 'label': 'PanDA decides destination'}
            ] 
        example output:
            piechart_data = [ ['User selected a site', 13046], 
                              ['User selected a cloud', 157], 
                              ['PanDA decides destination', 151990] 
            ]
    """
    piechart_data = []
    other_item_sum = 0
    for item in data:
        append = True
        if cutoff is not None:
            if cutoff < float(item['percent'][:-1]):
                append = True
            else:
                append = False
                other_item_sum += int(item['sum'])
        if append:
            piechart_data.append([ str('%s (%s %s)' % (item['label'], item['sum'], unit)), item['sum']])
    if other_item_sum > 0:
        piechart_data.append(['Other (%s %s)' % (other_item_sum, unit), other_item_sum])
    return piechart_data


def prepare_colors_for_piechart(data, cutoff=None):
    """
        prepare_colors_for_piechart
        
        
        data ... result of a queryset
        unit ... 'jobs', or 'jobDefs', or 'jobSets'
        cutoff ... anything with share smaller than cutoff percent will be grouped into 'Other' 
        
    """
    colors_names = get_colors_dictionary(data, cutoff)
    colors = []
    other_item_sum = 0
    for item in data:
        append = True
        if cutoff is not None:
            if cutoff < float(item['percent'][:-1]):
                append = True
            else:
                append = False
                other_item_sum += int(item['sum'])
        if append:
            if item['name'] in colors_names:
                colors.append(colors_names[item['name']])
            else:
                colors.append('#CCCCCC')
    if other_item_sum > 0:
        colors.append('#CCCCCC')
    return colors


def configure(request_GET):
    errors_GET = {}
    ### if startdate&enddate are provided, use them
    if 'startdate' in request_GET and 'enddate' in request_GET:
        ndays = -1
        ### startdate
        startdate = request_GET['startdate']
        try:
            dt_start = datetime.strptime(startdate, defaultDatetimeFormat)
        except ValueError:
            errors_GET['startdate'] = \
                'Provided startdate [%s] has incorrect format, expected [%s].' % \
                (startdate, defaultDatetimeFormat)
            startdate = datetime.utcnow() - timedelta(days=ndays)
            startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        ### enddate
        enddate = request_GET['enddate']
        try:
            dt_end = datetime.strptime(enddate, defaultDatetimeFormat)
        except ValueError:
            errors_GET['enddate'] = \
                'Provided enddate [%s] has incorrect format, expected [%s].' % \
                (enddate, defaultDatetimeFormat)
            enddate = datetime.utcnow()
            enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### if ndays is provided, do query "last N days"
    elif 'ndays' in request_GET:
        try:
            ndays = int(request_GET['ndays'])
        except:
            ndays = 8
            errors_GET['ndays'] = \
                'Wrong or no ndays has been provided.Using [%s].' % \
                (ndays)
        startdate = datetime.utcnow() - timedelta(days=ndays)
        startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow()
        enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    ### neither ndays, nor startdate&enddate was provided
    else:
        ndays = 8
        startdate = datetime.utcnow() - timedelta(days=ndays)
        startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        enddate = datetime.utcnow()
        enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
        errors_GET['noparams'] = \
                'Neither ndays, nor startdate & enddate has been provided. Using startdate=%s and enddate=%s.' % \
                (startdate, enddate)
    
    return startdate, enddate, ndays, errors_GET


def configure_plot(request_GET):
    ### if plotid is provided, use it
    if 'plotid' in request_GET:
        plotid = request_GET['plotid']
    ### plotid was not provided
    else:
        plotid = 0
    return plotid


def data_plot_groupby_category(query, values=['category'], \
        sum_param='jobcount', label_cols=['category'], label_translation=True, \
        order_by=[]):
    pre_data_01 = DailyLog.objects.filter(**query).values(*values).annotate(sum=Sum(sum_param))
    if len(order_by):
        pre_data_01 = pre_data_01.order_by(*order_by)
    total_data_01 = sum([x['sum'] for x in pre_data_01])
    data01 = []
    colors01 = {}
    for item in pre_data_01:
        item['name'] = item[label_cols[0]]
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_01)
        if label_translation:
            if len(label_cols) > 1:
                item['label'] = '%s (%s)' % (item[label_cols[0]], item[label_cols[1]])
            else:
                item['label'] = CATEGORY_LABELS[ item[label_cols[0]] ]
        else:
            if len(label_cols) > 1:
                item['label'] = '%s (%s)' % (item[label_cols[0]], item[label_cols[1]])
            else:
                item['label'] = item[label_cols[0]]
        data01.append(item)
    return data01


