from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
import cx_Oracle
import json
from django.db import models
from DataServer.models import User
# Create your views here.
def logindb(request):

    data =json.loads(request.body)
    #print(data['data1'])
    data_test= {"data1": " ",
                "data2": {"data": []
                         }
                }
    data_to_send={"status": "400", "msg": "No User", "data": "null" }
    print(data)
    conn2 = cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
    #
    cursor2 = conn2.cursor()
    #
    #cursor2.execute('select * from OLE_DB.CT_STANDARD_BEST')
    cursor2.execute('select * from OLE_DB.RPT_LINE_DAILY_L')
    result = cursor2.fetchmany(6)
    #
    print(cursor2.rowcount)
    #
    print(result)
    a=[1,2,3,4,5]
    data_test = {"data1": " ",
                 "data2": {"data": a
                          }
                 }
    data_to_send['data']=a

    for i in range(6):
        print(result[i])
    #
    cursor2.close()
    #
    conn2.close()

    return HttpResponse(json.dumps(data_to_send))
    #return HttpResponse(json.dumps(data_test))

def login(req):
    Method = req.method
    if Method == 'POST':
        data=json.loads(req.body)
        print(data)

        username = req.POST.get('username')
        username = data['username']

        print(username)

        password = req.POST.get('password')
        password = data['password']
        print(password)
        if username and password :
             username = username.strip()
             try:
                 user = User.objects.get(username=username)  # 判断用户名是否存在
             except:
                 res={"status": "400", "msg": "No User", "data": "null" }
                 #return HttpResponse(json.dumps(res), content_type="application/json")
                 return HttpResponse(json.dumps(res))
                 #return HttpResponse('用户名不存在')

             #if user.username == username:
             if user.password == password:
                 res = {"status": "200", "msg": "Success", "data": "null"}
                 return HttpResponse(json.dumps(res))
                 #return HttpResponse('登录成功')
             else:
                 res = {"status": "400", "msg": "Wrong Password", "data": "null"}
                 return HttpResponse(json.dumps(res))

   # return HttpResponse(' HELLO')