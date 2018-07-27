from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
import cx_Oracle
import json
import requests
from django.db import models
from DataServer.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework import exceptions
import datetime
from DataServer.database_login import database_login

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url='http://10.10.31.113/WebService/BJYJY.asmx/Encrypt'  ## Password Webservice

conn = cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
cursor2 = conn.cursor()

Token_list=[
    '123456',
    'abcdef',

]
##Token 认证
class UserAuthview(BaseAuthentication):
    data_to_send = {"status": "200", "msg": "认证失败", "data": "null"}
    def authenticate(self, request):
        tk=request._request.GET.get("token")

        if tk in Token_list:
            return (tk,None)

        #return HttpResponse(json.dumps({"status": "200", "msg": "认证失败", "data": "null"}))
        raise exceptions.AuthenticationFailed({"status": "200", "msg": "Authenticate Failed", "data": "null"})
        #return HttpResponse(json.dumps(data_to_send))
    def authenticate_header(self, request):
        pass


class userquery(APIView):
    authentication_classes = [UserAuthview, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):

        return HttpResponse(loguserquery(request))

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

def loguserquery(req):
    data = json.loads(req.body)
    print(data)
    username_query = {"USER_ID": ""}
    username_query["USER_ID"] = data["username"]
    print(username_query)
    password_json = {"password": ""}
    password_json["password"] = data["password"]
    s = json.dumps(password_json)
    headers = {'Content-Type': 'application/json'}
    password_encrpyt = requests.post(url, headers=headers, data=s)
    password_encrpyt_temp = json.loads(password_encrpyt.text)
    print(password_encrpyt_temp)
    password_crpty = json.loads(password_encrpyt_temp["d"])
    print(password_crpty["password"])

    ## check the database if the user exits
    try:
        cursor2.execute(
            "select *  from OLE_DB.SYSU_USER where USER_ID = :USER_ID"
            , username_query
        )

    except cx_Oracle.DatabaseError as e:

        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))
    result = cursor2.fetchall()
    if cursor2.rowcount==0:
        res = {"status": "400", "msg": "No User", "data": "null"}
        # return HttpResponse(json.dumps(res), content_type="application/json")
        return HttpResponse(json.dumps(res))
    else:
        username=result[0][0]
        userpassword=result[0][2]

    if userpassword==password_crpty["password"]:
        res = {"status": "200", "msg": "Success", "data": "null"}
        return HttpResponse(json.dumps(res))
        # return HttpResponse('登录成功')
    else:
        res = {"status": "400", "msg": "Wrong Password", "data": "null"}
        return HttpResponse(json.dumps(res))









