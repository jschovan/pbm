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
}

PLOT_TITLES = {
    'title01': 'User selected a site/User selected a cloud/PanDA Brokerage decision on Jobs', \
    'title02': 'User selected a site/User selected a cloud/PanDA Brokerage decision on jobDef', \
    'title03': 'User selected a site/User selected a cloud/PanDA Brokerage decision on jobSet', \
}


def prepare_data_for_piechart(data, unit='jobs'):
    """
        prepare_data_for_piechart
        
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
    for item in data:
        piechart_data.append([ '%s (%s %s)' % (item['label'], item['sum'], unit), item['sum']])
    return piechart_data


