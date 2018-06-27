import sqlite3
import xlwt
import getopt
import os
import sys
import datetime

filetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


class Export(object):
    def read_database(self, db_path):
        finaldata = []
        conn = sqlite3.connect(db_path)
        # '''创建游标'''
        cursor = conn.cursor()
        sql = (
            'select COUNT(d.LVL) as count,d.LVL FROM'
            '(select  CASE   when  c."总成功订单" BETWEEN 1 AND 4  THEN "A"  when  c."总成功订单" BETWEEN 5 AND 50  THEN "S"'
            'when  c."总成功订单" BETWEEN 51 AND 100  THEN "SS" '
            'when  c."总成功订单" >100  THEN "SSS"'
            'else "BC"'
            'END as "LVL"'
            'FROM 会员信息 c'
            ' where c."对应ID" not in (SELECT "下级对应ID" from 上下级管理)'
            ') d '
            'GROUP BY d.LVL '
            'union  '
            'select COUNT(e.LVL) as count,e.LVL FROM (	SELECT  CASE   when  h."总成功订单" BETWEEN 1 AND 4  THEN "L--A" when  h."总成功订单" BETWEEN 5 AND 50  THEN "L--S" '
            'when  h."总成功订单" BETWEEN 51 AND 100  THEN "L--SS" '
            'when  h."总成功订单" >100  THEN "L--SSS"'
            'else "L"'
            'END as "LVL"'
            'from   上下级管理 c'
            ' LEFT JOIN 会员信息 h on h."对应ID"=c."下级对应ID"      ) e GROUP BY e.LVL')
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
        filename = folder_path + '_客户分类报表—_' + filetime + '_.xls'
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

    __opts, _ = getopt.getopt(sys.argv[1:], "f:", ["folder="])  # 获取命令行参数
    dbfolder = ''

    for name, value in __opts:
        if name == "-f":  # 获取命令行参数e
            # alimama =title_dic[str( value)]
            dbfolder = str(value)
    exp = Export()
    files = exp.read_folder(dbfolder)

    for f in files:
        datas = exp.read_database(f)
        if len(datas) > 1:
            exp.write_excel(f, datas)
