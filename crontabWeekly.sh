#!/bin/bash

script_path = "/var/autoScript/"
# 这里的-x 参数判断$script_path是否存在并且是否具有可执行权限
if [ ! -x "$script_path"]; then
mkdir "$script_path"
fi

rm -rf "{$script_path}*"
cd $script_path
wget https://raw.githubusercontent.com/kikiloveswift/Trojan/master/dailyUpdate.py
python3 dailyUpdate.py