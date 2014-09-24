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

    ### debug jobDefCount vs jobSet
#    query['jobset__in'] = ['Ahmed_A._Hasib|22021', 'Benjamin_Tannenwald|2080', 'Steven_Schramm|30219', 'Tony_Kwan_skc-881|5783']

    ### User selected a site/User selected a cloud/Panda Brokerage decision
    ###     Plot 1: [User selected a site/User selected a cloud/Panda Brokerage decision] on Jobs
    pre_data_01 = DailyLog.objects.filter(**query).values('category').annotate(sum=Sum('jobcount'))
    total_data_01 = sum([x['sum'] for x in pre_data_01])
    data01 = []
    for item in pre_data_01:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_01)
        item['label'] = CATEGORY_LABELS[ item['category'] ]
        data01.append(item)

    ###     Plot 2: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobDef
    pre_data_02 = DailyLog.objects.filter(**query).values('category').annotate(sum=Sum('jobdefcount'))
    total_data_02 = sum([x['sum'] for x in pre_data_02])
    data02 = []
    for item in pre_data_02:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_02)
        item['label'] = CATEGORY_LABELS[ item['category'] ]
        data02.append(item)

    ###     Plot 3: [User selected a site/User selected a cloud/Panda Brokerage decision] on jobSet
    data03 = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_03 = DailyLog.objects.filter(**query).distinct('jobset').values('category').annotate(sum=Count('jobset'))
        total_data_03 = sum([x['sum'] for x in pre_data_03])
        for item in pre_data_03:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
            item['label'] = CATEGORY_LABELS[ item['category'] ]
            data03.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_03 = DailyLog.objects.filter(**query).values('category', 'jobset')
        categories = list(set([ x['category'] for x in pre_data_03]))
        pre2_data_03 = []
        total_data_03 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_03 if x['category'] == category]))
            print 'Category:', category, 'Jobsets:', jobsets_for_category
            pre2_data_03.append({'category': category, 'sum': len(jobsets_for_category)})
            total_data_03 += len(jobsets_for_category)
        for item in pre2_data_03:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_03)
            item['label'] = CATEGORY_LABELS[ item['category'] ]
            data03.append(item)


#    dataXX = DailyLog.objects.filter(**query).values('category', 'jobcount', 'jobdefcount', 'jobset')


#    ### User selected a site
    query = {}
    ### filter logdate__range
    query['logdate__range'] = [startdate, enddate]
    ### filter category == 'A'
    query['category'] = 'A'
    ###     Plot 4: [User selected a site] on Jobs
    pre_data_04 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobcount'))
    print pre_data_04
    total_data_04 = sum([x['sum'] for x in pre_data_04])
    data04 = []
    for item in pre_data_04:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_04)
        item['label'] = item['site']
        data04.append(item)

    ###     Plot 5: [User selected a site] on jobDef
    pre_data_05 = DailyLog.objects.filter(**query).values('category', 'site').annotate(sum=Sum('jobdefcount'))
    total_data_05 = sum([x['sum'] for x in pre_data_05])
    data05 = []
    for item in pre_data_05:
        item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_05)
        item['label'] = item['site']
        data05.append(item)

    ###     Plot 6: [User selected a site] on jobSet
    data06 = []
    try:
        ### TODO: FIXME: check that this pre_data_03 queryset works on MySQL and Oracle
        pre_data_06 = DailyLog.objects.filter(**query).distinct('jobset').values('site').annotate(sum=Count('jobset'))
        total_data_06 = sum([x['sum'] for x in pre_data_06])
        for item in pre_data_06:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
            item['label'] = item['site']
            data06.append(item)
    except NotImplementedError:
        ### This is queryset and aggregation for SQLite3 backend, as .distinct('jobset') raises NotImplementedError on SQLite3
        pre_data_06 = DailyLog.objects.filter(**query).values('site', 'jobset')
        categories = list(set([ x['site'] for x in pre_data_06]))
        pre2_data_06 = []
        total_data_06 = 0
        for category in sorted(categories):
            jobsets_for_category = list(set([x['jobset'] for x in pre_data_06 if x['site'] == category]))
            print 'Category:', category, 'Jobsets:', jobsets_for_category
            pre2_data_06.append({'site': category, 'sum': len(jobsets_for_category)})
            total_data_06 += len(jobsets_for_category)
        for item in pre2_data_06:
            item['percent'] = '%.2f%%' % (100.0 * item['sum'] / total_data_06)
            item['label'] = item['site']
            data06.append(item)


    ### set request response data
    data = { \
        'startdate': startdate,
        'enddate': enddate,
        'ndays': ndays,
        'data01': prepare_data_for_piechart(data=data01, unit='jobs'),
        'title01': PLOT_TITLES['title01'],
        'data02': prepare_data_for_piechart(data=data02, unit='jobDefs'),
        'title02': PLOT_TITLES['title02'],
        'data03': prepare_data_for_piechart(data=data03, unit='jobSets'),
        'title03': PLOT_TITLES['title03'],
##        'dataXX': dataXX,
        'data04': prepare_data_for_piechart(data=data04, unit='jobs', cutoff=1.0),
        'title04': PLOT_TITLES['title04'],
        'data05': prepare_data_for_piechart(data=data05, unit='jobDefs'),
        'title05': PLOT_TITLES['title05'],
        'data06': prepare_data_for_piechart(data=data06, unit='jobSets'),
        'title06': PLOT_TITLES['title06'],
    }
    return render_to_response('pbm/index.html', data, RequestContext(request))


