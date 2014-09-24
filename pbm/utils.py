"""
    pbm.utils
    
"""
import logging
_logger = logging.getLogger('bigpandamon-pbm')


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

}


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


