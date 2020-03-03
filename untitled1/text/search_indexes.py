#定义索引类
from haystack import indexes

#导入模型类
from text.models import TextContext

#指定对于某个类的某些数据建立索引
#格式 模型类名加index
class TextContextIndex(indexes.SearchIndex, indexes.Indexable):
    #索引字段，use_template=True指定根据表的哪些字段建立索引文件，把说明放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return TextContext

    #建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()