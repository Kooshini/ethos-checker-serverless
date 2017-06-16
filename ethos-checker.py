#!/usr/bin/python
#################################
# ethos server checker on AWS Lambda (ethosdistro.com)
# Required Env Vars:
# ETHOS_ID
# SMTP_LOGIN
# SMTP_PASS
# SMTP_HOST
# SMTP_PORT
# SMTP_TO
# SMTP_FROM
#################################
import os, math, smtplib, socket, urllib.request, json
###### configure below ##########
#################################
ethosId = os.environ['ETHOS_ID'] ## e.g. ef1234
## email details
smtpLogin = os.environ['SMTP_LOGIN']
smtpPass = os.environ['SMTP_PASS']
smtpHost = os.environ['SMTP_HOST']
smtpPort = os.environ['SMTP_PORT']
mailRecipients = os.environ['SMTP_TO'] ## add more  ['email1@example.com', 'email2@example.com']
mailSender = os.environ['SMTP_FROM'] ## your@email.com
###### end configure ##########
###############################
def lambda_handler(event, context):
    target_url = "http://%s.ethosdistro.com/?json=yes" % (ethosId)
    print("Checking target distro URL %s" % (target_url))
    with urllib.request.urlopen(target_url) as url:
        data = json.loads(url.read().decode())
        alive_gpus = data['alive_gpus']
        total_gpus = data['total_gpus']
        total_hash = data['total_hash']
    ## fire off an email if the space is above the required number
    if alive_gpus < total_gpus:
        print("Error: The number of GPUs is %d/%d - total hash is %d" % (alive_gpus,total_gpus,total_hash))
        ## send email via the SMTP server
        server = smtplib.SMTP(smtpHost,smtpPort)
        server.starttls()
        server.login(smtpLogin, smtpPass)
        msg = "Subject: Urgent: The number of GPUs is %d/%d - total hash is %s" % (alive_gpus,total_gpus,total_hash)
        server.sendmail(mailSender, mailRecipients, msg)
        server.quit()
