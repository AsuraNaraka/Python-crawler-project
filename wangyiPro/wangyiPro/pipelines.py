# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 在管道类的process_item中要将其接收到的item对象中存储的数据进行持久化存储操作(5)
class WangyiproPipeline:
    # def process_item(self, item, spider):
    #     print(item)
    #     return item

    fp = None
    def open_spider(self,spider):
        print('开始爬虫....' + '\n' + '###############################################')
        self.fp = open('./wangyi.csv', 'w', encoding='utf-8')

    # 专门用来处理 item 类型对象
    # 该方法可以接收爬虫文件提交过来的item对象
    # 该方法没接收到一个item就会被调用一次
    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        self.fp.write(title + ':\n' + content + '\n' + '\n')
        print('正在下载: ' + title)

        return item  # 就会传递给下一个即将被执行的管道类

    def close_spider(self, spider):
        print('结束爬虫！' + '\n' + '###############################################')
        self.fp.close()
