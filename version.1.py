from django.shortcuts import render , redirect
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from django.conf import settings
import pickle

def get_credentials_file_path(user_id):
    return os.path.join("{}/{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id , "credentials.pkl"))

def create_or_check_user_credential_file_path(user_id) : 
    if not os.path.exists(os.path.join("{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id))):
        os.mkdir(os.path.join("{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id)))
    
    if os.path.exists(os.path.join("{}/{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id , "credentials.pkl"))):
        os.remove(os.path.join("{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id)))
        os.mkdir(os.path.join("{}/{}/{}".format(settings.BASE_DIR , "credentials" , user_id)))

def user_credential_token_file_path(user_id) : 
    file_path = "{}/credentials/{}/credentials.pkl".format(settings.BASE_DIR , user_id)
    return file_path

def CreateCredentialsForUserDataAccess(*args , **kwargs) : 
    scopes = ["https://www.googleapis.com/auth/calendar"]
    client_secret_file = os.path.join(settings.BASE_DIR , "static" , "client_secret.json")
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file , scopes = scopes)
    credentials = flow.run_local_server()
    return credentials


def AllowAccess(request , *args ,**kwargs) : 
    context = {}
    if request.method == "POST" :
        user = request.user
        user_id = user.id
        create_or_check_user_credential_file_path(user_id)
        pickle.dump(CreateCredentialsForUserDataAccess() ,
                    open("{}".format(user_credential_token_file_path(user_id)) , "wb")
                    )
        print("Finally dumped !")
        return redirect("get-calender-access" , user_id = user_id)
    return render(request , "authentication/allow_calender_access.html" , context)


def GetAccess(request  , user_id , *args ,**kwargs) :
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
