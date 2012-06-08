## checks arxiv feed

import urllib
import datetime
from os import mkdir

now=datetime.datetime.utcnow()
time='{0}'.format(now.strftime('%Y%m%d_%H%M'))
mkdir(time)

urllib.urlretrieve("http://windmill.herokuapp.com/tools/women/division/",time+'/women.html')
urllib.urlretrieve("http://windmill.herokuapp.com/tools/open/division/",time+'/open.html')
urllib.urlretrieve("http://windmill.herokuapp.com/tools/mixed/division/",time+'/mixed.html')


