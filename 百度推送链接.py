import requests
import json
import sys



print('正在检测url.txt是否存在...')
try:
    f =open('url.txt')
    f.close()
    print('已检测到url.txt')
except FileNotFoundError:
    print ("未找到url.txt,请在当前目录创建")
    input('按enter退出')
    sys.exit()
except PermissionError:
    print ("没有权限读取url.txt,请检查权限设置")
    input('按enter退出')
    sys.exit()

url='http://data.zz.baidu.com/urls?'
headers={'Content-Type':'text/plain'}
u=str(input(r'请输入您的站点地址，不要带http(s)：'))
if 'https' in u:
    print('请不要带https')
    u = str(input(r'请输入您的站点地址，不要带http(s)：'))
elif 'http' in u:
    print('请不要带http')
    u = str(input(r'请输入您的站点地址，不要带http(s)：'))

print('正在检测是否存在准入密钥...')

try:
    f =open('pwd.txt')
    f.close()
    print('已检测到准入密钥，将继续接下来的操作')
    with open('pwd.txt', 'r',encoding='UTF-8') as k:
        key= k.read()
        k.close()
except FileNotFoundError:
    choose=input("未找到保存的准入密钥,是否填写并保存？(Y/n)")
    if choose == 'n':
        print("已选择不保存准入密钥")
        key = (input('请输入您的准入秘钥：'))
    else:
        print("已选择输入并保存准入密钥")
        key = (input('请输入您的准入秘钥：'))
        file_handle = open('pwd.txt', mode='w+')
        file_handle.write(key)

playload={'site':(u),'token':(key)}
with open("url.txt", "rb") as f:
    result=requests.post(url,data=f,params=playload,headers=headers)
jr=json.loads(result.text)
if 'error' in jr:
    er=jr['error']
    msg=jr['message']
    if 'token is not valid' in msg:
        msg='准入秘钥错误，请检查后重试'
    elif 'empty content' in msg:
        msg='需要提交的链接为空，请检查url.txt后重试'
    elif 'site init fail' in msg:
        msg='站点初始化失败，请检查站点地址是否正确'
    print('错误代码：',er,
          '\n返回信息:',msg)
    input('按enter退出')
else:
    rm=jr['remain']
    su=jr['success']

    print ('提交成功',su,'条链接\n'
           '剩余',rm,'条可提交')
    input('\n\n按enter退出')


