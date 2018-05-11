from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from Mychain.forms import *
import json,urllib


def index(request):
    return HttpResponse("hello!! this is demo")

def test(request,id):
    text = 'diplay id : ',id
    return HttpResponse(text)

def testid(request):
    testid = datetime.now().date()
    none = 'none'
    return render(request,'index.html',{'id':testid,'none':none})


def login(request):
    username = 'not logged in'
    
    if request.method == "POST":
        myloginform = LoginForm(request.POST)

        if myloginform.is_valid():
            username = myloginform.cleaned_data['username']

    else:
        myloginform = LoginForm()

    return render(request, 'loggedin.html', {'username':username})


'''def data(request):
    if request.method == "POST":
        json_data = JsonData(request.POST)
       
        if json_data.is_valid():
           sender = json_data.cleaned_data['sender']
           receiver = json_data.cleaned_data['receiver']
           amount = json_data.cleaned_data['amount']
        
    return render(request, 'transaction.html' , {'response':json_data})
'''
def mynode(request):
    return render(request, 'bc.html')