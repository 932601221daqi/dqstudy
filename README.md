# dqstudy
此项目是一个在线学习编程的网站。采用了Django1.11版本，目前还没有掌握vue所以没有用rest_framewok。  
使用了本地的mysql数据库和虚拟机上的redis数据库。将celery运行在了虚拟机上。  
# dqstudy包含两大app，为user和text.  
## &nbsp;&nbsp; user模块包含：注册、登陆、用户中心  
### &nbsp;&nbsp;&nbsp;&nbsp; 注册：采用了Django的认证模块，和celery分布式队列进行一个用户注册邮件的异步分发。  
### &nbsp;&nbsp;&nbsp;&nbsp; 登陆：采用Django的认证模块，进行登陆的验证，使用login和logout对用户进行状态的保持。  
### &nbsp;&nbsp; 用户中心：使用了Redis数据库作为缓存，用户浏览文章时添加记录作为历史记录，使用了list类型  
## &nbsp;&nbsp;&nbsp;&nbsp; text模块包含：查找、学习。  
### &nbsp;&nbsp;&nbsp;&nbsp; 学习:进行相关课程类型的查找，通过分页返回title列表展示，供自行选择。使用模板渲染防止转义safe过滤器。  
### &nbsp;&nbsp;&nbsp;&nbsp; 搜索：使用了haystack全文检索框架和whoosh搜索引擎，jieba进行分词处理。以title作为索引生成，进行检索和查询的操作。  
text的表结构设计为两张表，一个是类型表(id,type)，另一个信息表（id,title,content,type_id)。的关系，在使用中发现centent过多查询很慢，我觉得应该建三张表：类型表(id,type)、信息表（id,title、type_id）、文本表(id,content,text_id)减少数据库查询的压力。在表结构设计经验还是不足。勉励。  
前端部分：没有设计。之前学习的html,js,jquery,bootstrop大部分不会写了，但是能看懂。难受，知识不复习等于没学会！  
dqstudy是我自己学习django框架知识汇总写的一个项目。  
大琦加油！！  
