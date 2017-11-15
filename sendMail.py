import smtplib
import os 
import sys
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

if len(sys.argv) < 2:
  print "Usage -- python sendMail.py {mailerList} {attachment 1}  {attachment n}"
  sys.exit(1)

mailList = sys.argv[1]

if not os.path.exists(mailList):
  print "ERROR : Invalid path " + mailList + " !!!"
  sys.exit(1)

try:
  mailListObj = json.load(open(mailList))
  mailArray = mailListObj["email-addresses"]
  sender = mailListObj["email-sender"]
  message = mailListObj["email-message"]
  print ", ".join(mailArray)
except:
  print "ERROR !!!"
  e = sys.exc_info()[0]
  print e


FROM = sender["user-name"]
TO = ", ".join(mailArray)
msg = MIMEMultipart()
msg['From'] = sender["user-name"] 
msg['To'] = ", ".join(mailArray)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = message["sub"]
body = message["body"]
body = MIMEText(body)
msg.attach(body)
files = []

arguments = sys.argv
i = 2 
while  i < len(arguments):
  files.append(arguments[i])
  i+=1

print files

gmail_user = sender["user-name"]
gmail_pwd = sender["password"]

# Prepare actual message
try:
  try:
    for f in files:
      part = MIMEBase('application', "octet-stream")
      part.set_payload(open(f, "rb").read())
      Encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
      msg.attach(part)
  except:
    print "Attachment File Error"
    sys.exit(1)

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.ehlo()
  server.starttls()
  server.login(gmail_user, gmail_pwd)
  server.sendmail(FROM, TO, msg.as_string())
  server.close()
  print 'successfully sent the mail'
except:
  print "failed to send mail"
  e = sys.exc_info()[0]
  print e
  sys.exit(1)

