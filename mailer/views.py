from django.shortcuts import render
from .forms import emailForm, emailModelForm
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import emailModel
import sched, time
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import datetime

import smtplib,ssl


# Create your views here.

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "<gmail address>"
SENDER_EMAIL_PASSWORD = "<password>"

#FOR REPORT
ADMIN_EMAIL = "<admin email>"

def home(request):
    try:
        # form = emailForm(request.POST or None,request.FILES or None)
        form = emailModelForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            obj = form.save(commit=False)
            with ThreadPoolExecutor() as executor:
                executor.submit(send_email(data['email'], data['subject'], data['cc'], data['bcc'], data['message']))
            # form.save()
            obj.save()
            form = emailModelForm()
        context = {"title": "Welcome to Email Service", "user": request.user, "form":form}
        return render(request, 'index.html', context)
    except Exception as e:
        print(e)
        return render(request, 'index.html', {"user": "Something went Wrong"})

def send_email(recipient_email,subject,cc,bcc,message):
    try:

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "soem_dummy_account"
        msg['To'] = recipient_email
        msg['cc'] = cc
        msg['bcc']=bcc

        # part2 = MIMEText(html, 'html')
        part3 = MIMEText(message, 'plain')
        msg.attach(part3)
        # msg.attach(part1)

        context = ssl.create_default_context()
        print("Trying to connect to SMTP server")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Can be omitted
            print("Hello Completed! Ready to connect")
            server.starttls(context=context)
            print("TLS security accepted")
            server.ehlo()  # Can be omitted
            print("Trying to login with the sender's email account")
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            print("Mail sent !")
            del msg
    except smtplib.SMTPException as error:
        print(error)
    except smtplib.SMTPServerDisconnected as error:
        print(error)
    except smtplib.SMTPResponseException as error:
        print(error)
    except smtplib.SMTPSenderRefused as error:
        print(error)
    except smtplib.SMTPRecipientsRefused as error:
        print(error)
    except smtplib.SMTPDataError as error:
        print(error)
    except smtplib.SMTPConnectError as error:
        print(error)
    except smtplib.SMTPHeloError as error:
        print(error)
    except smtplib.SMTPNotSupportedError as error:
        print(error)
    except smtplib.SMTPAuthenticationErrorr as error:
        print(error)
    except Exception as error:
        print(error)

@periodic_task(run_every=(crontab(minute='*/30')), name="email_report", ignore_result=True)
def send_report():
    try:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        total_emails = emailModel.objects.filter(timestamp__gt=yesterday)

        count_emails = len(total_emails)
        email_json = [] #it is actually a list
        for email in total_emails:
            email_json.append(str(email.timestamp))
        message = "Total {} emails were sent with the following timestamps {}".format(count_emails,email_json)
        print(message)
        send_email(ADMIN_EMAIL,"Email Report",ADMIN_EMAIL,ADMIN_EMAIL,str(message))
        print("Sent Report to ",ADMIN_EMAIL)
            # didnt know what to do with cc , bcc. Leaving it as admin email for now.
    except Exception as err:
        print("Some Error occured")
        print(err)
