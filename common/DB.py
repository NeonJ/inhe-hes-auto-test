# -*- coding: UTF-8 -*-
import psycopg2
import psycopg2.extras
import cx_Oracle
import os
import yaml
import json
import datetime


# import cx_Oracle
# conn = psycopg2.connect(database="ami_db", user="ami", password="ami", host="10.32.233.146", port="5557")
# print("Opened database successfully")
#
# cur = conn.cursor()
# cur.execute("SELECT *  from c_ar_meter")
# rows = cur.fetchall()
# for row in rows:
#     print(row)
# conn.close()

try:
    cx_Oracle.init_oracle_client(lib_dir=r"E:\Tool\instantclient-basic-nt-19.12.0.0.0dbru\instantclient_19_12")
except Exception as err:
    print("Whoops! cx_Oracle 32bit failed")
    print(err)

class DB:

    def __init__(self, **kwargs):
        self.source = kwargs['source']
        self.host = kwargs['host']
        self.database = kwargs['database']
        self.username = kwargs['username']
        self.passwd = kwargs['passwd']
        self.port = kwargs['port']
        self.sid = kwargs['sid']

    def connect(self):
        if self.source == 'Postgre':
            try:
                return psycopg2.connect(database=self.database, user=self.username, password=self.passwd,
                                        host=self.host, port=self.port)
            except Exception as e:
                print("get error: %s" % e)
        elif self.source == 'Oracle':
            try:
                dsn_tns = cx_Oracle.makedsn(self.host, self.port, self.sid)
                # 如果是Oracle 12c 数据库需要替换sid 为service_name
                dsn_tns = dsn_tns.replace('SID', 'SERVICE_NAME')
                conn = cx_Oracle.connect(self.username, self.passwd, dsn_tns)
                return conn
            except Exception as e:
                print("get error: %s" % e)

    def fetchall(self, sql):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def fetchall_dict(self, sql):
        try:
            con = self.connect()
            cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql)
            fc = cur.fetchall()
            fc1 = []
            for row in fc:
                fc1.append(dict(row))
            return fc1
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def orcl_fetchall_dict(self, sql):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(sql)
            fc = cur.fetchall()
            cols = [d[0] for d in cur.description]
            fc1 = []
            for row in fc:
                b = dict(zip(cols, row))
                fc1.append(b)
            return fc1
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def fetchone(self, sql):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(sql)
            fc = cur.fetchone()
            return fc
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def fetchone_dict(self, sql):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(sql)
            fc = cur.fetchone()
            return fc
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def save_result(self, table_name, result_type, result, register_id):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = f"update {table_name} set {result_type}='{json.dumps(result)}' where register_id='{register_id}'"
            # print(sql)
            cur.execute(sql)
            con.commit()
            return
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def read_config(file_path):
        """读取配置文件内容"""
        with open(file_path, encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config

    def initial_result(self, meter_no):
        """初始化OBIS Check结果表"""
        table_name = 'h_ptl_register_check_' + datetime.datetime.now().strftime('%Y%m%d%H%M')
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(
                f"create table {table_name} as select * from h_ptl_register where device_type=1 and ptl_type =(select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no='{meter_no}'))")
            cur.execute(f"alter table {table_name} add get_result varchar(128)")
            cur.execute(f"alter table {table_name} add get_value varchar(1280)")
            cur.execute(f"alter table {table_name} add set_result varchar(128)")
            cur.execute(f"alter table {table_name} add set_value varchar(128)")
            cur.execute(f"alter table {table_name} add action_result varchar(128)")
            cur.execute(f"alter table {table_name} add action_value varchar(128)")
            cur.execute(f"alter table {table_name} add default_value varchar(1024)")
            con.commit()
            return table_name
        except Exception as e:
            print("initial check result error: %s" % e)
        finally:
            cur.close()
            con.close()

    def find_last_result(self):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = "select tablename from pg_tables where tablename like 'h_ptl_register_check%' order by tablename desc limit 1"
            cur.execute(sql)
            fc = cur.fetchone()
            return fc
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def orcl_find_last_result(self):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = "select table_name from user_tables where table_name like 'H_PTL_REGISTER_CHECK%' and ROWNUM=1 order by table_name desc"
            cur.execute(sql)
            fc = cur.fetchone()
            return fc
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

if __name__ == '__main__':
    file_path = os.path.abspath(f"conf/DefaultValue/tulip/user.yaml")
    user_config = DB.read_config(file_path)
    db_queue = DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
                  database=user_config['Database']['database'], username=user_config['Database']['username'],
                  passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
                  sid=user_config['Database']['sid']).fetchall_dict(
        "select register_id,class_id,attribute_id,register_desc,is_method,data_type,rw from H_PTL_REGISTER where PTL_TYPE = (select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no='1KFM5600000003'))")
    print(db_queue)

    DB(source=user_config['Database']['source'], host=user_config['Database']['host'],
       database=user_config['Database']['database'], username=user_config['Database']['username'],
       passwd=user_config['Database']['passwd'], port=user_config['Database']['port'],
       sid=user_config['Database']['sid']).save_result('set_result', {
        "dataItemType": 16,
        "dataItemValue": "-60"
    }, '0.0.1.0.0.255830')

    # class MyOracle:
    #     SHOW_SQL = True
    #
    #     def __init__(self, host='127.0.0.1', port=1521, user='system', password='oracle', sid='cndba'):
    #         self.host = host
    #         self.port = port
    #         self.user = user
    #         self.password = password
    #         self.sid = sid
    #
    #     def get_con(self):
    #         try:
    #             dsn_tns = cx_Oracle.makedsn(self.host, self.port, self.sid)
    #             # 如果是Oracle 12c 数据库需要替换sid 为service_name
    #             dsn_tns = dsn_tns.replace('SID', 'SERVICE_NAME')
    #             conn = cx_Oracle.connect(self.user, self.password, dsn_tns)
    #             return conn
    #         except cx_Oracle.Error as e:
    #             print(e)
    #
    #     def select_all(self, sql):
    #         try:
    #             con = self.get_con()
    #             # print con
    #             cur = con.cursor()
    #             cur.execute(sql)
    #             fc = cur.fetchall()
    #             return fc
    #         except cx_Oracle.Error as e:
    #             print(e)
    #         finally:
    #             cur.close()
    #             con.close()
    #
    #     def select_by_where(self, sql, data):
    #         try:
    #             con = self.get_con()
    #             # print con
    #             d = (data,)
    #             cur = con.cursor()
    #             cur.execute(sql, d)
    #             fc = cur.fetchall()
    #             # if len(fc) > 0:
    #             #     for e in range(len(fc)):
    #             #         print(fc[e])
    #             return fc
    #         except cx_Oracle.Error as e:
    #             print(e)
    #         finally:
    #             cur.close()
    #             con.close()
    #
    #     def dml_by_where(self, sql, params):
    #         try:
    #             con = self.get_con()
    #             cur = con.cursor()
    #
    #             for d in params:
    #                 if self.SHOW_SQL:
    #                     print('执行sql:[{}],参数:[{}]'.format(sql, d))
    #                 cur.execute(sql, d)
    #             con.commit()
    #
    #         except cx_Oracle.Error as e:
    #             print(e)
    #         finally:
    #             cur.close()
    #             con.close()
    #
    #     # 不带参数的更新方法
    #     def dml_nowhere(self, sql):
    #         try:
    #             con = self.get_con()
    #             cur = con.cursor()
    #             count = cur.execute(sql)
    #             con.commit()
    #             return count
    #         except cx_Oracle.Error as e:
    #             print(e)
    #         finally:
    #             cur.close()
    #             con.close()
    #
    #
    # if __name__ == '__main__':
    #     A(host="***",
    #       db="***",
    #       user="***",
    #       pwd="***",
    #       port="***")
