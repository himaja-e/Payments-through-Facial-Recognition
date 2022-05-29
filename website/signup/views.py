from django.shortcuts import render
import MySQLdb as sql
fn=''
em=''
pwd=''
# Create your views here.
def signaction(request):
    global fn,em,pwd
    if request.method=="POST":
        m=sql.connect(host="localhost",user="root",passwd="himaja",database='website')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="user_name":
                fn=value
            if key=="email":
                em=value
            if key=="password":
                pwd=value
        
        c1="select * from users where user_name='{}'".format(fn)
        cursor.execute(c1)
        t1=cursor.fetchall()
        c2="select * from users where email='{}'".format(em)
        cursor.execute(c2)
        t2=cursor.fetchall()
        if(t1!=() and t2!=()):
            if(t1[0][0]==fn and t2[0][1]==em):
                return render(request,'exists.html')
        if(t1!=() and t1[0][0]==fn):
            return render(request,'usernameexists.html')
        if(t2!=() and t2[0][1]==em):
            return render(request,'emailexists.html')
        
        c="insert into users values('{}','{}','{}')".format(fn,em,pwd)
        cursor.execute(c)
        m.commit()

    return render(request,'signup_page.html')
def values():
    print(emlist)