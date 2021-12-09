"""
# File       : configs.py
# Time       : 2021/10/19 9:03
# Author     : 黄大彬
# version    : python 3.7
"""

class Project:
    name='ivy'          #与下面setting项目key对应
    tag='hesTest'              #对应comms.marker
    path='/'            #对testCase目录接口对应


#所有项目配置
setting={
    "ivy":{
        "db_host":"10.32.233.164",
        "db_user":"ami",
        "db_port":1621,
        "db_pwd":'ami',
        "db_service":'ami',
        "meter":312121,
        "HESAPI":'http://10.32.233.31:30073'

    },
    "saturn03":{
        "db_host":"10.32.233.164",
        "db_user":"ami",
        "db_port":1621,
        "db_pwd":'ami',
        "db_service":'ami',
        "meter":312121
    }
}


