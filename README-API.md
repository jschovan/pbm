PanDA Brokerage Monitor API
=====

PanDA Brokerage Monitor (pbm) is a simple Django app to visualize brokerage decisions 
of PanDA Workload Management System in a set of piechart plots and tables. 

For more information please see https://github.com/PanDAWMS/panda-bigmon-brokerage .

API: ?type=XYZ
-----------
The 'type' parameter is compulsory.

There are optional parameters: 
* 'nhours' to show last N hours worth of log entries. Please note that max(nhours)=10*24. Default value is 'nhours'=6.
* 'starttime' and 'endtime' as desired time range boundaries, expected format is datetime.datetime.isoformat().

**N.B.** 'nhours' has higher priority, therefore if 'nhours' is specified, 'starttime' and 'endtime' are not taken into account. 
If 'nhours' is not specified and neither is 'starttime', 'starttime' is set to (datetime.datetime.utcnow()-timedelta(hours=6)). 
If 'nhours' is not specified and neither is 'endtime', 'endtime' is set to datetime.datetime.utcnow(). 

The API has 3 HTTP return states: 200, 404, 400.

**200 OK**: _type_ was provided, log file found in DB, no errors while downloading.

**404 NOT FOUND**: _type_ was provided (but does not exist), or no PanDA logger record found for that type and time range. Example of returned error message:
  ```
'errors': {'lookup': 'Log record for parameters has not been found. 
                      query={'type': u'analy_brokerage', 
                      'time__range': ['2014-10-11 14:49:44', '2014-10-12 14:49:44'], 
                      'bintime__range': ['2014-10-11 14:49:44', '2014-10-12 14:49:44']}' 
}
  ```
**400 BAD REQUEST**:

* When _type_ has not been provided, following error message is produced:
  ```
'errors': {'missingparameter': 'Missing expected GET parameter type. '}
  ```
* For another error the error dictionary contains keys _lookup_.


In any case, the data dictionary with the following keys is returned in the response: 
  ```
'GET_parameters'  ... dictionary of request.GET,
'query'        ... QuerySet filter parameter used to retrieve PanDA logger records, 
'nrecords'        ... integer specifies how many PanDA logger records have been found, 
'data'       ... list of PanDA logger records found, 
'timestamp'  ... datetime in isoformat, time when the response has been sent,
'errors'     ... dictionary with list of errors encountered, 
'warnings'   ... dictionary with list of warnings encountered, e.g. when an optional parameter is missing.
  ```


**Example usage**:

Successful pass, only 'type' specified:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' \
  "http://HOSTNAME/pbm/api/?type=analy_brokerage"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /pbm/api/?type=analy_brokerage HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 200 OK
< Date: Sun, 12 Oct 2014 15:10:15 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
[data not shown]
{'timestamp': '2014-10-12T15:10:15.641547', 'GET_parameters': {u'type': 'analy_brokerage'}, 
'query': {'time__range': ['2014-10-11 15:10:15', '2014-10-12 15:10:15'], 'type': u'analy_brokerage', 
          'bintime__range': ['2014-10-11 15:10:15', '2014-10-12 15:10:15']}, 
'errors': {}, 
'warnings': {'missingoptionalparameter': 'Missing optional GET parameter starttime. Missing optional GET parameter endtime. Missing optional GET parameter nhours. '}, 
'nrecords': 1208, 
'data': [{'bintime': '2014-10-11T23:15:46', 'pid': 0, 'module': u'broker', 'line': 298, 
          'message': u"dn=\\'SomeUserDN\\' : jobset=6040 jobdef=6042 : nJobs=20 countryGroup=de", 
          'name': u'panda.mon.prod', 'loglevel': 20, 'filename': u'broker.py', 'loguser': u'', 'time': u'2014-10-11 23:15:46', 
          'type': u'analy_brokerage', 'levelname': u'INFO'}, ... ]
}
* Closing connection #0
  
  ```


Successful pass, 'type' and 'nhours' specified:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' \
  "http://HOSTNAME/pbm/api/?type=analy_brokerage&nhours=1"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /pbm/api/?type=analy_brokerage&nhours=1 HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNMAE
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 200 OK
< Date: Sun, 12 Oct 2014 15:16:18 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
[data not shown]
{'timestamp': '2014-10-12T15:16:18.911275', 'GET_parameters': {u'type': 'analy_brokerage', u'nhours': '1'}, 
'query': {'time__range': ['2014-10-11 15:16:18', '2014-10-12 15:16:18'], 'type': u'analy_brokerage', 
          'bintime__range': ['2014-10-11 15:16:18', '2014-10-12 15:16:18']}
'errors': {}, 
'warnings': {'missingoptionalparameter': 'Missing optional GET parameter starttime. Missing optional GET parameter endtime. '}, 
'nrecords': 1191, 
'data': [{'bintime': '2014-10-11T23:15:46', 'pid': 0, 'module': u'broker', 'line': 298, 
          'message': u"dn=\\'SomeUserDN\\' : jobset=6040 jobdef=6042 : nJobs=20 countryGroup=de", 
          'name': u'panda.mon.prod', 'loglevel': 20, 'filename': u'broker.py', 'loguser': u'', 'time': u'2014-10-11 23:15:46', 
          'type': u'analy_brokerage', 'levelname': u'INFO'}, ... ]
}
* Closing connection #0
  
  ```


