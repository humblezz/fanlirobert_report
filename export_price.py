import sqlite3
import xlwt
import getopt
import os
import sys
import time
import datetime


class Export(object):
    def read_database(self, db_path, start_date, end_date):
        finaldata = []
        conn = sqlite3.connect(db_path)
        # '''创建游标'''
        cursor = conn.cursor()
        sql = 'select * from  申请提现 c    where c."时间">={0} and  c."时间"<={1} '.format(
            start_date, end_date)
        results = cursor.execute(sql)
        all_tixian = results.fetchall()
        allfields = []
        fields = cursor.description
        for field in range(0, len(fields)):
            allfields.append(fields[field][0]) 
        cursor.close()
        finaldata.append(allfields)
        for tixian in all_tixian: 
            finaldata.append(tixian)
        return finaldata

    # 写入excel
    def write_excel(self, folder_path, data, start_date, end_date): 
        filename = folder_path + '_' + start_date + '_' + end_date + '.xls'
        wb = xlwt.Workbook()
        sheet = wb.add_sheet(start_date + '_' + end_date)
        for i in range(0, len(data)): 
            for j in range(0, len(data[i])):
                if j==0 and i>0:
                    sheet.write(i, j, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data[i][j]))) )
                else:
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

    __opts, _ = getopt.getopt(sys.argv[1:], "f:s:e:",
                              ["folder=", "start=", "end="])  # 获取命令行参数
    dbfolder = ''
    start_date = ''
    end_date = ''

    for name, value in __opts:
        if name == "-f":  # 获取命令行参数e
            # alimama =title_dic[str( value)]
            dbfolder = str(value)
        if name == "-s":
            start_date = str(value)
        if name == "-e":
            end_date = str(value)
 

    start = int(
        time.mktime(
            time.strptime(
                datetime.datetime.strptime(
                    start_date, '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S"),
                "%Y-%m-%d %H:%M:%S")))
    end = int(
        time.mktime(
            time.strptime(
                datetime.datetime.strptime(
                    end_date, '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S"),
                "%Y-%m-%d %H:%M:%S")))

 
    exp = Export()
    files = exp.read_folder(dbfolder)

    for f in files:
        datas = exp.read_database(f, start, end) 
        if len(datas) > 1:
            exp.write_excel(f, datas, start_date, end_date)
