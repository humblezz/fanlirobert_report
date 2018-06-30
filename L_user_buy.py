import sqlite3
import xlwt
import getopt
import os
import sys
import datetime
import time

filetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Export(object):
    def read_database(self, db_path, start, end):
        finaldata = []
        conn = sqlite3.connect(db_path)
        # '''创建游标'''
        cursor = conn.cursor()
        sql = ( 
            ' select  COUNT(w.LVL) as "总订单数",w.LVL  from ( '
            ' SELECT '
            '		 CASE WHEN z."总订单数" BETWEEN 1  AND 4 THEN "L--A" '
            ' WHEN z."总订单数" BETWEEN 5  AND 50 THEN "L--S" '
            ' WHEN z."总订单数" BETWEEN 51 AND 100 THEN"L--SS" '
            ' WHEN z."总订单数" > 100 THEN	"L--SSS" ELSE "L" END AS "LVL" '
            ' FROM '
            ' 	(	SELECT s."下级对应ID",h."总订单数" 	FROM	上下级管理 s '
            ' LEFT JOIN (	SELECT COUNT( b."订单编号" ) AS "总订单数",	b."对应ID"  '
            ' FROM	( SELECT DISTINCT a."订单编号", a."对应ID" FROM 订单管理 a ) b 	GROUP BY	b."对应ID" )'
            '	  h ON s."下级对应ID" = h."对应ID" 		'
            ' where s."时间">= ' + str(start) + ' AND  s."时间"<=  ' + str(end) +
            ') z			) w'
            ' GROUP BY w.LVL;'	)
        print(sql)
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
    def write_excel(self, folder_path, data):
        filename = folder_path + '_L_User_Buy_' + filetime + '_.xls'
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
    if len(files) == 0:
        print('未找到机器人数据库文件')
    for f in files:
        datas = exp.read_database(f, start, end)
        if len(datas) > 1:
            exp.write_excel(f, datas)
