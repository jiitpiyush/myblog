from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
 
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
import ipdb

@csrf_exempt
def login(request):
	# ipdb.set_trace()
	#Post request handling
	if request.method == 'POST':
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")

		#validating user
		user = authenticate(username = username , password = password)

		#if id/pw combination is wrong
		if user == None:
			status = 'wrong id/pw combination'

			#sending back Json Response
			return JsonResponse({'status':'ok','result':{'response':status}})
		else:
			status = 'logged in successfully'
			#generating token for user
			token = Token.objects.get_or_create(user=user)
			userdata = UserData.objects.get(author=user.username)

			request.session['user'] = token[0]
			return HttpResponseRedirect("/")
			# # return JsonResponse({'status':'ok','cookie':s['user'],'result':{'response':status,'token':str(token[0])} , 'usertype' : str(userdata.user_type)})

	#other request handling except POST
	else:
		return render(request, 'login/signin.html',)


@csrf_exempt
def signup(request):

	#handling post request
	if request.method == 'POST':

		#creating user
		user = User.objects.create_user(request.POST.get("username",""), request.POST.get("email",""), request.POST.get("password",""))
		user.save()

		userdata = UserData(author = request.POST.get("username","") , user_type = request.POST.get("user_type",""));
		userdata.save()

		return JsonResponse({'status':'ok','result':{'response':'successfully created'}})

	#handling other requests
	else:
		#sending back Json Response
		return render(request, 'login/signup.html',)

def logout(request):
    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
        return HttpResponseRedirect('/')