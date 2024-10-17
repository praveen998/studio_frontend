from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings

@csrf_exempt 
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        print(username,password,email)
        #first_name = data.get('first_name', '')
        #last_name = data.get('last_name', '')

        if not username or not password or not email:
            return JsonResponse({"sucess": False,'error': 'Username, password, and email are required.'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"sucess": False,'error': 'Username already exists.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"sucess": False,'error': 'Email already exists.'}, status=400)

        user = User(
            username=username,
            email=email,
        )

        user.set_password(password)  
        user.save()
        return JsonResponse({"sucess": True,'message': 'User created successfully'}, status=201)
    
    return JsonResponse({"sucess": False,'error': 'Invalid request method'}, status=400)



@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print('username and password:',username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('user is valid')
            return JsonResponse({"sucess": True,'message': 'Login successful'},status=200)
        else:
            print('user is not valid')
            return JsonResponse({"sucess": False,'error': 'Invalid credentials'}, status=400)
        
    return JsonResponse({"sucess": False,'error': 'Invalid request method'}, status=400)


@csrf_exempt 
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Call Django's built-in logout function
        return JsonResponse({'message': 'Logged out successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)


def dashboard(request):
    if request.user.is_authenticated:
        print(f'user: {request.user.username}')
        return render(request,'dashboard.html')
    return JsonResponse({"sucess": False,'error': 'Login required'}, status=400)


def index(request):
    return render(request,'index.html')


def login_page(request):
    return render(request,'login_page.html')


def signup_page(request):
    return render(request,'signup_page.html')


@csrf_exempt
def upload_images(request):
    if request.method == 'POST':
        projectname = request.POST.get('projectname', '')
        uploaded_files =  request.FILES.getlist('files') 
        saved_files_info = []
        print('project names:',projectname)
        print('file length',uploaded_files)
        if uploaded_files:
            project_path = os.path.join(settings.MEDIA_ROOT, projectname)
            os.makedirs(project_path, exist_ok=True)
            print('project path:',project_path)
            saved_files_info = []
            for uploaded_file in uploaded_files:
                with open(f'media/{projectname}/{uploaded_file.name}', 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                saved_files_info.append(uploaded_file.name)
            return JsonResponse({'status': 'success',}, status=200)
        return JsonResponse({'status': 'error', 'message': 'No files uploaded'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


'''
        for image in uploaded_files:
            project_path = os.path.join(settings.MEDIA_ROOT, projectname)
            os.makedirs(project_path, exist_ok=True)
            file_name = image.name
            file_size = image.size
           
            print(f'Received image: {image.name}')
            # Optionally, save the file locally
   
        return JsonResponse({'status': 'success',}, status=200)

    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
    '''