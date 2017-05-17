# -*- coding: UTF-8 -*-
# @file   memcache
# @author zh1995
# @date   17-5-15
# @brief
import memcache

mcache= memcache.Client(['127.0.0.1:11211'])
print mcache.set('say', 'hello,memcache', 60) #display - True
value = mcache.get('say')
print value #display - hello,memcache
