# -*- coding:utf-8 -*-
import os,sys,re
import string
reload(sys)
sys.setdefaultencoding('utf-8')
cnt = u'回复@咩咩的真爱小珍:你好'

print cnt
pattern = re.compile(u'回复@(.*):')
cnt = pattern.sub('', cnt)
# cnt = cnt.replace(u'回复(.*):','')
print cnt

id = 'C_4021944712268667'
patt = re.compile('C_(.*)')
test = patt.sub('1', id)
print id
print test