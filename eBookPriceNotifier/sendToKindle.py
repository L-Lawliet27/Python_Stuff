import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os import scandir, path, makedirs, replace, chdir
from sys import argv


kindleFolder = "/Users/Andres/Documents/Kindle/"
downloadsFolder = "Downloads/"
downloadsPath = "/Users/Andres/Downloads/"
ebookTypes = ('.epub', '.mobi', '.pdf')


def getSubtype(fileExt):
    return path.splitext(fileExt)[1][1:]


def attachEbook(fileName, filePath, fileExt, dir, msg):
    with open(filePath, "rb") as b:
        ebook_data = b.read()
        ebook = MIMEApplication(ebook_data, Name=fileName,
                                _subtype=getSubtype(fileExt))
        ebook.add_header('Content-Disposition', 'attachment',
                         filename=ebook.get_filename())
        msg.attach(ebook)
        newPath = path.join(dir, fileName)
        replace(filePath, newPath)


def scanAndSort(msg, directory):
    totalFileSize = 0.0
    couldNotSend = 0
    for file in scandir(kindleFolder):
        if file.is_file():
            fileExt = path.splitext(file.name)[1].lower()
            if fileExt in ebookTypes:
                totalFileSize += (file.stat().st_size / (1024*1024))
                if totalFileSize < 25:
                    attachEbook(fileName=file.name, filePath=file.path,
                                fileExt=fileExt, dir=directory, msg=msg)
                else: couldNotSend+=1
    return couldNotSend


def sendToKindle(kindleEmail, email, passwd, oneEbook=None):
    directory = path.join(kindleFolder, "SentEbooks")
    makedirs(directory, exist_ok=True)
    msg = MIMEMultipart()
    msg['Subject'] = "eBook(s) Sent"
    msg['To'] = kindleEmail
    msg['From'] = email

    if oneEbook is None:
        booksLeft = scanAndSort(msg, directory)
    else:
        attachEbook(fileName=oneEbook[0], filePath=oneEbook[1],
                    fileExt=oneEbook[2], dir=directory, msg=msg)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email, passwd)
        smtp.sendmail(email, kindleEmail, msg.as_string())
        smtp.quit()
    
    if booksLeft > 0:
        print(f"There are {booksLeft} books still in folder")


def main():
    chdir(path.dirname(path.realpath(__file__)))
    info = json.load(open("info.json"))
    kindleEmail = info.get("kindle_email")
    email = info.get("my_email")
    passwd = info.get("sender_pswd")

    if len(argv) == 3:
        if argv[1] != "-d" or argv[1] != "-k":
            print(
                "Usage: sendToKindle.py [-s <path to file in \"Downloads\" or \"Kindle\" folder or file name>]\n\n")
            exit()

        base_name = path.split(argv[2])[1].strip()
        absPath = path.join(
            downloadsPath, base_name) if argv[1] == "-d" else path.join(kindleFolder, base_name)

        if path.isfile(absPath):
            fileExt = path.splitext(base_name)[1].lower()
            if fileExt in ebookTypes:
                sendToKindle(kindleEmail, email, passwd,
                             oneEbook=(base_name, absPath, fileExt))
            else:
                print("This is not a valid file — Valid files: .epub, .mobi, .pdf\n\n")
                exit()
    else:
        sendToKindle(kindleEmail, email, passwd)


if __name__ == '__main__':
    main()
