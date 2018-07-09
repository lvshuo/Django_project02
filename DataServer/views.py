from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
import cx_Oracle
import json
from django.db import models
from DataServer.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework import exceptions
import datetime
# Create your views here.
class dbreadrest(APIView):
   # authentication_classes = [TestAuthentication, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        data_to_send = {"status": "400", "msg": "No User", "data": "null"}
        a = [1, 2, 3, 4, 5]
        data_to_send['data'] = a
        return HttpResponse(json.dumps(data_to_send))
        #return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

class dbreadrest01(APIView):
   # authentication_classes = [TestAuthentication, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        data_to_send = {"status": "400", "msg": "No User", "data": "null"}
        a = [1, 2, 3, 4, 8]
        data_to_send['data'] = a
        #return HttpResponse(json.dumps(data_to_send))
        return Response(data_to_send)
        #return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')
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
    cursor2.execute('select * from OLE_DB.CT_STANDARD_BEST')
    result=cursor2.fetchone()
    data1=result[3]
    date_test=datetime.datetime.now()
    print(date_test)
    print(date_test.month)
    print(data1)
    #cursor2.execute('select * from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE =')
    cursor2.execute("select * from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE =TO_DATE('2018-07-06', 'YYYY-MM-DD')")
    #cursor2.execute("select * from OLE_DB.RPT_LINE_DAILY_L where  date_format(WORK_DATE ,'%Y-%m-%d') ='2018-07-06'")
    result = cursor2.fetchall()
    #result = cursor2.fetchmany(10)
    #
   # print(result.rowcount)
    #
    print(result)
    a=[1,2,3,4,5]
    data_test = {"data1": " ",
                 "data2": {"data": a
                          }
                 }
    data_to_send['data']=a

    for i in range(cursor2.rowcount):
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

