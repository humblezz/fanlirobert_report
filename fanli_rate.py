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
            ' select d.counter as "推广首单数量",e.* FROM (select a."上级对应ID", COUNT(c."对应ID" ) as counter from 上下级管理 a '
            ' left join ( select DISTINCT(b."对应ID"),b."状态" from "订单管理" b '
            ' where b."状态"="交易成功") c '
            ' on a."下级对应ID"=c."对应ID"   '
            ' where c."对应ID" is not NULL  '
            ' GROUP BY a."上级对应ID"  '
            ' ORDER BY a."上级对应ID"  ) d '
            ' left join 会员信息 e '
            ' on d."上级对应ID"=e."对应ID" '
            'where d.counter>=3')
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
        filename = folder_path + '_客户返利比例—_' + filetime + '_.xls'
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
