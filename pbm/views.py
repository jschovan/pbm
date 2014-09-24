"""
    pbm.views
    
"""
import logging
import pytz
from datetime import datetime, timedelta

from django.db.models import Count, Sum
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader

from .models import DailyLog
from .utils import CATEGORY_LABELS, PLOT_TITLES, COLORS, defaultDatetimeFormat, \
configure, \
prepare_data_for_piechart, prepare_colors_for_piechart, \
data_plot_groupby_category

_logger = logging.getLogger('bigpandamon-pbm')


def plot_nothing(id, query):
    return [], [], PLOT_TITLES['title' + id]


def plot_01(id, query):
    data = data_plot_groupby_category(query, values=['category'], sum_param='jobcount', \
                    label_cols=['category'], label_translation=True)
    title = PLOT_TITLES['title' + id]
    colors = COLORS[id]
    return data, colors, title


def plot_02(id, query):
    data = data_plot_groupby_category(query, values=['category'], sum_param='jobdefcount', \
                    label_cols=['category'], label_translation=True)
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_03(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_03 = DailyLog.objects.filter(**query).distinct('jobset').values('category').annotate(sum=Count('jobset'))
        total_data_03 = sum([x['sum'] for x in pre_data_03])
        for item in pre_data_03:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
            item['label'] = CATEGORY_LABELS[ item['category'] ]
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_03 = DailyLog.objects.filter(**query).values('category', 'jobset')
        categories = list(set([ x['category'] for x in pre_data_03]))
        pre2_data_03 = []
        total_data_03 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_03 if x['category'] == category]))
            pre2_data_03.append({'category': category, 'sum': len(jobsets_for_category)})
            total_data_03 += len(jobsets_for_category)
        for item in pre2_data_03:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
            item['label'] = CATEGORY_LABELS[ item['category'] ]
            data.append(item)
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_04(id, query):
    data = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobcount', \
                    label_cols=['site', 'cloud'], label_translation=False, \
                    order_by=['cloud', 'site'])
    colors = prepare_colors_for_piechart(data, cutoff=1.0)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_05(id, query):
    data = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobdefcount', \
                    label_cols=['site', 'cloud'], label_translation=False, \
                    order_by=['cloud', 'site'])
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_06(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_06 = DailyLog.objects.filter(**query).distinct('jobset').values('site', 'cloud').annotate(sum=Count('jobset')).order_by('cloud', 'site')
        total_data_06 = sum([x['sum'] for x in pre_data_06])
        for item in pre_data_06:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_06 = DailyLog.objects.filter(**query).values('site', 'cloud', 'jobset').order_by('cloud', 'site')
        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_06]))
        pre2_data_06 = []
        total_data_06 = 0
        for category, cat2 in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_06 if x['site'] == category]))
            pre2_data_06.append({'site': category, 'cloud': cat2, 'sum': len(jobsets_for_category)})
            total_data_06 += len(jobsets_for_category)
        for item in pre2_data_06:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_07(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_08(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_09(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_09 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
        total_data_09 = sum([x['sum'] for x in pre_data_09])
        for item in pre_data_09:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_09)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_09 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
        categories = list(set([ x['cloud'] for x in pre_data_09]))
        pre2_data_09 = []
        total_data_09 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_09 if x['cloud'] == category]))
            pre2_data_09.append({'cloud': category, 'sum': len(jobsets_for_category)})
            total_data_09 += len(jobsets_for_category)
        for item in pre2_data_09:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_09)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_13(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_14(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_15(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_15 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
        total_data_15 = sum([x['sum'] for x in pre_data_15])
        for item in pre_data_15:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_15 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
        categories = list(set([ x['cloud'] for x in pre_data_15]))
        pre2_data_15 = []
        total_data_15 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_15 if x['cloud'] == category]))
            pre2_data_15.append({'cloud': category, 'sum': len(jobsets_for_category)})
            total_data_15 += len(jobsets_for_category)
        for item in pre2_data_15:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_16(id, query):
    data = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobcount', \
                    label_cols=['site', 'cloud'], label_translation=False, \
                    order_by=['cloud', 'site'])
    colors = prepare_colors_for_piechart(data, cutoff=1.0)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_17(id, query):
    data = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobdefcount', \
                    label_cols=['site', 'cloud'], label_translation=False, \
                    order_by=['cloud', 'site'])
    colors = prepare_colors_for_piechart(data, cutoff=1.0)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_18(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_19(id, query):
    data = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
                    label_cols=['cloud'], label_translation=False)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_20(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_20 = DailyLog.objects.filter(**query).distinct('jobset').values('category').annotate(sum=Count('jobset'))
        total_data_20 = sum([x['sum'] for x in pre_data_20])
        pre2_data_20 = []
        for item in [x for x in pre_data_20 if x['category'] == 'E']:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_20)
            item['label'] = CATEGORY_LABELS[ 'E+' ]
            data.append(item)
        not_excluded = [x for x in pre_data_20 if x['category'] != 'E']
        for item in not_excluded[:1]:
            item['percent'] = '%.2f%%' % (100.0 * sum([x['sum'] for x in not_excluded]) / total_data_20)
            item['label'] = CATEGORY_LABELS[ 'E-' ]
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_20 = DailyLog.objects.filter(**query).values('category', 'jobset')
        excluded = list(set([ x['jobset'] for x in pre_data_20 if x['category'] == 'E']))
        not_excluded = list(set([ x['jobset'] for x in pre_data_20 if x['category'] != 'E']))
        if len(excluded) + len(not_excluded) < 1:
            percent_excluded = '%.2f%%' % (0.0)
            percent_not_excluded = '%.2f%%' % (0.0)
        else:
            percent_excluded = '%.2f%%' % (100.0 * len(excluded) / (len(excluded) + len(not_excluded)))
            percent_not_excluded = '%.2f%%' % (100.0 * len(not_excluded) / (len(excluded) + len(not_excluded)))
        data.append({'category': 'E', 'sum': len(excluded), \
                       'percent': percent_excluded, \
                       'label': CATEGORY_LABELS[ 'E+' ]\
                       })
        data.append({'category': 'ABC', 'sum': len(not_excluded), \
                       'percent': percent_not_excluded, \
                       'label': CATEGORY_LABELS[ 'E-' ]\
                       })
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_21(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_21 = DailyLog.objects.filter(**query).distinct('jobset').values('site', 'cloud').annotate(sum=Count('jobset')).order_by('cloud', 'site')
        total_data_21 = sum([x['sum'] for x in pre_data_21])
        for item in pre_data_21:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_21)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_21 = DailyLog.objects.filter(**query).values('site', 'cloud', 'jobset')
        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_21]))
        pre2_data_21 = []
        total_data_21 = 0
        for category, cat2 in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_21 if x['site'] == category]))
            pre2_data_21.append({'site': category, 'cloud': cat2, 'sum': len(jobsets_for_category)})
            total_data_21 += len(jobsets_for_category)
        for item in pre2_data_21:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_21)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    colors = prepare_colors_for_piechart(data, cutoff=1.0)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_22(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_22 = DailyLog.objects.filter(**query).distinct('dnuser').values('site', 'cloud').annotate(sum=Count('dnuser')).order_by('cloud', 'site')
        total_data_22 = sum([x['sum'] for x in pre_data_22])
        for item in pre_data_22:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_22)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_22 = DailyLog.objects.filter(**query).values('site', 'cloud', 'dnuser')
        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_22]))
        pre2_data_22 = []
        total_data_22 = 0
        for category, cat2 in sorted(categories):
            dnusers_for_category = list(set([x['dnuser'] for x in pre_data_22 if x['site'] == category]))
            pre2_data_22.append({'site': category, 'cloud': cat2, 'sum': len(dnusers_for_category)})
            total_data_22 += len(dnusers_for_category)
        for item in pre2_data_22:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_22)
            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
            item['name'] = item['site']
            data.append(item)
    colors = prepare_colors_for_piechart(data, cutoff=1.0)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_23(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_23 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset')).order_by('cloud')
        total_data_23 = sum([x['sum'] for x in pre_data_23])
        for item in pre_data_23:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_23)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_23 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
        categories = list(set([ x['cloud'] for x in pre_data_23]))
        pre2_data_23 = []
        total_data_23 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_23 if x['cloud'] == category]))
            pre2_data_23.append({'cloud': category, 'sum': len(jobsets_for_category)})
            total_data_23 += len(jobsets_for_category)
        for item in pre2_data_23:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_23)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_24(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_24 = DailyLog.objects.filter(**query).distinct('dnuser').values('cloud').annotate(sum=Count('dnuser')).order_by('cloud')
        total_data_24 = sum([x['sum'] for x in pre_data_24])
        for item in pre_data_24:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_24)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_24 = DailyLog.objects.filter(**query).values('site', 'cloud', 'dnuser')
        categories = list(set([ x['cloud'] for x in pre_data_24]))
        pre2_data_24 = []
        total_data_24 = 0
        for category in sorted(categories):
            dnusers_for_category = list(set([x['dnuser'] for x in pre_data_24 if x['cloud'] == category]))
            pre2_data_24.append({'cloud': category, 'sum': len(dnusers_for_category)})
            total_data_24 += len(dnusers_for_category)
        for item in pre2_data_24:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_24)
            item['label'] = item['cloud']
            item['name'] = item['cloud']
            data.append(item)
    colors = prepare_colors_for_piechart(data)
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_25(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_25 = DailyLog.objects.filter(**query).distinct('country').values('country', 'jobcount').annotate(sum=Sum('jobcount')).order_by('country')
        total_data_25 = sum([x['sum'] for x in pre_data_25])
        for item in pre_data_25:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_25)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_25 = DailyLog.objects.filter(**query).values('country', 'jobcount')
        categories = list(set([ x['country'] for x in pre_data_25]))
        pre2_data_25 = []
        total_data_25 = 0
        for category in sorted(categories):
            jobsets_for_category = [x['jobcount'] for x in pre_data_25 if x['country'] == category]
            pre2_data_25.append({'country': category, 'sum': sum(jobsets_for_category)})
            total_data_25 += len(jobsets_for_category)
        for item in pre2_data_25:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_25)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_26(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_26 = DailyLog.objects.filter(**query).distinct('country').values('country', 'jobdefcount').annotate(sum=Sum('jobdefcount')).order_by('country')
        total_data_26 = sum([x['sum'] for x in pre_data_26])
        for item in pre_data_26:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_26)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_26 = DailyLog.objects.filter(**query).values('country', 'jobdefcount')
        categories = list(set([ x['country'] for x in pre_data_26]))
        pre2_data_26 = []
        total_data_26 = 0
        for category in sorted(categories):
            jobsets_for_category = [x['jobdefcount'] for x in pre_data_26 if x['country'] == category]
            pre2_data_26.append({'country': category, 'sum': sum(jobsets_for_category)})
            total_data_26 += len(jobsets_for_category)
        for item in pre2_data_26:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_26)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot_27(id, query):
    data = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_27 = DailyLog.objects.filter(**query).distinct('jobset').values('country').annotate(sum=Count('jobset'))
        total_data_27 = sum([x['sum'] for x in pre_data_27])
        for item in pre_data_27:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_27)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_27 = DailyLog.objects.filter(**query).values('country', 'jobset')
        categories = list(set([ x['country'] for x in pre_data_27]))
        pre2_data_27 = []
        total_data_27 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_27 if x['country'] == category]))
            pre2_data_27.append({'country': category, 'sum': len(jobsets_for_category)})
            total_data_27 += len(jobsets_for_category)
        for item in pre2_data_27:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_27)
            item['label'] = item['country']
            item['name'] = item['country']
            data.append(item)
    colors = COLORS[id]
    title = PLOT_TITLES['title' + id]
    return data, colors, title


