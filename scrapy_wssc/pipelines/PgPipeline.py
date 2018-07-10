import psycopg2
from scrapy.utils.project import get_project_settings

from scrapy_wssc.BookItem import BookItem

class PgPipeline(object):
    def __init__(self):
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        settings = get_project_settings()

        self.connection = psycopg2.connect(
            # database=settings.get('POSTGRES_DB'),
            # user=settings.get('POSTGRES_USER'),
            # password=settings.get('POSTGRES_PW'),
            # host=settings.get('POSTGRES_SERVER'),
            # port=settings.get('POSTGRES_PORT'),
            database='wsscdb',
            user='postgres',
             password='postgres',
             host='104.225.148.44',
             port='5432',
        )
        self.cursor = self.connection.cursor()


    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            _sql = """INSERT INTO t_book(id,cate_id,name,author,create_date,is_hot,is_serial,status,last_update,describe,book_url)
                  VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" % (
            item['id'], item['cateId'], item['name'], item['author'], item['create_date'], item['isHot'],
            item['isSerial'], item['status'],item['lastUpdate'], item['describe'], item['bookUrl'])

        try:
            self.cursor.execute(self.cursor.mogrify(_sql))
            self.connection.commit()

        except Exception, e:
            self.connection.rollback()
            print "Error: %s" % e

        return item