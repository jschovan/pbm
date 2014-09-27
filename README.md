PanDA Brokerage Monitor (pbm)
=====

PanDA Brokerage Monitor (pbm) is a simple Django app to visualize brokerage decisions 
of PanDA Workload Management System in a set of piechart plots and tables. 

Default view plots data from the past week. Time range can be modified with URL parameters: 
* last N days: ?ndays=N,
* date range: ?startdate=2014-09-01&enddate=2014-09-27

Plots are created with the Highcharts (4.0.4) interactive JavaScript charts library, http://www.highcharts.com/.

PanDA Brokerage Monitor follows ATLAS Distributed Computing color scheme 
https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/ADCStandards.

Further documentation of PanDA Brokerage Monitor is available at 
https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/PandaBrokerageMonitor .


Quick start
-----------

1. Add "pbm" and "pbm.templatetags" to your INSTALLED_APPS setting like this:
  ```
INSTALLED_APPS = (
    ...
    'pbm',
    'pbm.templatetags',
    ....
)
  ``` 
  If you are using django.js in your site app, do not forget to update JS_I18N_APPS_EXCLUDE.

2. Add 'pbm' DB router to DATABASE_ROUTERS settings like this:
  ```
DATABASE_ROUTERS = ['pbm.dbrouter.PandaBrokerageMonDBRouter']
  ```

3. Add templates of "pbm" to TEMPLATE_DIRS setting like this:
  ```
import pbm
TEMPLATE_DIRS = (
    ...
    join(dirname(pbm.__file__), 'templates'),
    ...
)
  ```
  List pbm templates only after your Django site's templates, to allow for template extension.

4. Include the filebrowser URLconf in your project urls.py like this:
  ```
url(r'^pbm/', include('pbm.urls')),
  ```

5. Visit http://127.0.0.1:8000/pbm/ to view the PanDA Brokerage Monitor.

6. Run unit tests from your Django site area:
  ```
python manage.py test pbm.tests
  ```
