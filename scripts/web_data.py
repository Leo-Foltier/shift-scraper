import re

import lxml
import lxml.html
import requests
from bs4 import BeautifulSoup as bs

def login(settings): #Opens scraping session and goes through the login sequence

    client = requests.session()

    loginpage = client.get(settings['loginURL'], cookies=settings['portalid']) #Gets webpage info for crsf token

    soup = bs(loginpage.text,'lxml')
    crsf_token = soup.find(id="CRSF_TOKEN")['value']

    payload = {
        'txtSecurity' : '',
        'Username' : settings['username'],
        'Password' : settings['password'],
        'CRSF_TOKEN' : crsf_token 
        }

    client.post(settings['loginURL'], cookies=settings['portalid'], data=payload, headers=settings['headers']) #Logs the user in

    start = client.get(settings['startURL'], cookies=settings['portalid']) #Gets webpage info for enaid

    soup = bs(start.text,'lxml')
    EnAID = re.search('\'..(.*)\', \'main\'', soup.find(title="Scheduling Homepage")['onclick']).group(1)

    homeURL = settings['homeURLstart'] + EnAID + settings['homeURLend']
    home = client.get(homeURL, cookies=settings['portalid']) #Gets webpage info for getting authorisation cookie

    soup = bs(home.text,'lxml')
    scheduleURL = soup.find(id="teamhoursiframe")['src'] #Url to get session specific authorisation cookie for accessing schedule and tips

    client.get(scheduleURL, cookies=settings['portalid']) 
    
    return(client)

def get_web_info(date_, client, settings): #Gets the page countent containing the schedule, xpath tree of the tipsheet and the row conatining the users info
    
    scheduleURL = settings['scheduleURL'] + date_ + '/0?' #Url for the schedule page
    schedule = client.get(scheduleURL, cookies=settings['portalid'], stream=True)
    
    tipsURL = settings['tipsURL'] + date_ + '?' #Url for the tips page
    tips = client.get(tipsURL, cookies=settings['portalid'])

    schedule.raw.decode_content = True
    rotatree = lxml.html.parse(schedule.raw)

    tablepos = 1
    while rotatree.xpath(f'//*[@id="scheduleTable"]/tbody/tr[{tablepos}]/td[1]/@data-staffid') != settings['staffID']:
        tablepos +=1

    return(rotatree, tips, tablepos)

def get_tips(tips, settings): #Returns the users tips for the week

    soup = bs(tips.text, 'lxml')

    tag = soup.find_all('input', {'data-staffid': settings['staffID']})

    totaltips = sum(float(str(n['value'])) for n in tag)

    return(totaltips)

def get_schedule(index, rotatree, tablepos): #Returns the users schedule to be processed

    
    rolelist = rotatree.xpath('//*[@id="scheduleTable"]/tbody/tr[' + str(tablepos) + ']/td[' + str(index) + ']/div/div[2]/text()') #Finds what roles the user is that day
    startendtimes = rotatree.xpath('//*[@id="scheduleTable"]/tbody/tr[' + str(tablepos) + ']/td[' + str(index) + ']/div/div[1]/text()') #Finds the start and end times for each shift
    hoursworked = rotatree.xpath('//*[@id="scheduleTable"]/tbody/tr[' + str(tablepos) + ']/td[' + str(index) + ']/div/@data-hours') #Finds the number of hours worked that day
    
    holiday = False
    if rotatree.xpath('//*[@id="scheduleTable"]/tbody/tr[' + str(tablepos) + ']/td[' + str(index) + ']/text()') == ['\n            Holiday\n        ']: #Checks if user has a holiday day
        holiday = True
    
    return(rolelist, startendtimes, hoursworked, holiday)