# coding:utf-8
from collections import OrderedDict

class LRUCache:
    def __init__(self, max_size):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, key):
        """获取缓存内容"""
        if key in self.cache:
            # 模拟 move_to_end 的行为：删除后重新插入
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def set(self, key, value):
        """设置缓存内容"""
        if key in self.cache:
            # 删除后重新插入（更新现有的值并将其移到最后）
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # 如果缓存满了，移除最旧的一项
            self.cache.popitem(last=False)
        self.cache[key] = value

    def __repr__(self):
        """返回缓存内容的字符串表示"""
        return "LRUCache({})".format(self.cache)


# 使用示例
cache = LRUCache(max_size=3)
cache.set('a', 1)
cache.set('b', 2)
cache.set('c', 3)
print(cache)  # 输出: LRUCache(OrderedDict([('a', 1), ('b', 2), ('c', 3)]))

cache.get('a')  # 访问 'a'，将其移到最后
print(cache)  # 输出: LRUCache(OrderedDict([('b', 2), ('c', 3), ('a', 1)]))

cache.set('d', 4)  # 插入 'd'，导致最旧的 'b' 被移除
print(cache)  # 输出: LRUCache(OrderedDict([('c', 3), ('a', 1), ('d', 4)]))
