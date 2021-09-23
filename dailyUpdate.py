import os, shutil, re, subprocess

from typing import Pattern

def patternNum(pat, str):
    # '(?<=cert)\d+'
    sourceStr = "(?<=" + pat + ")\d+"
    # print("sourceStr" + sourceStr)
    pattern = re.compile(sourceStr)
    # print(pattern)
    nums = pattern.findall(str)
    if len(nums):
        return int(nums[0])
    else:
        return -1

def createFileIfNeeded(filePath):
    if os.path.exists(filePath):
        return

def Touch(file_name):
       if file_name in os.listdir('.'):
              print("file exist!")
       else:
              print("creating %s" %file_name)
              fid = open(file_name,'w')
              fid.close()  

"""
 匹配“cert=”后面的数字
pattern = re.compile(r'(?<=cert)\d+\.?\d*')
pattern.findall(string)
['0.9863265752792358']
"""

# clone 证书 放到 
cert_git_dir = "/var/certDir/bingxiaolee/"
if os.path.exists(cert_git_dir):
    # pull
    os.chdir(cert_git_dir)
    subprocess.call(["git", "pull", "origin", "HEAD"])
 else:
    # clone
    os.mkdir("/var/certDir/")
    os.chdir("/var/certDir/")
    subprocess.call(["git", "clone", "git@gitlab.com:konglee873/bingxiaolee.git"])

des_Dir = cert_git_dir + "bingxiaolee.com"
max_numCert = -1
max_numCert_Path = ""
max_privkey = -1
max_privkey_Path = ""
for parent, dirnames, filenames in os.walk(des_Dir):
    for filename in filenames:
        file_path = os.path.join(des_Dir, filename)
        # print(file_path)
        numCert = patternNum("cert", file_path)
        # print("numCert")
        # print(numCert)
        if max_numCert == -1:
            max_numCert = numCert
            max_numCert_Path = file_path
        else:
            if numCert > max_numCert:
                max_numCert = numCert
                max_numCert_Path = file_path
        # cert
        # privkey
        numPri = patternNum("privkey", file_path)
        # print("privkey")
        # print(numPri)
        if max_privkey == -1:
            max_privkey = numPri
            max_privkey_Path = file_path
        else:
            if numPri > max_privkey:
                max_privkey = numPri
                max_privkey_Path = file_path

print(max_numCert_Path)
print(max_privkey_Path)

# 创建文件 /etc/HTTPSCertDir/cert.pem
# 创建文件 /etc/HTTPSCertDir/privkey.pem

cert_des_path = "/var/HTTPSCertDir/cert.pem"
privkey_des_path = "/var/HTTPSCertDir/privkey.pem"

certDir = "/var/HTTPSCertDir/"
if not os.path.exists(certDir):
    os.mkdir(certDir)

os.chdir(certDir)


# Touch("cert.pem")
# Touch("privkey.pem")
os.remove(cert_des_path)
os.remove(privkey_des_path)
os.symlink(max_numCert_Path, cert_des_path)
os.symlink(max_privkey_Path, privkey_des_path)