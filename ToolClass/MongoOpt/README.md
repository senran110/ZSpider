### MongoDB
代码借鉴自此[博文](https://blog.csdn.net/yangxiaodong88/article/details/80748972)
 
一、比较符号

|符号	|含义		|示例						|
| ---	| ---		| ---						|
|$lt	|小于		|{'age': {'$lt': 20}}		|
|$lte	|小于等于	|{'age': {'$lte': 20}}		|
|$gt	|大于		|{'age': {'$gt': 20}}		|
|$gte	|大于等于	|{'age': {'$gte': 20}}		|
|$ne	|不等于		|{'age': {'$ne': 20}}		|
|$in	|在范围内	|{'age': {'$in': [20, 23]}}	|
|$nin	|不在范围内	|{'age': {'$nin': [20, 23]}}|

二、功能符号

|符号	|含义			|示例												|示例含义						|
| ---	| ---			| ---												|   ---							|
|$regex	|匹配正则表达式	|{'name': {'$regex': '^M.*'}}						|以M开头的name					|
|$exists|属性是否存在	|{'name': {'$exists': True}}						|name属性存在					|
|$type	|类型判断		|{'age': {'$type': 'int'}}							|age的类型为int					|
|$mod	|数字模操作		|{'age': {'$mod': [5, 0]}}							|年龄模5余0						|
|$text	|文本查询		|{'$text': {'$search': 'Mike'}}						|text类型的属性中包含Mike字符串	|
|$where	|高级条件查询	|{'$where': 'obj.fans_count == obj.follows_count'}	|自身粉丝数等于关注数			|

### 思考一
关于pymongo连接池,搜索资料得知：

PyMongo是线程安全的,并且为多线程应用提供了内置的连接池,每个MongoClient实例在每个MongoDb服务器都有一个内置的连接池。