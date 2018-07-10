import psycopg2
from scrapy.utils.project import get_project_settings

from scrapy_wssc import BookItem


def __init__(self):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    settings = get_project_settings()

    self.connection = psycopg2.connect(
        database=settings.get('POSTGRES_DB'),
        user=settings.get('POSTGRES_USER'),
        password=settings.get('POSTGRES_PW'),
        host=settings.get('POSTGRES_SERVER'),
        port=settings.get('POSTGRES_PORT'),
    )
    self.cursor = self.connection.cursor()


def process_item(self, item, spider):
    if isinstance(item, BookItem):
        _sql = """INSERT INTO BitautoCar(carid,url,treeurl,brand,brandurl,brandmodel4,brandmodel5,version,image,cyear,ctype,color,price1,price2,displacement,shiftgears,shifttype,clength,cwidth,cheight,wheelbase,mingrounddistance,motor,intaketype,maxhorsepower,maxpower,maxrpm,oiltype,oilsupply,tankvolume,drivetype,braketype,frontwheel,backwheel) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" % (
        item['carid'], item['url'], item['treeurl'], item['brand'], item['brandurl'], item['brandmodel4'],
        item['brandmodel5'], item['version'], item['image'], item['cyear'], item['ctype'], item['color'],
        item['price1'], item['price2'], item['displacement'], item['shiftgears'], item['shifttype'], item['clength'],
        item['cwidth'], item['cheight'], item['wheelbase'], item['mingrounddistance'], item['motor'],
        item['intaketype'], item['maxhorsepower'], item['maxpower'], item['maxrpm'], item['oiltype'], item['oilsupply'],
        item['tankvolume'], item['drivetype'], item['braketype'], item['frontwheel'], item['backwheel'])

    try:
        self.cursor.execute(self.cursor.mogrify(_sql))
        self.connection.commit()

    except Exception, e:
        self.connection.rollback()
        print "Error: %s" % e

    return item