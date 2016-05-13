from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse


def get_user(request):
	if 'user' in request.session:
		token = str(request.session['user'])
		token_object = Token.objects.get(key=token)
		user = token_object.user
		return user
	else:
		return 