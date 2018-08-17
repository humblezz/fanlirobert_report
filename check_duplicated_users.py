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
        sql = ('select  "'+fanligo_name+'" as fligo, a."��ӦID",a."΢������",a."�ܳɹ�����",a."�����ֽ��",a."δ�ջ����",a."�����ֽ��",a."ǩ������",a."ǩ������",a."�ƹ㽱��",a."�������",datetime( a."ע��ʱ��", "unixepoch", "localtime" ) as ע��ʱ��,b."�ϼ���ӦID" ,datetime( b."ʱ��", "unixepoch", "localtime" )  as ��ʱ��   from  ��Ա��Ϣ a LEFT JOIN   ���¼����� b on a."��ӦID" = b."�¼���ӦID" order by b."�ϼ���ӦID",b."ʱ��" ')
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
            table_defined = 'CREATE TABLE "All_Users" ("id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "fligo" TEXT, "��ӦID" TEXT, "΢������" TEXT, "�ܳɹ�����" INTEGER, "�����ֽ��" INTEGER, "δ�ջ����" INTEGER, "�����ֽ��" INTEGER, "ǩ������" INTEGER, "ǩ������" INTEGER, "�ƹ㽱��" INTEGER, "�������" INTEGER, "ע��ʱ��" TEXT, "�ϼ���ӦID" text, "��ʱ��" TEXT)'
            corsor.execute(table_defined)
        
        # for data in datas:
        #     corsor.execute('insert INTO All_Users("fligo","��ӦID","΢������","�ܳɹ�����","�����ֽ��","δ�ջ����","�����ֽ��","ǩ������","ǩ������","�ƹ㽱��","�������",ע��ʱ��,"�ϼ���ӦID","��ʱ��") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
        # conn.commit()

        corsor.executemany('insert INTO All_Users("fligo","��ӦID","΢������","�ܳɹ�����","�����ֽ��","δ�ջ����","�����ֽ��","ǩ������","ǩ������","�ƹ㽱��","�������",ע��ʱ��,"�ϼ���ӦID","��ʱ��") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datas)
        conn.commit()
        corsor.close()
        conn.close()

    def get_duplicateUsers(sqlf, db_combine_path):
        sql = ('select allu.counter as "�ظ�����",b.* from (select a."��ӦID",count(a.id) as "counter" from All_Users  a  GROUP BY a."��ӦID" HAVING COUNT(a.id)>1 order by count(a.id)) allu left join All_Users  b on allu."��ӦID"=b."��ӦID"')
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

    # д��excel
    def write_excel(self, folder_path, data):
        filename = os.path.join(folder_path, '_duplicate_user_' + filetime + '_.xls')
        wb = xlwt.Workbook()
        sheet = wb.add_sheet(filetime)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                sheet.write(i, j, data[i][j])
        wb.save(filename)
        print("д�����ݳɹ���" + filename)

    def read_folder(self, folder_path):
        db_all = []
        for parent, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.db':
                    file_path = os.path.join(parent, filename)
                    db_all.append(file_path)
        return db_all


if __name__ == '__main__':

    # __opts, _ = getopt.getopt(sys.argv[1:], "f:s:e:", ["folder=", "start=", "end="])  # ��ȡ�����в���
    __opts, _ = getopt.getopt(sys.argv[1:], "f:", ["folder="])  # ��ȡ�����в���
    dbfolder = ''
    start_date = ''
    end_date = ''

    for name, value in __opts:
        if name == "-f":  # ��ȡ�����в���e
            dbfolder = str(value)
 
    db_combine_path = os.path.join(dbfolder, 'combind_db.fix')
    if os.path.exists(db_combine_path):
        os.remove(db_combine_path)
        
    exp = Export()
    files = exp.read_folder(dbfolder)
    if len(files) == 0:
        print('δ�ҵ����������ݿ��ļ�')

    for f in files:
        datas = exp.read_database(f)
        if len(datas) > 1:
            exp.writeToDB(datas, db_combine_path)

    duplicate_users = exp.get_duplicateUsers(db_combine_path)
    exp.write_excel(dbfolder, duplicate_users)
    



            
