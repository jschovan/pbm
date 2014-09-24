"""
    pbm.views
    
"""
import logging
import pytz
from datetime import datetime, timedelta
from django.db.models import Count, Sum
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
#from django.core.urlresolvers import reverse
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
#from .utils import get_rucio_pfns_from_guids, fetch_file

from .models import DailyLog
from .utils import CATEGORY_LABELS, PLOT_TITLES, prepare_data_for_piechart

_logger = logging.getLogger('bigpandamon-pbm')

defaultDatetimeFormat = '%Y-%m-%d'

def index(request):
    """
        index -- pbm's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ndays = 8
    try:
        ndays = request.GET['ndays']
    except:
        ndays = 8
    print defaultDatetimeFormat

    ### start the query parameters
    query={}

    ### filter logdate__range
    startdate = datetime.utcnow() - timedelta(days=ndays)
    startdate = startdate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    enddate = datetime.utcnow() - timedelta(days=1)
    enddate = enddate.replace(tzinfo=pytz.utc).strftime(defaultDatetimeFormat)
    query['logdate__range'] = [startdate, enddate]

    ### filter category__in
    query['category__in'] = ['A', 'B', 'C']

#    ### User selected a site/User selected a cloud/Panda Brokerage decision
#    ###     Plot 1: [User selected a site/User selected a cloud/Panda Brokerage decision] on Jobs
#    pre_data_01 = DailyLog.objects.filter(**query).values('category').annotate(sum=Sum('jobcount'))
#    total_data_01 = sum([x['sum'] for x in pre_data_01])
#    data01 = []
#    for item in pre_data_01:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_01)
#        item['label'] = CATEGORY_LABELS[ item['category'] ]
#        data01.append(item)
#
#    ###     Plot 2: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobDef
#    pre_data_02 = DailyLog.objects.filter(**query).values('category').annotate(sum=Sum('jobdefcount'))
#    total_data_02 = sum([x['sum'] for x in pre_data_02])
#    data02 = []
#    for item in pre_data_02:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_02)
#        item['label'] = CATEGORY_LABELS[ item['category'] ]
#        data02.append(item)
#
#    ###     Plot 3: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobSet
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
#            print 'Category:', category, 'Jobsets:', jobsets_for_category
#            pre2_data_03.append({'category': category, 'sum': len(jobsets_for_category)})
#            total_data_03 += len(jobsets_for_category)
#        for item in pre2_data_03:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
#            item['label'] = CATEGORY_LABELS[ item['category'] ]
#            data03.append(item)
#
#
##    dataXX = DailyLog.objects.filter(**query).values('category', 'jobcount', 'jobdefcount', 'jobset')
#
#
#    ### User selected a site - Top sites > 1 %
#    query = {}
#    ### filter logdate__range
#    query['logdate__range'] = [startdate, enddate]
#    ### filter category == 'A'
#    query['category'] = 'A'
#    ###     Plot 4: [User selected a site] on Jobs - Top sites > 1 %
#    pre_data_04 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobcount'))
#    total_data_04 = sum([x['sum'] for x in pre_data_04])
#    data04 = []
#    for item in pre_data_04:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_04)
#        item['label'] = item['site']
#        data04.append(item)
#
#    ###     Plot 5: [User selected a site] on jobDef - Top sites > 1 %
#    pre_data_05 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobdefcount'))
#    total_data_05 = sum([x['sum'] for x in pre_data_05])
#    data05 = []
#    for item in pre_data_05:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_05)
#        item['label'] = item['site']
#        data05.append(item)
#
#    ###     Plot 6: [User selected a site] on jobSet - Top sites > 1 %
#    data06 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_06 = DailyLog.objects.filter(**query).distinct('jobset').values('site').annotate(sum=Count('jobset'))
#        total_data_06 = sum([x['sum'] for x in pre_data_06])
#        for item in pre_data_06:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
#            item['label'] = item['site']
#            data06.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_06 = DailyLog.objects.filter(**query).values('site', 'jobset')
#        categories = list(set([ x['site'] for x in pre_data_06]))
#        pre2_data_06 = []
#        total_data_06 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_06 if x['site'] == category]))
#            print 'Category:', category, 'Jobsets:', jobsets_for_category
#            pre2_data_06.append({'site': category, 'sum': len(jobsets_for_category)})
#            total_data_06 += len(jobsets_for_category)
#        for item in pre2_data_06:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
#            item['label'] = item['site']
#            data06.append(item)
#
#
#
#
##    ### User selected a site - Per cloud
#    query = {}
#    ### filter logdate__range
#    query['logdate__range'] = [startdate, enddate]
#    ### filter category == 'A'
#    query['category'] = 'A'
#    ###     Plot 7: [User selected a site] on Jobs - Per cloud
#    pre_data_07 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobcount'))
#    total_data_07 = sum([x['sum'] for x in pre_data_07])
#    data07 = []
#    for item in pre_data_07:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_07)
#        item['label'] = item['cloud']
#        data07.append(item)
#
#    ###     Plot 8: [User selected a site] on jobDef - Per cloud
#    pre_data_08 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobdefcount'))
#    total_data_08 = sum([x['sum'] for x in pre_data_08])
#    data08 = []
#    for item in pre_data_08:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_08)
#        item['label'] = item['cloud']
#        data08.append(item)
#
#    ###     Plot 9: [User selected a site] on jobSet - Per cloud
#    data09 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_09 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
#        total_data_09 = sum([x['sum'] for x in pre_data_09])
#        for item in pre_data_09:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_09)
#            item['label'] = item['cloud']
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
#            data09.append(item)
#
#
#
##    ### User selected a cloud - Top sites > 1 %
#    query = {}
#    ### filter logdate__range
#    query['logdate__range'] = [startdate, enddate]
#    ### filter category == 'B'
#    query['category'] = 'B'
#    ###     Plot 10: [User selected a cloud] on Jobs - Top sites > 1 %
#    pre_data_10 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobcount'))
#    total_data_10 = sum([x['sum'] for x in pre_data_10])
#    data10 = []
#    for item in pre_data_10:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_10)
#        item['label'] = item['site']
#        data10.append(item)

#    ###     Plot 11: [User selected a cloud] on jobDef - Top sites > 1 %
#    pre_data_11 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobdefcount'))
#    total_data_11 = sum([x['sum'] for x in pre_data_11])
#    data11 = []
#    for item in pre_data_11:
#        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_11)
#        item['label'] = item['site']
#        data11.append(item)
#
#    ###     Plot 12: [User selected a cloud] on jobSet - Top sites > 1 %
#    data12 = []
#    try:
#        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
#        pre_data_12 = DailyLog.objects.filter(**query).distinct('jobset').values('site').annotate(sum=Count('jobset'))
#        total_data_12 = sum([x['sum'] for x in pre_data_12])
#        for item in pre_data_12:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_12)
#            item['label'] = item['site']
#            data12.append(item)
#    except NotImplementedError:
#        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
#        pre_data_12 = DailyLog.objects.filter(**query).values('site', 'jobset')
#        categories = list(set([ x['site'] for x in pre_data_12]))
#        pre2_data_12 = []
#        total_data_12 = 0
#        for category in sorted(categories):
#            jobsets_for_category = list(set([x['jobset'] for x in pre_data_12 if x['site'] == category]))
#            print 'Category:', category, 'Jobsets:', jobsets_for_category
#            pre2_data_12.append({'site': category, 'sum': len(jobsets_for_category)})
#            total_data_12 += len(jobsets_for_category)
#        for item in pre2_data_12:
#            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_12)
#            item['label'] = item['site']
#            data12.append(item)
#
#
#
#
    ### User selected a cloud - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'B'
    ###     Plot 13: [User selected a cloud] on Jobs - Per cloud
    pre_data_13 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobcount'))
    print pre_data_13
    total_data_13 = sum([x['sum'] for x in pre_data_13])
    data13 = []
    for item in pre_data_13:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_13)
        item['label'] = item['cloud']
        data13.append(item)

    ###     Plot 14: [User selected a cloud] on jobDef - Per cloud
    pre_data_14 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobdefcount'))
    total_data_14 = sum([x['sum'] for x in pre_data_14])
    data14 = []
    for item in pre_data_14:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_14)
        item['label'] = item['cloud']
        data14.append(item)

    ###     Plot 15: [User selected a cloud] on jobSet - Per cloud
    data15 = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_15 = DailyLog.objects.filter(**query).distinct('jobset').values('cloud').annotate(sum=Count('jobset'))
        total_data_15 = sum([x['sum'] for x in pre_data_15])
        for item in pre_data_15:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
            item['label'] = item['cloud']
            data15.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_15 = DailyLog.objects.filter(**query).values('cloud', 'jobset')
        categories = list(set([ x['cloud'] for x in pre_data_15]))
        pre2_data_15 = []
        total_data_15 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_15 if x['cloud'] == category]))
            print 'Category:', category, 'Jobsets:', jobsets_for_category
            pre2_data_15.append({'cloud': category, 'sum': len(jobsets_for_category)})
            total_data_15 += len(jobsets_for_category)
        for item in pre2_data_15:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_15)
            item['label'] = item['cloud']
            data15.append(item)


    ### PanDA Brokerage decision - Top sites with share > 1 %
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'B'
    query['category'] = 'C'
    ###     Plot 16: PanDA Brokerage decision on Jobs - Top sites with share > 1 %
    pre_data_16 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobcount'))
    total_data_16 = sum([x['sum'] for x in pre_data_16])
    data16 = []
    for item in pre_data_16:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_16)
        item['label'] = item['site']
        data16.append(item)

    ###     Plot 17: PanDA Brokerage decision on JobDefs - Top sites with share > 1 %
    pre_data_17 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobdefcount'))
    total_data_17 = sum([x['sum'] for x in pre_data_17])
    data17 = []
    for item in pre_data_17:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_17)
        item['label'] = item['site']
        data17.append(item)


    ### PanDA Brokerage decision  - Per cloud
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'C'
    query['category'] = 'C'
    ###     Plot 18: PanDA Brokerage decision  on Jobs - Per cloud
    pre_data_18 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobcount'))
    print pre_data_18
    total_data_18 = sum([x['sum'] for x in pre_data_18])
    data18 = []
    for item in pre_data_18:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_18)
        item['label'] = item['cloud']
        data18.append(item)

    ###     Plot 19: PanDA Brokerage decision  on jobDef - Per cloud
    pre_data_19 = DailyLog.objects.filter(**query).values('category', 'cloud').annotate(sum=Sum('jobdefcount'))
    total_data_19 = sum([x['sum'] for x in pre_data_19])
    data19 = []
    for item in pre_data_19:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_19)
        item['label'] = item['cloud']
        data19.append(item)




    ### set request response data
    data = { \
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,
#        'data01': prepare_data_for_piechart(data=data01, unit='jobs'),
#        'title01': PLOT_TITLES['title01'],
#        'data02': prepare_data_for_piechart(data=data02, unit='jobDefs'),
#        'title02': PLOT_TITLES['title02'],
#        'data03': prepare_data_for_piechart(data=data03, unit='jobSets'),
#        'title03': PLOT_TITLES['title03'],
#
#        'data04': prepare_data_for_piechart(data=data04, unit='jobs', cutoff=1.0),
#        'title04': PLOT_TITLES['title04'],
#        'data05': prepare_data_for_piechart(data=data05, unit='jobDefs'),
#        'title05': PLOT_TITLES['title05'],
#        'data06': prepare_data_for_piechart(data=data06, unit='jobSets'),
#        'title06': PLOT_TITLES['title06'],
#
#        'data07': prepare_data_for_piechart(data=data07, unit='jobs'),
#        'title07': PLOT_TITLES['title07'],
#        'data08': prepare_data_for_piechart(data=data08, unit='jobDefs'),
#        'title08': PLOT_TITLES['title08'],
#        'data09': prepare_data_for_piechart(data=data09, unit='jobSets'),
#        'title09': PLOT_TITLES['title09'],
#
#        'data10': prepare_data_for_piechart(data=data10, unit='jobs', cutoff=1.0),
#        'title10': PLOT_TITLES['title10'],
#        'data11': prepare_data_for_piechart(data=data11, unit='jobDefs'),
#        'title11': PLOT_TITLES['title11'],
#        'data12': prepare_data_for_piechart(data=data12, unit='jobSets'),
#        'title12': PLOT_TITLES['title12'],
#
#        'data13': prepare_data_for_piechart(data=data13, unit='jobs'),
#        'title13': PLOT_TITLES['title13'],
#        'data14': prepare_data_for_piechart(data=data14, unit='jobDefs'),
#        'title14': PLOT_TITLES['title14'],
#        'data15': prepare_data_for_piechart(data=data15, unit='jobSets'),
#        'title15': PLOT_TITLES['title15'],
#
        'data16': prepare_data_for_piechart(data=data16, unit='jobs', cutoff=1.0),
        'title16': PLOT_TITLES['title16'],
        'data17': prepare_data_for_piechart(data=data17, unit='jobDefs', cutoff=1.0),
        'title17': PLOT_TITLES['title17'],

        'data18': prepare_data_for_piechart(data=data18, unit='jobs'),
        'title18': PLOT_TITLES['title18'],
        'data19': prepare_data_for_piechart(data=data19, unit='jobDefs'),
        'title19': PLOT_TITLES['title19'],

#        'dataXX': dataXX,

}
    return render_to_response('pbm/index.html', data, RequestContext(request))


