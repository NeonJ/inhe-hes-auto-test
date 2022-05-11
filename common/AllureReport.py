"""
 File       : main.py
 Time       : 2022/2/11 15:37
 Author     : 曹剑南
 version    : python 3.7
"""
import shutil
import json
import os

from common.YamlConfig import readConfig



def get_dirname():
    history_file = os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}/report/{readConfig()['project']}", "history.json")
    print(history_file)
    if os.path.exists(history_file):
        with open(history_file) as f:
            li = eval(f.read())
        li.sort(key=lambda x: x['buildOrder'], reverse=True)
        return li[0]["buildOrder"] + 1, li
    else:
        with open(history_file, "w") as f:
            pass
        return 1, None


def update_trend_data(dirname, old_data: list):
    WIDGETS_DIR = os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}/report/{readConfig()['project']}", f"{str(dirname)}/widgets")
    with open(os.path.join(WIDGETS_DIR, "history-trend.json")) as f:
        data = f.read()

    new_data = eval(data)
    if old_data is not None:
        new_data[0]["buildOrder"] = old_data[0]["buildOrder"] + 1
    else:
        old_data = []
        new_data[0]["buildOrder"] = 1
    new_data[0]["reportUrl"] = f"{dirname}/index.html"
    new_data[0]["duration"] = f""
    old_data.insert(0, new_data[0])
    for i in range(1, dirname + 1):
        with open(os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}/report/{readConfig()['project']}", f"{str(i)}/widgets/history-trend.json"), "w+") as f:
            f.write(json.dumps(old_data))
    history_file = os.path.join(f"{os.path.dirname(os.path.dirname(__file__))}/report/{readConfig()['project']}", "history.json")

    with open(history_file, "w+") as f:
        f.write(json.dumps(old_data))
    return old_data, new_data[0]["reportUrl"]


def environment():
    shutil.copyfile(f"{os.path.dirname(os.path.dirname(__file__))}/categories.json", f"{os.path.dirname(os.path.dirname(__file__))}/result/categories.json")
    file = open(f"{os.path.dirname(os.path.dirname(__file__))}/result/environment.properties", "w")
    # env = open("{}/nacos-data/snapshot/{}+{}+HES".format(os.path.dirname(os.path.dirname(__file__)),readConfig()['project'],readConfig()['group']),encoding="utf-8")
    env = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config/settings.yaml'),encoding='utf-8')
    # file.write(setting[Project.name].__str__().replace("{", '').replace("}", '').replace("': '","'='").replace(",","\n").replace("'",''))
    file.write(env.read().__str__())

if __name__ == '__main__':
    environment()