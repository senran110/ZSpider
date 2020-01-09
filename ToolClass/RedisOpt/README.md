### Redis 

### 一、数据类型

|类型					|场景(例子)	|操作(例子)	|  操作成功返回   |
|-						|-		|-		|  -  |
|String（字符串）		| 计数/粉丝数		|	r.set('name', 'jun')	|  True  |
|List（列表）			| 粉丝列表/消息队列/最新内容		|	r.lpush("0",1,2,3,4) 	|  列表长度  |
|Hash（字典）			| 用户信息/关系型数据库的映射		|	r.hset(name, key, value) 	|  1  |
|Set（集合）			|	共同关注/共同喜好（取交集）	|	r.sadd("name", 1,2)	|  集合长度  |
|Sorted Set（有序集合）	|	积分排行榜/好友亲密度	|	r.zadd('zz', {'n1': 1, 'n2': 2})	|  集合长度  |

### 二、常见操作

Bitmap：通过比特位来表示某个元素对应的值或者状态

应用场景：

1、用户签到

2、统计活跃用户

3、用户在线状态

| 操作 | 例子 | 说明 |
| - | - | - |
| SETBIT | SETBIT key offset value | 对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit),当 key 不存在时，自动生成一个新的字符串值。|
| GETBIT | GETBIT key offset | 字符串值指定偏移量上的位(bit) |


### 补充一
redis连接时加上参数decode_responses=True，写入的键值对中的value为str类型若不加这个参数写入的则为字节类型。
```
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
```
