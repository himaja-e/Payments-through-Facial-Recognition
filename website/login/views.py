from django.shortcuts import render
import MySQLdb as sql
from django.http import HttpResponseRedirect
em=''
pwd=''

# Create your views here.
def loginaction(request):
    global em,pwd
    t=()
    if request.method=="POST":
        d=request.POST
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        if(em=="abcd@gmail.com" and pwd=="12345"):
            return HttpResponseRedirect('/image/')
            
        else:
            m=sql.connect(host="localhost",user="root",passwd="himaja",database='website')
            cursor=m.cursor()
            c="select * from users where email='{}' and password='{}'".format(em,pwd)
            cursor.execute(c)
            t=tuple(cursor.fetchall())
        
        if t==() :
            return render(request,'error.html')
        else:
            return HttpResponseRedirect('/image/')

    return render(request,'index.html')
def __username__(self):
    return self.em