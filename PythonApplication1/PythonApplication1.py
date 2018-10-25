import requests
from lxml import html
from bs4 import BeautifulSoup
import re
import sys
import datetime
curversionlink = 'a36-7ecbac6055b0fd097177e43469d5d846.pck'
curversion = "3.45"
USERNAME = "jacob-f-larsen@hotmail.com"
PASSWORD = "xxx"

LOGIN_URL = "https://account.worxlandroid.com/login"
URL = "https://account.worxlandroid.com/product-items/30173504170106010009"

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Notification sent")
    except:
        print("FAILED to send notification to ") + TO[0]

def main():
    session_requests = requests.session()

    # Get login token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]

    # Create payload
    payload = {
        "email": USERNAME,
        "password": PASSWORD,
        "_token": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//div[@class='Version']/a/text()")

    #print(bucket_names)
    recipients = ["jacob-f-larsen@hotmail.com"]
    adminrecipients = ["jacob-f-larsen@hotmail.com", "anders8585@gmail.com"]
    soup = BeautifulSoup( result.content, 'html.parser' )
    #print(soup)
    linkarray = []
    for link in soup.find_all('a'):
        s = link.get('href')
        string = link
        #print(s)
        linkarray.append(s)
        #print(my_list[1])
        #print(string)
       # if re.search(r"https://s3.eu-west-1.amazonaws.com/firmware.worxlandroid.com/" + curversionlink, s):
       #     print(s)
       #     print("Version is updated")
       # elif re.search('https://s3.eu-west-1.amazonaws.com/firmware.workxlandroid.com/(.*).pck', s):
       #     print(s)
       #     print("Version is old")
    print(linkarray[9])

    count = 0
    for link in linkarray:
        count += 1
        if count == 10 and link[8] != "s":
            print("Something is wrong!")
            send_email('jakedotre@gmail.com', 'xx', adminrecipients, 'Buller - ERROR','Something is wrong! \nCount was 9 but link[8] was not "s"\nLink at count is: ' + link)
            
    for elem in soup.find_all(text = re.compile("Version")):
        string = soup.get_text()
        #print(string)
        clean = re.sub('<[^<]+?>', '', string)
        space = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", clean).strip()
        s = str(elem.parent)
        if re.search(curversion, string):
            print("OK - UPDATED!")
            #print clean
            #with open("/home/pi/Public/landroid/log2.txt", "a") as logfile:
            #    logfile.write("OK - " + str(datetime.date.today()) + "\n")
        else:
            print("Possibly new update available")
            #
            send_email('jakedotre@gmail.com','x', recipients, 'Buller skal opdateres!', 'Buller skal nu opdateres! \nDownload opdateringen direkte fra: ' + linkarray[9] + ' \n\n(Guide til opdatering: https://www.worxlandroid.com/en/learn/software-upgrade-landroid-s/ ) \n\n\nHilsen Raspberry Pi' )
            #with open("/home/pi/Public/landroid/log2.txt", "a") as logfile:
            #    logfile.write("New Update - " + str(datetime.date.today()) + "\n")

if __name__ == '__main__':
    main()
