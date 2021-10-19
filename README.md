## 自动化框架依赖环境

### Python 解析器
+ python3.6 (32bit),  推荐安装`Miniconda3-4.3.31-Windows-x86.exe`

### 第三方扩展包  
+ pythonnet, 推荐安装`pythonnet-2.4.0-cp36-cp36m-win32`
+ PyYAML, 推荐安装`PyYAML-5.1.1-cp36-cp36m-win32`
+ lxml, 推荐安装`lxml-4.3.4-cp36-cp36m-win32`
+ openpyxl, 推荐安装`openpyxl-2.6.2`
+ pyserial, 推荐安装`pyserial-3.4-py2.py3-none-any`

### 在线安装方法
+ pip install `包名`
> 指定包名时无需带上后缀，例如`pythonnet`, `pyyaml`, `pyserial`

### 本地安装方法
+ 下载对应安装包(注意选择`python3.6 32bit`版本, 优先选择后缀为`whl`的文件)
+ pip install `文件名.whl`


### 执行方式
## 检查默认值
python  main.py -p tulip --client 1 --comPort 9 --tag default_value_check

## 检查权限
+ 先获取所有Get权限的OBIS返回结果保存在当前目录admin_result.xlsx(如果OBIS列表没有改动过则可以跳过此步骤)
python  main.py -p tulip --client 1 --comPort 9 --tag get_data

+ 执行以下命令检查权限
python  main.py -p tulip --client 1 --comPort 9 --tag access_rights_check

