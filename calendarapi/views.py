from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import pickle
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import render , redirect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib.auth.models import User
def get_credentials_file_path(user_id):
    return os.path.join("{}/{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id , "credentials.pkl"))


def check_user_credential_file_path(user_id) :
    scopes = ["https://www.googleapis.com/auth/calendar"]
    credentials = None
    create_flag = True
    file_path = os.path.join("{}/{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id , "credentials.pkl"))
    if os.path.exists(file_path) : 
        credentials = pickle.load(open(file_path , "rb"))
        if credentials and credentials.expired and credentials.refresh_token :
            credentials.refresh(Request())
            create_flag = False
        if credentials.valid or not credentials.expired:
            create_flag = False
    else : 
        return True
    return create_flag

def create_user_credential_file_path(user_id) : 
    file_path = os.path.join("{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id ))
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    

def user_credential_token_file_path(user_id) : 
    file_path = "{}/credentials/{}/credentials.pkl".format(settings.BASE_DIR , user_id)
    return file_path

def CreateCredentialsForUserDataAccess(*args , **kwargs) : 
    scopes = ["https://www.googleapis.com/auth/calendar"]
    client_secret_file = os.path.join(settings.BASE_DIR , "static" , "client_secret.json")
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file , scopes = scopes)
    credentials = flow.run_local_server()
    return credentials




def GoogleCalendarinitView(request , *args ,**kwargs) : 
    context = {}
    if request.method == "POST" :
        user = request.user
        user_id = user.id
        if check_user_credential_file_path(user_id):
            create_user_credential_file_path(user_id)
            pickle.dump(CreateCredentialsForUserDataAccess() ,
                    open("{}".format(user_credential_token_file_path(user_id)) , "wb")
                    )
            print("Finally dumped !")
        return redirect("get-calender-access" , user_id = user_id)
    return render(request , "authentication/allow_calender_access.html" , context)


def GoogleCalendarRedirectView(request  , user_id , *args ,**kwargs) :
    credentials = pickle.load(open(get_credentials_file_path(user_id) , "rb"))
    service = build("calendar" , "v3" , credentials = credentials)
    calendars = service.calendarList().list().execute()
    calendarId = calendars["items"][0]["id"]
    events = service.events().list(calendarId = calendarId).execute()
    events = events["items"]
    context = {
        "events" : events ,
    }
    return render(request , "authentication/get_calender_access.html" , context)


@api_view(["GET"])
def calendarInit(request , *args , **kwargs):
    user_id = 1
    context = {}
    return_data = [user_id , "success"]
    if request.method == "GET" :
        user = User.objects.get(id = 1)
        user_id = user.id
        if check_user_credential_file_path(user_id):
            create_user_credential_file_path(user_id)
            pickle.dump(CreateCredentialsForUserDataAccess() ,
                    open("{}".format(user_credential_token_file_path(user_id)) , "wb")
                    )
            print("Finally dumped !")
            return_data = [user_id , "success"]
            return Response(return_data)
        else : 
            return_data = [user_id , "success"]
            return Response(return_data)
    return Response([user_id , "error"])
    
@api_view(["GET"])
def calendarRedirect(request , *args , **kwargs) :
    user_id = 1
    credentials = pickle.load(open(get_credentials_file_path(user_id) , "rb"))
    service = build("calendar" , "v3" , credentials = credentials)
    calendars = service.calendarList().list().execute()
    calendarId = calendars["items"][0]["id"]
    events = service.events().list(calendarId = calendarId).execute()
    events = events["items"]
    return_events = [ ]
    for event in events :
        try : 
            return_events.append(event["summary"])
        except : 
            ...
    return Response(return_events)