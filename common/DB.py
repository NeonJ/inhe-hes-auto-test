"""
# File       : configs.py
# Time       : 2021/12/16 18:03
# Author     : 曹剑南
# version    : python 3.7
"""
import datetime
import json

import yaml

from common.YamlConfig import readConfig

import cx_Oracle
import nacos
import psycopg2
import psycopg2.extras


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

# try:
#     cx_Oracle.init_oracle_client(lib_dir=r"E:\Tool\instantclient-basic-nt-19.12.0.0.0dbru\instantclient_19_12")
# except Exception as err:
#     print("Whoops! cx_Oracle 32bit failed")
#     print(err)

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
        else:
            print("数据库类型不支持")

    def fetchall_dict(self, sql):
        if self.source == 'Postgre':
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

        elif self.source == 'Oracle':
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
        else:
            print("数据库类型不支持")

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
            cols = [d[0] for d in cur.description]
            print(cols)
            print(fc)
            fc1 = []
            for row in fc:
                b = dict(zip(cols, row))
                fc1.append(b)
                print(fc1)
            return fc1
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def save_result(self, table_name, result_column, result, value_column, value, elapsed, register_id):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = f"update {table_name} set {result_column}='{json.dumps(result)}',{value_column}='{json.dumps(value)}',elapsed='{elapsed}' where register_id='{register_id}'"
            cur.execute(sql)
            con.commit()
            return
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def update(self, sql):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def initial_result(self, meter_no):
        """初始化OBIS Check结果表"""
        table_name = 'H_CONFIG_REGISTER_CHECK_' + str(meter_no) + '_' + datetime.datetime.now().strftime('%y%m%d')
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute(
                f"create table {table_name} as select * from H_CONFIG_REGISTER where  ptl_type =(select PTL_TYPE from c_ar_model where MODEL_CODE = (select model_code from c_ar_meter where meter_no='{meter_no}'))")
            cur.execute(f"alter table {table_name} add get_result varchar(128)")
            cur.execute(f"alter table {table_name} add get_value varchar(1280)")
            cur.execute(f"alter table {table_name} add set_result varchar(128)")
            cur.execute(f"alter table {table_name} add set_value varchar(128)")
            cur.execute(f"alter table {table_name} add action_result varchar(128)")
            cur.execute(f"alter table {table_name} add action_value varchar(128)")
            cur.execute(f"alter table {table_name} add default_value varchar(1024)")
            cur.execute(f"alter table {table_name} add elapsed varchar(128)")
            con.commit()
            return table_name
        except Exception as e:
            print("initial check result error: %s" % e)
        finally:
            cur.close()
            con.close()

    def last_result(self, meter_no):
        if self.source == 'Postgre':
            meter_no = str(meter_no).lower()
            try:
                con = self.connect()
                cur = con.cursor()
                sql = f"select tablename from pg_tables where tablename like 'h_config_register_check_{meter_no}%' order by tablename desc limit 1"
                print(sql)
                cur.execute(sql)
                fc = cur.fetchone()
                return fc
            except Exception as e:
                print("get error: %s" % e)
            finally:
                cur.close()
                con.close()
        elif self.source == 'Oracle':
            try:
                con = self.connect()
                cur = con.cursor()
                sql = f"select table_name from user_tables where table_name like 'H_CONFIG_REGISTER_CHECK_{meter_no}%' and ROWNUM=1 order by table_name desc"
                cur.execute(sql)
                fc = cur.fetchone()
                return fc
            except Exception as e:
                print("get error: %s" % e)
            finally:
                cur.close()
                con.close()
        else:
            print("数据库类型不支持")

    def meter_init(self, meter_no):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = "update c_ar_meter set dev_status=2 where meter_no='{}'".format(meter_no)
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def meter_init_except_1(self, meter_no):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = "update c_ar_meter set DEV_STATUS=1 where METER_NO='{}'".format(meter_no)
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

    def meter_init_except_2(self, meter_no):
        try:
            con = self.connect()
            cur = con.cursor()
            sql = "update c_ar_meter set DEV_STATUS=2, CONN_TYPE=13, COMMUNICATION_TYPE=7 where METER_NO='{}'".format(
                meter_no)
            cur.execute(sql)
            con.commit()
        except Exception as e:
            print("get error: %s" % e)
        finally:
            cur.close()
            con.close()

if __name__ == '__main__':
    client = nacos.NacosClient(server_addresses=readConfig()['nacos_url'], namespace='HES', username="nacos",
                               password="nacos")
    data_id = readConfig()['project']
    group = readConfig()['group']
    config = yaml.load(client.get_config(data_id, group), Loader=yaml.FullLoader)
    database = DB(source=config['DATABASE']['db_source'], host=config['DATABASE']['db_host'],
                  database=config['DATABASE']['db_database'], username=config['DATABASE']['db_user'],
                  passwd=config['DATABASE']['db_pwd'], port=config['DATABASE']['db_port'],
                  sid=config['DATABASE']['db_service'])
    table_name = database.meter_init(meter_no=config['Device']['device_number'])