def plot(id, query):
    dispatch = {
        '01': plot_01, \
        '02': plot_02, \
        '03': plot_03, \
        '04': plot_04, \
        '05': plot_05, \
        '06': plot_06, \
        '07': plot_07, \
        '08': plot_08, \
        '09': plot_09, \
        '10': plot_nothing, \
        '11': plot_nothing, \
        '12': plot_nothing, \
        '13': plot_13, \
        '14': plot_14, \
        '15': plot_15, \
        '16': plot_16, \
        '17': plot_17, \
        '18': plot_18, \
        '19': plot_19, \
        '20': plot_20, \
        '21': plot_21, \
        '22': plot_22, \
        '23': plot_23, \
        '24': plot_24, \
        '25': plot_25, \
        '26': plot_26, \
        '27': plot_27, \
    }
    return dispatch[id](id, query)


def index(request):
    """
        index -- pbm's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### configure time interval for queries
    startdate, enddate, ndays, errors_GET = configure(request.GET)

    ### start the query parameters
    query={}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]

    ### filter category__in
    query['category__in'] = ['A', 'B', 'C']

    ### User selected a site/User selected a cloud/Panda Brokerage decision
    ###     Plot 1: [User selected a site/User selected a cloud/Panda Brokerage decision] on Jobs
#    data01 = data_plot_groupby_category(query, values=['category'], sum_param='jobcount', \
#                    label_cols=['category'], label_translation=True)
#    if '01' in COLORS:
#        colors01 = COLORS['01']
#    else:
#        colors01 = []
    data01, colors01, title01 = plot('01', query)

    ###     Plot 2: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobDef
#    data02 = data_plot_groupby_category(query, values=['category'], sum_param='jobdefcount', \
#                    label_cols=['category'], label_translation=True)
#    if '02' in COLORS:
#        colors02 = COLORS['02']
#    else:
#        colors02 = []
    data02, colors02, title02 = plot('02', query)

    ###     Plot 3: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobSet
#    data03 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_03 = DailyLog.objects.filter(**query).distinct('jobset').values('category').annotate(sum=Count('jobset'))
#        total_data_03 = sum([x['sum'] for x in pre_data_03])
#        for item in pre_data_03:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
#            item['label'] = CATEGORY_LABELS[ item['category'] ]
#            data03.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_03 = DailyLog.objects.filter(**query).values('category', 'jobset')
#        categories = list(set([ x['category'] for x in pre_data_03]))
#        pre2_data_03 = []
#        total_data_03 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_03 if x['category'] == category]))
#            pre2_data_03.append({'category': category, 'sum': len(jobsets_for_category)})
#            total_data_03 += len(jobsets_for_category)
#        for item in pre2_data_03:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
#            item['label'] = CATEGORY_LABELS[ item['category'] ]
#            data03.append(item)
#    if '03' in COLORS:
#        colors03 = COLORS['03']
#    else:
#        colors03 = []
    data03, colors03, title03 = plot('03', query)


    ### User selected a site - Top sites > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'A'
    query['category'] = 'A'
    ###     Plot 4: [User selected a site] on Jobs - Top sites > 1 %
#    data04 = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobcount', \
#                    label_cols=['site', 'cloud'], label_translation=False, \
#                    order_by=['cloud', 'site'])
    data04, colors04, title04 = plot('04', query)

    ###     Plot 5: [User selected a site] on jobDef - Top sites > 1 %
#    data05 = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobdefcount', \
#                    label_cols=['site', 'cloud'], label_translation=False, \
#                    order_by=['cloud', 'site'])
    data05, colors05, title05 = plot('05', query)

    ###     Plot 6: [User selected a site] on jobSet - Top sites > 1 %
#    data06 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_06 = DailyLog.objects.filter(**query).distinct('jobset').values('site', 'cloud').annotate(sum=Count('jobset')).order_by('cloud', 'site')
#        total_data_06 = sum([x['sum'] for x in pre_data_06])
#        for item in pre_data_06:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data06.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_06 = DailyLog.objects.filter(**query).values('site', 'cloud', 'jobset').order_by('cloud', 'site')
#        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_06]))
#        pre2_data_06 = []
#        total_data_06 = 0
#        for category, cat2 in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_06 if x['site'] == category]))
#            pre2_data_06.append({'site': category, 'cloud': cat2, 'sum': len(jobsets_for_category)})
#            total_data_06 += len(jobsets_for_category)
#        for item in pre2_data_06:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data06.append(item)
    data06, colors06, title06 = plot('06', query)


#    ### User selected a site - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'A'
    query['category'] = 'A'
    ###     Plot 7: [User selected a site] on Jobs - Per cloud
#    data07 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
#                    label_cols=['cloud'], label_translation=False)
    data07, colors07, title07 = plot('07', query)

    ###     Plot 8: [User selected a site] on jobDef - Per cloud
#    data08 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
#                    label_cols=['cloud'], label_translation=False)
    data08, colors08, title08 = plot('08', query)

    ###     Plot 9: [User selected a site] on jobSet - Per cloud
#    data09 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_09 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
#        total_data_09 = sum([x['sum'] for x in pre_data_09])
#        for item in pre_data_09:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_09)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data09.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_09 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
#        categories = list(set([ x['cloud'] for x in pre_data_09]))
#        pre2_data_09 = []
#        total_data_09 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_09 if x['cloud'] == category]))
#            print 'Category:', category, 'Jobsets:', jobsets_for_category
#            pre2_data_09.append({'cloud': category, 'sum': len(jobsets_for_category)})
#            total_data_09 += len(jobsets_for_category)
#        for item in pre2_data_09:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_09)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data09.append(item)
    data09, colors09, title09 = plot('09', query)



###    ### User selected a cloud - Top sites > 1 %
##    query = {}
##    ### filter logdate__range
##    query['logdate__range'] = [startdate, enddate]
##    ### filter category == 'B'
##    query['category'] = 'B'
##    ###     Plot 10: [User selected a cloud] on Jobs - Top sites > 1 %
##    data10 = data_plot_groupby_category(query, values=['category', 'site'], sum_param='jobcount', \
##                    label_cols=['site'], label_translation=False)
#
##    ###     Plot 11: [User selected a cloud] on jobDef - Top sites > 1 %
##    data11 = data_plot_groupby_category(query, values=['category', 'site'], sum_param='jobdefcount', \
##                    label_cols=['site'], label_translation=False)
##
##    ###     Plot 12: [User selected a cloud] on jobSet - Top sites > 1 %
##    data12 = []
##    try:
##        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
##        pre_data_12 = DailyLog.objects.filter(**query).distinct('jobset').values('site').annotate(sum=Count('jobset'))
##        total_data_12 = sum([x['sum'] for x in pre_data_12])
##        for item in pre_data_12:
##            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_12)
##            item['label'] = item['site']
##            item['name'] = item['site']
##            data12.append(item)
##    except NotImplementedError:
##        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
##        pre_data_12 = DailyLog.objects.filter(**query).values('site', 'jobset')
##        categories = list(set([ x['site'] for x in pre_data_12]))
##        pre2_data_12 = []
##        total_data_12 = 0
##        for category in sorted(categories):
##            jobsets_for_category = list(set([x['jobset'] for x in pre_data_12 if x['site'] == category]))
##            print 'Category:', category, 'Jobsets:', jobsets_for_category
##            pre2_data_12.append({'site': category, 'sum': len(jobsets_for_category)})
##            total_data_12 += len(jobsets_for_category)
##        for item in pre2_data_12:
##            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_12)
##            item['label'] = item['site']
##            item['name'] = item['site']
##            data12.append(item)
##
##
##
##
    ### User selected a cloud - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'B'
    ###     Plot 13: [User selected a cloud] on Jobs - Per cloud
#    data13 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
#                    label_cols=['cloud'], label_translation=False)
    data13, colors13, title13 = plot('13', query)

    ###     Plot 14: [User selected a cloud] on jobDef - Per cloud
#    data14 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
#                    label_cols=['cloud'], label_translation=False)
    data14, colors14, title14 = plot('14', query)

    ###     Plot 15: [User selected a cloud] on jobSet - Per cloud
#    data15 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_15 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
#        total_data_15 = sum([x['sum'] for x in pre_data_15])
#        for item in pre_data_15:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data15.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_15 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
#        categories = list(set([ x['cloud'] for x in pre_data_15]))
#        pre2_data_15 = []
#        total_data_15 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_15 if x['cloud'] == category]))
#            pre2_data_15.append({'cloud': category, 'sum': len(jobsets_for_category)})
#            total_data_15 += len(jobsets_for_category)
#        for item in pre2_data_15:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data15.append(item)
    data15, colors15, title15 = plot('15', query)


    ### PanDA Brokerage decision - Top sites with share > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'C'
    ###     Plot 16: PanDA Brokerage decision on Jobs - Top sites with share > 1 %
#    data16 = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobcount', \
#                    label_cols=['site', 'cloud'], label_translation=False, \
#                    order_by=['cloud', 'site'])
    data16, colors16, title16 = plot('16', query)

    ###     Plot 17: PanDA Brokerage decision on JobDefs - Top sites with share > 1 %
#    data17 = data_plot_groupby_category(query, values=['category', 'site', 'cloud'], sum_param='jobdefcount', \
#                    label_cols=['site', 'cloud'], label_translation=False, \
#                    order_by=['cloud', 'site'])
    data17, colors17, title17 = plot('17', query)


    ### PanDA Brokerage decision  - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'C'
    query['category'] = 'C'
    ###     Plot 18: PanDA Brokerage decision  on Jobs - Per cloud
#    data18 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobcount', \
#                    label_cols=['cloud'], label_translation=False)
    data18, colors18, title18 = plot('18', query)

    ###     Plot 19: PanDA Brokerage decision  on jobDef - Per cloud
#    data19 = data_plot_groupby_category(query, values=['category', 'cloud'], sum_param='jobdefcount', \
#                    label_cols=['cloud'], label_translation=False)
    data19, colors19, title19 = plot('19', query)


    ### User excluded a site on distinct jobSet - With exclude / Without exclude
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['A', 'B', 'C', 'E']
    ###     Plot 20: User excluded a site on distinct jobSet - With exclude / Without exclude
#    data20 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_20 = DailyLog.objects.filter(**query).distinct('jobset').values('category').annotate(sum=Count('jobset'))
#        total_data_20 = sum([x['sum'] for x in pre_data_20])
#        pre2_data_20 = []
#        for item in [x for x in pre_data_20 if x['category'] == 'E']:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_20)
#            item['label'] = CATEGORY_LABELS[ 'E+' ]
#            data20.append(item)
#        not_excluded = [x for x in pre_data_20 if x['category'] != 'E']
#        for item in not_excluded[:1]:
#            item['percent'] = '%.2f%%' % (100.0 * sum([x['sum'] for x in not_excluded]) / total_data_20)
#            item['label'] = CATEGORY_LABELS[ 'E-' ]
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_20 = DailyLog.objects.filter(**query).values('category', 'jobset')
#        excluded = list(set([ x['jobset'] for x in pre_data_20 if x['category'] == 'E']))
#        not_excluded = list(set([ x['jobset'] for x in pre_data_20 if x['category'] != 'E']))
#        if len(excluded) + len(not_excluded) < 1:
#            percent_excluded = '%.2f%%' % (0.0)
#            percent_not_excluded = '%.2f%%' % (0.0)
#        else:
#            percent_excluded = '%.2f%%' % (100.0 * len(excluded) / (len(excluded) + len(not_excluded)))
#            percent_not_excluded = '%.2f%%' % (100.0 * len(not_excluded) / (len(excluded) + len(not_excluded)))
#        data20.append({'category': 'E', 'sum': len(excluded), \
#                       'percent': percent_excluded, \
#                       'label': CATEGORY_LABELS[ 'E+' ]\
#                       })
#        data20.append({'category': 'ABC', 'sum': len(not_excluded), \
#                       'percent': percent_not_excluded, \
#                       'label': CATEGORY_LABELS[ 'E-' ]\
#                       })
#    if '20' in COLORS:
#        colors20 = COLORS['20']
#    else:
#        colors20 = []
    data20, colors20, title20 = plot('20', query)


    ### User excluded a site on jobSet - Top sites with share > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['E']
    ###     Plot 21: User excluded a site on jobSet - Top sites with share > 1 %
#    data21 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_21 = DailyLog.objects.filter(**query).distinct('jobset').values('site', 'cloud').annotate(sum=Count('jobset')).order_by('cloud', 'site')
#        total_data_21 = sum([x['sum'] for x in pre_data_21])
#        for item in pre_data_21:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_21)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data21.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_21 = DailyLog.objects.filter(**query).values('site', 'cloud', 'jobset')
#        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_21]))
#        pre2_data_21 = []
#        total_data_21 = 0
#        for category, cat2 in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_21 if x['site'] == category]))
#            pre2_data_21.append({'site': category, 'cloud': cat2, 'sum': len(jobsets_for_category)})
#            total_data_21 += len(jobsets_for_category)
#        for item in pre2_data_21:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_21)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data21.append(item)
    data21, colors21, title21 = plot('21', query)

    ###     Plot 22: User excluded a site on distinct DnUser - Top sites with share > 1 %
#    data22 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_22 = DailyLog.objects.filter(**query).distinct('dnuser').values('site', 'cloud').annotate(sum=Count('dnuser')).order_by('cloud', 'site')
#        total_data_22 = sum([x['sum'] for x in pre_data_22])
#        for item in pre_data_22:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_22)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data22.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_22 = DailyLog.objects.filter(**query).values('site', 'cloud', 'dnuser')
#        categories = list(set([ (x['site'], x['cloud']) for x in pre_data_22]))
#        pre2_data_22 = []
#        total_data_22 = 0
#        for category, cat2 in sorted(categories):
#            dnusers_for_category = list(set([x['dnuser'] for x in pre_data_22 if x['site'] == category]))
#            pre2_data_22.append({'site': category, 'cloud': cat2, 'sum': len(dnusers_for_category)})
#            total_data_22 += len(dnusers_for_category)
#        for item in pre2_data_22:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_22)
#            item['label'] = '%s (%s)' % (item['site'], item['cloud'])
#            item['name'] = item['site']
#            data22.append(item)
    data22, colors22, title22 = plot('22', query)


    ### User excluded a site on jobSet - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['E']
    ###     Plot 23: User excluded a site on jobSet - Per cloud
#    data23 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_23 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset')).order_by('cloud')
#        total_data_23 = sum([x['sum'] for x in pre_data_23])
#        for item in pre_data_23:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_23)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data23.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_23 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
#        categories = list(set([ x['cloud'] for x in pre_data_23]))
#        pre2_data_23 = []
#        total_data_23 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_23 if x['cloud'] == category]))
#            pre2_data_23.append({'cloud': category, 'sum': len(jobsets_for_category)})
#            total_data_23 += len(jobsets_for_category)
#        for item in pre2_data_23:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_23)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data23.append(item)
    data23, colors23, title23 = plot('23', query)

    ###     Plot 24: User excluded a site on distinct DnUser - Per cloud
#    data24 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_24 = DailyLog.objects.filter(**query).distinct('dnuser').values('cloud').annotate(sum=Count('dnuser')).order_by('cloud')
#        total_data_24 = sum([x['sum'] for x in pre_data_24])
#        for item in pre_data_24:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_24)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data24.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_24 = DailyLog.objects.filter(**query).values('site', 'cloud', 'dnuser')
#        categories = list(set([ x['cloud'] for x in pre_data_24]))
#        pre2_data_24 = []
#        total_data_24 = 0
#        for category in sorted(categories):
#            dnusers_for_category = list(set([x['dnuser'] for x in pre_data_24 if x['cloud'] == category]))
#            pre2_data_24.append({'cloud': category, 'sum': len(dnusers_for_category)})
#            total_data_24 += len(dnusers_for_category)
#        for item in pre2_data_24:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_24)
#            item['label'] = item['cloud']
#            item['name'] = item['cloud']
#            data24.append(item)
    data24, colors24, title24 = plot('24', query)


    ### Submitted by Country (from UserDN)
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category__in
    query['category__in'] = ['A', 'B', 'C', 'E']
    ###     Plot 25: Jobs submitted by Country
#    data25 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_25 = DailyLog.objects.filter(**query).distinct('country').values('country', 'jobcount').annotate(sum=Sum('jobcount')).order_by('country')
#        total_data_25 = sum([x['sum'] for x in pre_data_25])
#        for item in pre_data_25:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_25)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data25.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_25 = DailyLog.objects.filter(**query).values('country', 'jobcount')
#        categories = list(set([ x['country'] for x in pre_data_25]))
#        pre2_data_25 = []
#        total_data_25 = 0
#        for category in sorted(categories):
#            jobsets_for_category = [x['jobcount'] for x in pre_data_25 if x['country'] == category]
#            pre2_data_25.append({'country': category, 'sum': sum(jobsets_for_category)})
#            total_data_25 += len(jobsets_for_category)
#        for item in pre2_data_25:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_25)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data25.append(item)
#    if '25' in COLORS:
#        colors25 = COLORS['25']
#    else:
#        colors25 = []
    data25, colors25, title25 = plot('25', query)


    ###     Plot 26: JobDefs submitted by Country
#    data26 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_26 = DailyLog.objects.filter(**query).distinct('country').values('country', 'jobdefcount').annotate(sum=Sum('jobdefcount')).order_by('country')
#        total_data_26 = sum([x['sum'] for x in pre_data_26])
#        for item in pre_data_26:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_26)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data26.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_26 = DailyLog.objects.filter(**query).values('country', 'jobdefcount')
#        categories = list(set([ x['country'] for x in pre_data_26]))
#        pre2_data_26 = []
#        total_data_26 = 0
#        for category in sorted(categories):
#            jobsets_for_category = [x['jobdefcount'] for x in pre_data_26 if x['country'] == category]
#            pre2_data_26.append({'country': category, 'sum': sum(jobsets_for_category)})
#            total_data_26 += len(jobsets_for_category)
#        for item in pre2_data_26:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_26)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data26.append(item)
#    if '26' in COLORS:
#        colors26 = COLORS['26']
#    else:
#        colors26 = []
    data26, colors26, title26 = plot('26', query)


    ###     Plot 27: JobSets submitted by Country
#    data27 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_27 = DailyLog.objects.filter(**query).distinct('jobset').values('country').annotate(sum=Count('jobset'))
#        total_data_27 = sum([x['sum'] for x in pre_data_27])
#        for item in pre_data_27:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_27)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data27.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_27 = DailyLog.objects.filter(**query).values('country', 'jobset')
#        categories = list(set([ x['country'] for x in pre_data_27]))
#        pre2_data_27 = []
#        total_data_27 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_27 if x['country'] == category]))
#            pre2_data_27.append({'country': category, 'sum': len(jobsets_for_category)})
#            total_data_27 += len(jobsets_for_category)
#        for item in pre2_data_27:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_27)
#            item['label'] = item['country']
#            item['name'] = item['country']
#            data27.append(item)
#    if '27' in COLORS:
#        colors27 = COLORS['27']
#    else:
#        colors27 = []
    data27, colors27, title27 = plot('27', query)


    ### set request response data
    data = { \
        'errors_GET': errors_GET,
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,

        'data01': prepare_data_for_piechart(data=data01, unit='jobs'),
        'title01': title01,
        'colors01': colors01,
        'data02': prepare_data_for_piechart(data=data02, unit='jobDefs'),
        'title02': title02,
        'colors02': colors02,
        'data03': prepare_data_for_piechart(data=data03, unit='jobSets'),
        'title03': title03,
        'colors03': colors03,

        'data04': prepare_data_for_piechart(data=data04, unit='jobs', cutoff=1.0),
        'title04': title04,
        'colors04': colors04,
        'data05': prepare_data_for_piechart(data=data05, unit='jobDefs'),
        'title05': title05,
        'colors05': colors05,
        'data06': prepare_data_for_piechart(data=data06, unit='jobSets'),
        'title06': title06,
        'colors06': colors06,

        'data07': prepare_data_for_piechart(data=data07, unit='jobs'),
        'title07': title07,
        'colors07': colors07,
        'data08': prepare_data_for_piechart(data=data08, unit='jobDefs'),
        'title08': title08,
        'colors08': colors08,
        'data09': prepare_data_for_piechart(data=data09, unit='jobSets'),
        'title09': title09,
        'colors09': colors09,
##
##        'data10': prepare_data_for_piechart(data=data10, unit='jobs', cutoff=1.0),
##        'title10': PLOT_TITLES['title10'],
##        'colors10': prepare_colors_for_piechart(data10, cutoff=1.0),
##        'data11': prepare_data_for_piechart(data=data11, unit='jobDefs'),
##        'title11': PLOT_TITLES['title11'],
##        'colors11': prepare_colors_for_piechart(data11),
##        'data12': prepare_data_for_piechart(data=data12, unit='jobSets'),
##        'title12': PLOT_TITLES['title12'],
##        'colors12': prepare_colors_for_piechart(data12),
##
        'data13': prepare_data_for_piechart(data=data13, unit='jobs'),
        'title13': title13,
        'colors13': colors13,
        'data14': prepare_data_for_piechart(data=data14, unit='jobDefs'),
        'title14': title14,
        'colors14': colors14,
        'data15': prepare_data_for_piechart(data=data15, unit='jobSets'),
        'title15': title15,
        'colors15': colors15,

        'data16': prepare_data_for_piechart(data=data16, unit='jobs', cutoff=1.0),
        'title16': title16,
        'colors16': colors16,
        'data17': prepare_data_for_piechart(data=data17, unit='jobDefs', cutoff=1.0),
        'title17': title17,
        'colors17': colors17,

        'data18': prepare_data_for_piechart(data=data18, unit='jobs'),
        'title18': title18,
        'colors18': colors18,
        'data19': prepare_data_for_piechart(data=data19, unit='jobDefs'),
        'title19': title19,
        'colors19': colors19,

        'data20': prepare_data_for_piechart(data=data20, unit='jobSets'),
        'title20': PLOT_TITLES['title20'],
        'colors20': colors20,

        'data21': prepare_data_for_piechart(data=data21, unit='jobSets', cutoff=1.0),
        'title21': title21,
        'colors21': colors21,
        'data22': prepare_data_for_piechart(data=data22, unit='UserDNs', cutoff=1.0),
        'title22': title22,
        'colors22': colors22,
        'data23': prepare_data_for_piechart(data=data23, unit='jobSets'),
        'title23': title23,
        'colors23': colors23,
        'data24': prepare_data_for_piechart(data=data24, unit='UserDNs'),
        'title24': title24,
        'colors24': colors24,

        'data25': prepare_data_for_piechart(data=data25, unit='jobs', cutoff=1.0),
        'title25': title25,
        'colors25': colors25,
        'data26': prepare_data_for_piechart(data=data26, unit='jobDefs', cutoff=1.0),
        'title26': title26,
        'colors26': colors26,
        'data27': prepare_data_for_piechart(data=data27, unit='jobSets', cutoff=1.0),
        'title27': title27,
        'colors27': colors27,

}
    return render_to_response('pbm/index.html', data, RequestContext(request))


