from __future__ import print_function
import pickle
from datetime import datetime
import pandas as pd, csv, sqlite3
from rest_framework.generics import  ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from django.views.generic import ListView
from django.shortcuts import render,redirect
from .serializers import EmailsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
import os.path
import base64
import email
import email
import imaplib
from apiclient import errors
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.shortcuts import render,redirect
from .models import Emails,AutoReplyIds

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']



def gmail_authenticate(request):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    response = service.users().messages().list(userId='me',labelIds=['INBOX']
                                               ).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='me', labelIds=['INBOX'],
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
    From    = []
    Date    = []
    subject = []
    Text    = []
    msg_i   = []
    # Check cache and sync mails
    sync_ids = Emails.objects.values_list('Msg_id')
    cache = {}
    
    for a in sync_ids:
        cache[a[0]]=1
    gmail_msg_ids = {}  
    for msg_id in messages:
        gmail_msg_ids[msg_id['id']]=1
    for msg_id in messages:
        try :
            # print(msg_id)
            if msg_id['id'] not in cache:
                messg = service.users().messages().get(userId='me', id=msg_id['id'],format='metadata').execute()
                headers = messg['payload']['headers']
                From    += [i['value'] for i in headers if i["name"]=="From"]
                Date    += [i['value'] for i in headers if i["name"]=="Date"]
                subject += [i['value'] for i in headers if i["name"]=="Subject"]
                Text    += [messg['snippet']]
                msg_i   += [msg_id['id']]
        except errors.HttpError:
                print ('An error occurred:')    

    #Delete mails when Email present in DB but not in Gmail Account       
    for ids in cache.keys():
        if ids not in gmail_msg_ids:
                q = Emails.objects.filter(Msg_id=ids)
                q.delete()
    #Connect to DB and load data to log mails synced 
    conn = sqlite3.connect('db.sqlite3')
    my_dict= {'Msg_id':msg_i,'Date':Date,'From':From,'Subject':subject,'Message':Text}
    df = pd.DataFrame(my_dict,columns = ['Msg_id','Date','From','Subject','Message'])
    df.to_sql('gmailapi_emails', conn, if_exists='append', index=False)
    conn.close()
    return redirect('/api/v1/Emails')                 
                

#GET API TO FETCH PAGINATED EMAILS
class ListPaginatedEmailsView(ListView):
    model = Emails
    template_name = 'Emails/index.html'  
    context_object_name = 'object_list'  # Default: object_list
    paginate_by = 10
    queryset = Emails.objects.all()  
    
#Auto Reply Button Functionality


def AutoReply(request):
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    response = service.users().messages().list(userId='me', q='from : sanbreak100@gmail.com "Please help me"').execute()
    # print(response)

    msg_ids = []
    Label  = []
    Date   = []
    From   = []
    To     = [] 
    Subject = []
    Message = []
    reply_ids  = AutoReplyIds.objects.values_list('Msg_id')
    cache = {}
    #Cache Implmentation to not allow sending replies to same person again
    for a in reply_ids:
        cache[a[0]]=1
    for msg in response['messages'] :
        print(msg['id'])
        if msg['id'] not in cache: 
            messg   = service.users().messages().get(userId='me', id=msg['id'],format='metadata').execute()
            headers = messg['payload']['headers']
            t = [i['value'] for i in headers if i["name"]=="From"]
            to   = t[0]
            F = [i['value'] for i in headers if i["name"]=="To"]
            From_ = F[0]
            subject = 'Hi'
            message_text = 'Hello There, We will get back to you on this'
            message = MIMEText(message_text)
            # print (message)
            message['to'] = to
            message['from'] = From_
            message['subject'] = subject
            # print(message)
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            body = {'raw': raw}
            # to_send_msg = {'raw': base64.urlsafe_b64encode(message.as_string())}
            # print(to_send_msg)
            try:    
                    # print(1)
                    message = (service.users().messages().send(userId='me', body=body)
                       .execute())
                    now         = datetime.now()
                    date_str    = now.strftime("%d/%m/%Y %H:%M:%S")
                    # print ('Message Id: %s' % message['id'])
                    # print(message)
            except errors.HttpError:
                    print ('An error occurred:')
            msg_ids     += [msg['id']]
            To          += [to]
            From        += [From_]
            Subject     += [subject]
            Message     += [message_text]
            Label       += ['SENT']
            Date        += [date_str]       
    #Connect and load data to log auto reply ids
    conn = sqlite3.connect('db.sqlite3')
    my_dict= {'Msg_id':msg_ids,'Label':Label,'Date':Date,'From':From,'To':To,'Subject':Subject,'Message':Message}
    df = pd.DataFrame(my_dict,columns = ['Msg_id','Label','Date','From','To','Subject','Message'])
    df.to_sql('gmailapi_autoreplyids', conn, if_exists='append', index=False)   
    conn.close()
    return redirect('/api/v1/Emails/')

       
#Authenticate with google





    
