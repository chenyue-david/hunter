from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlencode

url = ('http://www.dm5.com/manhua-jinjidejuren/')
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent } 
req = Request(url, None, headers)

try:
   response = urlopen(req, timeout = 10)
except URLError, e:  
  if hasattr(e, 'reason'):  
    print 'We failed to reach a server.'  
    print 'Reason: ', e.reason  
  elif hasattr(e, 'code'):  
    print 'The server couldn\'t fulfill the request.'  
    print 'Error code: ', e.code  
  else:  
    print 'No exception was raised.'  

print response.read()
