from os import listdir, mkdir
from os.path import isfile
from time import sleep
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def checkFiles():
    files, needed, missing = listdir(), ["credentials.txt", "content.txt", "mails.txt", "attachments"], []
    for data in needed:
        if data not in files: missing.append(data)
    return missing

def createCred():
    text = "Email => yourmail@yourmail.com\nPassword => yourpassword"
    file = open("credentials.txt", "w+")
    file.write(text)
    file.close()
    print("credentials.txt created.")

def createContent():
    text = "Yor mail subject is here\nYour mail here"
    file = open("content.txt", "w+")
    file.write(text)
    file.close()
    print("content.txt created.")
    
def createMails():
    text = "MailsHere@exampleMail.com\nMailsHere2@exampleMail.com"
    file = open("mails.txt", "w+")
    file.write(text)
    file.close()
    print("mails.txt created.")
    
def createAttach():
    mkdir("attachments")
    print("attachments directory created")

def install(missingFiles):
    print("There is missing files. Installation starts.\n")
    for missingFile in missingFiles:
        if missingFile == "credentials.txt": createCred()
        elif missingFile == "content.txt": createContent()
        elif missingFile == "mails.txt": createMails()
        elif missingFile == "attachments": createAttach()
    print("\nInstallation complete. Please fill the files and restart program to continue")

def deleteSpaces(text): #in case if user accidentally puts unnecessary spaces
    if len(text) == 0: return ""
    while text[0] == " ":
        if len(text) == 1: return ""
        text = text[1:];
    while text[-1] == " ":
        if len(text) == 1: return ""
        text = text[:-1]
    return text

def splitContent(content):
    for key in range(len(content)-1):
        if content[key] == "\n":
            return (content[:key], content[key+1:])
    return (content, "")

def getData():
    #get credentials
    creds = open("credentials.txt", "r")
    data = creds.read().split("\n")
    if len(data) != 2: input("Your credentials are missing."); exit()
    id, password = deleteSpaces(data[0].split("=>")[-1]), deleteSpaces(data[1].split("=>")[-1]) #splitting reduces performance
    creds.close()
    creds = (id, password)
    
    #get content
    content = open("content.txt", "r")
    data = splitContent(content.read())
    content.close()
    content = data
    
    #get mails
    mails = open("mails.txt", "r")
    data = list(map(deleteSpaces, [mail for mail in mails.read().split("\n") if mail != ""]))
    mails.close()
    mails = data
    
    #get attachments
    attachments = ["attachments/" + value for value in listdir("attachments/") if isfile("attachments/" + value)]
    
    #check
    if creds[0] == "": input("Your email is missing."); exit() #input because I want to show the error message before program stops.
    if creds[1] == "": input("Your password is missing."); exit()
    if content[0] == "": input("Your mail subject is missing."); exit()
    if len(mails) == 1 and mails[0] == "": input("Mails are missing."); exit()
    
    return creds, content, mails, attachments
    
def printData(creds, content, mails, attachments):
    print("Your Email adress => " + creds[0] + "\nYour password => " + creds[1] + "\n\nYour mail subject => " + content[0] + "\nYour mail content =>\n" + content[1] + "\n\nAttachments =>\n\n" + "\n".join(attachments) + "\n\nMails=>\n\n" + "\n".join(mails))
    
def sendMails(creds, content, mails, attachments):
    print()
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(creds[0], creds[1])
    for receiver in mails:
        msg = MIMEMultipart()
        msg['From'] = creds[0]
        msg['To'] = receiver
        msg['Subject'] = content[0]
        msg.attach(MIMEText(content[1], 'plain'))
        for attachment in attachments:
            attach_file = open(attachment, "rb")
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload)
            filename = attachment.split("/")[1]
            payload.add_header("Content-Disposition", f"attachment; filename= {filename}")
            msg.attach(payload)
        text = msg.as_string()
        session.sendmail(creds[0], receiver, text)
        print("Mail sent to " + receiver)
        sleep(30 + randint(0,30))
    session.quit()
    print("\nMails sent")

def main():
    #check files
    missingFiles = checkFiles()
    if missingFiles:
        install(missingFiles)
        return()
    
    #get data
    creds, content, mails, attachments = getData()
    
    #ask if user wants to continue
    printData(creds, content, mails, attachments)
    answer = input("\nAre you sure you want to send the mails (y/n) => ")
    while answer not in ["y", "n"]:
        answer = input("Are you sure you want to send the mails (y/n) => ")
    if answer == "n": return
    
    #send mails
    sendMails(creds, content, mails, attachments)

if __name__ == "__main__":
    main()
    input()
