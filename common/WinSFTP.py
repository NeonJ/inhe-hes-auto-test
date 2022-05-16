# _*_ coding: utf-8 _*_
# @Time      : 2022/5/5 10:27
# @Author    : Jiannan Cao
# @FileName  : WinSFTP.py.py
from stat import S_ISDIR

import paramiko as paramiko
import os

class Linux(object):
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        self.t = ''
        self.chan = ''
        self.try_times = 3

    def connect(self):
        pass

    def close(self):
        pass

    def send(self, cmd):
        pass

    def sftp_get(self, remotefile, localfile):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
        t.close()

    def sftp_put(self, localfile, remotefile):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
        t.close()

    def __get_all_files_in_remote_dir(self, sftp, remote_dir):
        # 保存所有文件的列表
        all_files = list()

        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if S_ISDIR(x.st_mode):
                all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    def __get_all_files_in_local_dir(self, local_dir):
        # 保存所有文件的列表
        all_files = list()

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = os.listdir(local_dir)
        for x in files:
            # local_dir目录中每一个文件或目录的完整路径
            fullpath = os.path.join(local_dir, x)
            # 如果是目录，则递归处理该目录
            if os.path.isdir(fullpath):
                all_files.append(fullpath)
                all_files.extend(self.__get_all_files_in_local_dir(fullpath))
            else:
                all_files.append(fullpath)
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        t = paramiko.Transport(sock=(self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # 去掉路径字符穿最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_local_dir(local_dir)

        root = local_dir.replace(os.path.split(local_dir)[:-1][0], remote_dir)
        root = root.replace("\\", "/")
        if os.path.isdir(local_dir):
            try:
                sftp.mkdir(root)
                print(u'Create root dir...')
            except IOError:
                print(u'Error: Root directory already exists, please check if there is a conflict')
        local_dir = os.path.split(local_dir)[:-1][0]
        # 依次put每一个文件
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_filename = x.replace(local_dir, remote_dir)
            # print(remote_filename)
            remote_filename = remote_filename.replace("\\", "/")
            # print(x)
            # print(remote_filename)
            if os.path.isdir(x):
                sftp.mkdir(remote_filename)
                # print(u'Put文件夹%s创建中...' % filename)
                continue
            else:
                # print(u'Put文件%s传输中...' % filename)
                sftp.put(x, remote_filename)


if __name__ == '__main__':
    remoteFile = r'/opt/test'
    localFile = r'F:\Training\Bukhara Training Record & Examine Result'
    host = Linux('10.32.233.164', 'root', 'kaifa123')

    host.sftp_put_dir(localFile,remoteFile)
