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
        finaldata = []
        conn = sqlite3.connect(db_path)
        # '''创建游标'''
        cursor = conn.cursor()
        sql = ( 
            ' SELECT datetime( s."时间", "unixepoch", "localtime" ) AS "下线绑定时间",'
            ' c."微信名字" AS "上级微信",'
            ' s."上级对应ID",'
            ' c."推广奖励" as "上级推广奖励",'
            ' datetime( c."注册时间", "unixepoch", "localtime" ) AS "上级注册时间",'
            ' s."下级对应ID",'
            ' d."微信名字" AS "下级微信", '
            ' d."推广奖励" as "下级推广奖励",'
            ' datetime( d."注册时间", "unixepoch", "localtime" ) AS "下级注册时间",'
            ' c."总成功订单" AS "上级总成功订单",'
            ' c."总提现金额" AS "上级总提现金额",'
            ' d."总成功订单" AS "下级总成功订单",'
            ' d."总提现金额" AS "下级总提现金额",'
            ' datetime( b."时间", "unixepoch", "localtime" ) AS "下级订单时间",'
            ' b."商品ID" as "下级购买商品ID",'
            ' b."付费金额" as "下级付费金额" , '
            ' b."买家佣金" as "下级买家佣金",'
            ' b."推广佣金" as "下级推广佣金",'
            ' b."商品标题",'
            ' b."联盟佣金比例",'
            ' b."联盟佣金",'
            ' b."预计收入" as "下级预计收入",'
            ' b."状态" as "订单状态",'
            ' b."类目" AS "购物平台" '
            ' FROM 上下级管理 s '
            ' LEFT JOIN 订单管理 b ON s."下级对应ID" = b."对应ID" '
            ' LEFT JOIN 会员信息 c ON s."上级对应ID" = c."对应ID" ' 
            ' LEFT JOIN 会员信息 d ON s."下级对应ID" = d."对应ID" '
            ' ORDER BY s."上级对应ID", '
            ' b."对应ID"'	)
        # print(sql)
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
        filename = folder_path + '_L_User_orders_' + filetime + '_.xls'
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
            # alimama =title_dic[str( value)]
            dbfolder = str(value)
        # if name == "-s":
        #     start_date = str(value)
        # if name == "-e":
        #     end_date = str(value)

    # start = int(
    #     time.mktime(
    #         time.strptime(
    #             datetime.datetime.strptime(
    #                 start_date, '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S"),
    #             "%Y-%m-%d %H:%M:%S")))
    # end = int(
    #     time.mktime(
    #         time.strptime(
    #             datetime.datetime.strptime(
    #                 end_date, '%Y-%m-%d').strftime("%Y-%m-%d %H:%M:%S"),
    #             "%Y-%m-%d %H:%M:%S")))

    exp = Export()
    files = exp.read_folder(dbfolder)
    if len(files) == 0:
        print('未找到机器人数据库文件')
    for f in files:
        datas = exp.read_database(f)
        if len(datas) > 1:
            exp.write_excel(f, datas)