Successful pass, 'type' and 'starttime' and 'endtime' specified:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' \
  "http://HOSTNAME/pbm/api/?type=analy_brokerage&starttime=2014-10-12T09:00:00&endtime=2014-10-12T13:00:00"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /pbm/api/?type=analy_brokerage&starttime=2014-10-12T09:00:00&endtime=2014-10-12T13:00:00 HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 200 OK
< Date: Sun, 12 Oct 2014 15:20:29 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
[data not shown]
{'timestamp': '2014-10-12T15:20:29.617126', 
'GET_parameters': {u'type': 'analy_brokerage', u'endtime': '2014-10-12T13:00:00', u'starttime': '2014-10-12T09:00:00'}
'query':  {'time__range': ['2014-10-12 09:00:00', '2014-10-12 13:00:00'], 'type': u'analy_brokerage', 
           'bintime__range': ['2014-10-12 09:00:00', '2014-10-12 13:00:00']}
'errors': {}, 
'warnings': {'missingoptionalparameter': 'Missing optional GET parameter nhours. '}, 
'nrecords': 31, 
'data': [{'bintime': '2014-10-12T12:59:13', 'pid': 0, 'module': u'broker', 'line': 298, 
          'message': u"dn=\\'SomeUserDN\\' : jobset=3210 jobdef=5543 : nJobs=20 countryGroup=us", 
          'name': u'panda.mon.prod', 'loglevel': 20, 'filename': u'broker.py', 'loguser': u'', 'time': u'2014-10-12 12:59:13', 
          'type': u'analy_brokerage', 'levelname': u'INFO'}, ... ]
}
* Closing connection #0
  
  ```


Missing _type_ parameter:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' \
  "http://HOSTNAME/pbm/api/?type="
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /pbm/api/?type= HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 400 BAD REQUEST
< Date: Sun, 12 Oct 2014 15:28:30 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
{ [data not shown]
{'timestamp': '2014-10-12T15:28:30.705011', 
'GET_parameters': {u'type': ''}, 
'errors': {'lookup': "Log record for parameters has not been found. 
                      {'type': None, 
                       'time__range': ['2014-10-11 15:28:30', '2014-10-12 15:28:30'], 
                       'bintime__range': ['2014-10-11 15:28:30', '2014-10-12 15:28:30']}", 
           'missingparameter': 'Missing expected GET parameter type. '}, 
'warnings': {'missingoptionalparameter': 'Missing optional GET parameter starttime. Missing optional GET parameter endtime. Missing optional GET parameter nhours. '}, 
'query': {'time__range': ['2014-10-11 15:28:30', '2014-10-12 15:28:30'], 'type': None, 
          'bintime__range': ['2014-10-11 15:28:30', '2014-10-12 15:28:30']}, 
'nrecords': 0, 'data': []}
* Closing connection #0

  ```


Non-existing _type_:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' \
  "http://HOSTNAME/pbm/api/?type=blah"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /pbm/api/?type=blah HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 404 NOT FOUND
< Date: Sun, 12 Oct 2014 15:31:46 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
{ [data not shown]
{'timestamp': '2014-10-12T15:31:46.697476', 
'GET_parameters': {u'type': 'blah'}, 
'errors': {'lookup': "Log record for parameters has not been found. 
                      {'time__range': ['2014-10-11 15:31:46', '2014-10-12 15:31:46'], 'type': u'blah', 
                       'bintime__range': ['2014-10-11 15:31:46', '2014-10-12 15:31:46']}"}, 
'warnings': {'missingoptionalparameter': 'Missing optional GET parameter starttime. Missing optional GET parameter endtime. Missing optional GET parameter nhours. '}, 
'query': {'time__range': ['2014-10-11 15:31:46', '2014-10-12 15:31:46'], 'type': u'blah', 
          'bintime__range': ['2014-10-11 15:31:46', '2014-10-12 15:31:46']}, 
'nrecords': 0, 'data': []}
* Closing connection #0



