#coding=gbk
import sqlite3
import xlwt
import getopt
import os
import sys
import datetime
import time

filetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Export(object):
    def read_database(self, db_path): 
        conn = sqlite3.connect(db_path)
        fanligo_name = os.path.basename(db_path)
        cursor = conn.cursor()
        sql = ('select  "'+fanligo_name+'" as fligo, a."对应ID",a."微信名字",a."总成功订单",a."总提现金额",a."未收货金额",a."可提现金额",a."签到次数",a."签到奖励",a."推广奖励",a."定向比例",datetime( a."注册时间", "unixepoch", "localtime" ) as 注册时间,b."上级对应ID" ,datetime( b."时间", "unixepoch", "localtime" )  as 绑定时间   from  会员信息 a LEFT JOIN   上下级管理 b on a."对应ID" = b."下级对应ID" order by b."上级对应ID",b."时间" ')
        print(fanligo_name)
        results = cursor.execute(sql)
        all_tixian = results.fetchall() 
        cursor.close() 
        conn.close()
        return all_tixian

    def writeToDB(self, datas, dbpath):      
        isCreateTable = os.path.exists(dbpath)
        conn = sqlite3.connect(dbpath)
        corsor = conn.cursor()
        if not isCreateTable: 
            table_defined = 'CREATE TABLE "All_Users" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "fligo" TEXT, "对应ID" TEXT, "微信名字" TEXT, "总成功订单" INTEGER, "总提现金额" INTEGER, "未收货金额" INTEGER, "可提现金额" INTEGER, "签到次数" INTEGER, "签到奖励" INTEGER, "推广奖励" INTEGER, "定向比例" INTEGER, "注册时间" TEXT, "上级对应ID" text, "绑定时间" TEXT)'
            corsor.execute(table_defined)
        
        # for data in datas:
        #     corsor.execute('insert INTO All_Users("fligo","对应ID","微信名字","总成功订单","总提现金额","未收货金额","可提现金额","签到次数","签到奖励","推广奖励","定向比例",注册时间,"上级对应ID","绑定时间") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
        # conn.commit()

        corsor.executemany('insert INTO All_Users("fligo","对应ID","微信名字","总成功订单","总提现金额","未收货金额","可提现金额","签到次数","签到奖励","推广奖励","定向比例",注册时间,"上级对应ID","绑定时间") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datas)
        conn.commit()
        corsor.close()
        conn.close()

    def get_duplicateUsers(sqlf, db_combine_path):
        sql = ('select allu.counter as "重复次数",b.* from (select a."对应ID",count(a.id) as "counter" from All_Users  a  GROUP BY a."对应ID" HAVING COUNT(a.id)>1 order by count(a.id)) allu left join All_Users  b on allu."对应ID"=b."对应ID"')
        finaldata = []
        conn = sqlite3.connect(db_combine_path) 
        cursor = conn.cursor()
        results = cursor.execute(sql)
        all_tixian = results.fetchall()
        allfields = []
        fields = cursor.description
        for field in range(0, len(fields)):
            allfields.append(fields[field][0])
        cursor.close()
        conn.close()
        finaldata.append(allfields)
        for tixian in all_tixian:
            finaldata.append(tixian)
        return finaldata

    # 写入excel
    def write_excel(self, folder_path, data):
        filename = os.path.join(folder_path, '_duplicate_user_' + filetime + '_.xls')
        wb = xlwt.Workbook()
        sheet = wb.add_sheet(filetime)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                sheet.write(i, j, data[i][j])
        wb.save(filename)
        print("写入数据成功！" + filename)

    def read_folder(self, folder_path):
        db_all = []
        for parent, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.db':
                    file_path = os.path.join(parent, filename)
                    db_all.append(file_path)
        return db_all


if __name__ == '__main__':

    # __opts, _ = getopt.getopt(sys.argv[1:], "f:s:e:", ["folder=", "start=", "end="])  # 获取命令行参数
    __opts, _ = getopt.getopt(sys.argv[1:], "f:", ["folder="])  # 获取命令行参数
    dbfolder = ''
    start_date = ''
    end_date = ''

    for name, value in __opts:
        if name == "-f":  # 获取命令行参数e
            dbfolder = str(value)
 
    db_combine_path = os.path.join(dbfolder, 'combind_db.fix')
    if os.path.exists(db_combine_path):
        os.remove(db_combine_path)
        
    exp = Export()
    files = exp.read_folder(dbfolder)
    if len(files) == 0:
        print('未找到机器人数据库文件')

    for f in files:
        datas = exp.read_database(f)
        if len(datas) > 1:
            exp.writeToDB(datas, db_combine_path)

    duplicate_users = exp.get_duplicateUsers(db_combine_path)
    exp.write_excel(dbfolder, duplicate_users)
    



            
