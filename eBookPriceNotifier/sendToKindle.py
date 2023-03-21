import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os import scandir, path, makedirs, replace

kindleFolder = "/Users/Andres/Documents/Kindle/"
ebookTypes = ('.epub', '.mobi', '.pdf')
pdfType = '.pdf'


def getSubtype(fileExt):
    return path.splitext(fileExt)[1][1:]


def scanAndSort(msg):
    directory = path.join(kindleFolder, "SentEbooks")
    makedirs(directory, exist_ok=True)
    for file in scandir(kindleFolder):
        if file.is_file():
            fileExt = path.splitext(file.name)[1].lower()
            if fileExt in ebookTypes:
                with open(file.path, "rb") as b:
                    ebook_data = b.read()
                ebook = MIMEApplication(ebook_data, Name=file.name, _subtype=getSubtype(fileExt))
                ebook.add_header('Content-Disposition', 'attachment', filename=ebook.get_filename())
                msg.attach(ebook)
                newPath = path.join(directory, file.name)
                replace(file.path, newPath)



def sendToKindle(kindleEmail, email, passwd):
    msg = MIMEMultipart()
    msg['Subject']="eBook(s) Sent"
    msg['To']=kindleEmail
    msg['From']=email

    scanAndSort(msg)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email, passwd)
        smtp.sendmail(email, kindleEmail, msg.as_string())
        smtp.quit()



def main():
    info = json.load(open('info.json'))
    kindleEmail=info.get("kindle_email")
    email=info.get("my_email")
    passwd=info.get("sender_pswd")
    sendToKindle(kindleEmail, email, passwd)


if __name__ == '__main__':
    main()
    
