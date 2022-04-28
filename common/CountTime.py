# import paramiko
import datetime
import os


def count_time(func):
    def took_up_time(*args, **kwargs):
        start_time = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        took_up_time = (end_time - start_time).total_seconds()
        print(f"{func.__name__} execution took up time:{took_up_time}")
        return ret
    return took_up_time


# hostname = "10.32.233.164"
# port = 22
# username = "root"
# password = "kaifa123"
# REMOTE_PATH = "/opt/tomcat/webapps"
# LOCAL_PATH = "report/empower/2"
#
#
# def upload(_localDir, _remoteDir):
#     _localDir = LOCAL_PATH
#     _remoteDir = LOCAL_PATH
#     try:
#         t = paramiko.Transport((hostname, port))
#         t.connect(username=username, password=password)
#         sftp = paramiko.SFTPClient.from_transport(t)
#         print('upload file start %s ' % datetime.datetime.now())
#         for root, dirs, files in os.walk(_localDir):
#             # 相对与_localDir的路径
#             remoteRoot = root.replace("\\", "/")
#             # 文件名，不包括路径
#             for filespath in files:
#                 local_file = os.path.join(root, filespath)
#                 remote_file = REMOTE_PATH + "/" +remoteRoot + "/" + filespath
#                 remote_file = remote_file.replace("//", "/")
#                 # print("remote_file : %s" % remote_file)
#                 try:
#                     sftp.put(local_file, remote_file)
#                 except Exception:
#                     sftp.mkdir(os.path.split(remote_file)[0])
#                     sftp.put(local_file, remote_file)
#                 print("upload %s to remote %s" % (local_file, remote_file))
#             for name in dirs:
#                 remoteDir = _remoteDir +"/"+ remoteRoot +"/" + name
#                 remoteDir = remoteDir.replace("//", "/")
#                 print("remoteDir ", remoteDir)
#                 try:
#                     sftp.mkdir(remoteDir)
#                     print("mkdir path %s" % remoteDir)
#                 except Exception:
#                     pass
#         print('upload file success %s ' % datetime.datetime.now())
#         t.close()
#     except Exception as e:
#         print(e)
#
# t = paramiko.Transport(('10.32.233.164', 22))
#
# t.connect(username="root", password="kaifa123")
#
# sftp = paramiko.SFTPClient.from_transport(t)
#
# # 远程目录
# remotepath = '/opt/'
#
# # 本地文件
# localpath = 'README.md'
#
# # 上传文件
# sftp.put(localpath, remotepath)
#
# # 下载文件
# # sftp.get(remotepath, localpath)
#
# # 关闭连接
# t.close()


# upload(LOCAL_PATH, REMOTE_PATH)

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname, 22, username, password)
# stdin, stdout, stderr = ssh.exec_command("du -ah " + REMOTE_PATH)
# print(stdout.readlines())
# ssh.close()