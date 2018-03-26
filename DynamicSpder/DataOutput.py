import pymysql


class DataOutput(object):


    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                    passwd='smj19960827', db='mtime', charset='utf8')
        self.cur = self.conn.cursor()
        self.create_table('MTime')
        self.datas = []

    def create_table(self, table_name):
        values = '''
        id int not null auto_increment primary key,
        MovieId int,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal float NOT NULL DEFAULT 0.0,
        ROtherFinal float NOT NULL DEFAULT 0.0,
        RPictureFinal float NOT NULL DEFAULT 0.0,
        RDirectorFinal float NOT NULL DEFAULT 0.0,
        RStoryFinal float NOT NULL DEFAULT 0.0,
        Usercount int NOT NULL DEFAULT 0,
        AttitudeCount int NOT NULL DEFAULT 0,
        TotalBoxOffice varchar(20) NOT NULL,
        TodayBoxOffice varchar(20) NOT NULL,
        Rank int NOT NULL DEFAULT 0,
        ShowDays int NOT NULL DEFAULT 0,
        isRelease int NOT NULL
        '''
        self.cur.execute('use mtime')
        self.cur.execute('create table %s (%s)' % (table_name, values))
        self.conn.commit()

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas)>10:
            self.output_db('MTime')

    def output_db(self, table_name):
        for data in self.datas:
            sql = '''
            INSERT INTO `MTime` (`MovieId`,`MovieTitle`,`RatingFinal`,`ROtherFinal`,`RPictureFinal`,`RDirectorFinal`,`RStoryFinal`,`Usercount`,`AttitudeCount`,`TotalBoxOffice`,`TodayBoxOffice`,`Rank`,`ShowDays`,`isRelease`) VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s)
            ''' % data
            self.cur.execute(sql)
            self.datas.remove(data)
        self.conn.commit()

    def output_end(self):
        if len(self.datas)>0:
            self.output_db('MTime')
        self.cur.close()
        self.conn.close()
