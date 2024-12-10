# coding:utf-8
import lxbasic.core as bsc_core


cache = bsc_core.LRUCache()

cache.set('a', 1)
cache.set('b', 2)
cache.set('c', 3)

print 'a' in cache
print(cache)  # 输出: LRUCache(OrderedDict([('a', 1), ('b', 2), ('c', 3)]))

cache.get('a')  # 访问 'a'，将其移到最后
print(cache)  # 输出: LRUCache(OrderedDict([('b', 2), ('c', 3), ('a', 1)]))

cache.set('d', 4)  # 插入 'd'，导致最旧的 'b' 被移除
print(cache)  # 输出: LRUCache(OrderedDict([('c', 3), ('a', 1), ('d', 4)]))
