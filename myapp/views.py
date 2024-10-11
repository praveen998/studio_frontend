from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Authentication

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'createaccount.html')

@csrf_exempt
def login_auth(request):
    try:
       data = json.loads(request.body) 
       useremail=data.get('useremail')
       username=data.get('username')
       password=data.get('password')
       print(useremail,username,password)

       auth=Authentication(
           username=username,
           password=password,
           email=useremail
       )
       auth.save()
       return JsonResponse({"sucess": True}, status=200)
    except Exception :
        return JsonResponse({"sucess": False}, status=401)

def authentication(request):
    try:
        data=json.load(request.body)
        username=data.get('username')
        password=data.get('password')
        print('user username and password',username,password)
        user = Authentication.objects.get(username=username)
        if user.password == password:
                print('password is correct')
                return JsonResponse({"sucess": True}, status=200)
        else:
                print('password is incorrect')
                return JsonResponse({"sucess": False}, status=401)
    except Exception :
        print('exception')
        return JsonResponse({"sucess": False}, status=401)