from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST

from oauth2client.client import OAuth2WebServerFlow


def home(request):
    if request.user.is_authenticated():
        return render_to_response(template_name='home_logged_in.html')
    login_form = AuthenticationForm(request)
    return render_to_response(template_name='home_logged_out.html',
                              context={'login_form': login_form})


@require_POST
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    context_instance = RequestContext(request)

    if user is not None:
        login(request, user)
        return render_to_response(template_name='home_logged_in.html', context_instance=context_instance)
    else:
        # TODO: change to failure page, or add failure message
        return render_to_response(template_name='home_logged_out.html')


def logout_view(request):
    logout(request)
    return render_to_response(template_name='home_logged_out.html')


def google_auth(request):
    if request.POST:
        return google_callback(request)

    flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_CALENDAR_API_CLIENT_ID,
                               client_secret=settings.GOOGLE_CALENDAR_API_CLIENT_SECRET,
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri=settings.BASE_URL + '/auth/google')

    auth_uri = flow.step1_get_authorize_url()
    return HttpResponseRedirect(auth_uri)


def google_callback(request):
    flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_CALENDAR_API_CLIENT_ID,
                               client_secret=settings.GOOGLE_CALENDAR_API_CLIENT_SECRET,
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri=settings.BASE_URL + '/auth/google')
    flow.step2_exchange(request.data.get('code')).to_json()
    