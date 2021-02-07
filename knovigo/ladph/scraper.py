import requests
from bs4 import BeautifulSoup
import csv

def printCCSDB(db):
    #iterate through table
    for t in db:
        #iterate through rows in table
        for vals in t:
            #print row
            print (vals)
        #so that we can tell when one table ends and new begins
        print ("_____NEW TABLE______")


#table 0 - first table of Los Angeles County Case Summary
def scrapeCountyCaseSummary(table):
    db = []
    t = []
    #iterate through city/community table
    for row in table.findAll('tr'):
        tds = row.findAll('td');
        vals = []
        for i in tds:
            vals.append(i.text)
        #if row is empty, should not consider it
        if (all([i == "" for i in vals])):
            continue
        #if row starts with -, it is a subrow of whatever the previous table head was
        elif (vals[0].startswith("-")):
            #print ("Table Row: " + str(vals))
            t.append(vals)

        else:
            #print ("Table Head: " + str(vals))
            db.append(t)
            t = []
            t.append(vals)
    db.append(t)
    #at the very beginning there is something with the for loop where
    #it appends an empty table
    db = db[1:]

    printCCSDB(db)
    return db

def printDB(db):
    return len(db)
    '''
    for i in db:
        print (str(i))'''

def scrapeTable(table, headerKey):
    thead = table.find('thead')
    db = []
    head = []
    for header in thead:
        tds = header.findAll(headerKey)
        for i in tds:
            head.append(i.text)

    db.append(head)
    for row in table.findAll('tr'):
        tds = row.findAll('td');
        data = []
        for i in tds:
            data.append(i.text)
        db.append(data)
    db.pop(1)
    return db

#table 1 - Second Table of Los Angeles County Case Summary
def scrapeCityCommunityCaseSummary(table, headerKey = 'th'):
    return scrapeTable(table, headerKey)

#table 2 -
#LAC DPH Laboratory Confirmed COVID-19 Recent 14-day Cumulative
# Case and Rate per 100,000 by the Top 25 Cities/Communities
def scrapeLACDPHT25(table, headerKey = 'td'):
    return scrapeTable(table, headerKey)

#table 3 - County of LA
#LAC DPH Laboratory Confirmed COVID-19 14-day Cumulative Case
# and Rate Recent Trends by City/Community1,2
def scrapeLACDPHLACounty(table, headerKey = 'td'):
    return scrapeTable(table, headerKey)

#table 4 - Cities
#LAC DPH Laboratory Confirmed COVID-19 14-day Cumulative Case
# and Rate Recent Trends by City/Community1,2
def scrapeLACDPHCities(table, headerKey = 'th'):
    return scrapeTable(table, headerKey)

#table 6 - NonRes Covid Counts
#Los Angeles County Non-Residential Settings Meeting the Criteria
# of Three or More Laboratory-confirmed COVID-19 Cases
def scrapeNonResCases(table, headerKey = 'th'):
    return scrapeTable(table, headerKey)

#table 7 - Homeless Service Settings Covid Cases
#Los Angeles County Homeless Service Settings Meeting the Criteria
# of At Least One Laboratory-confirmed COVID-19 Case
def scrapeLACHomelessSettingCovidCases(table, headerKey = 'th'):
    return scrapeTable(table, headerKey)

def scrapeLACEducationalSettingCovidCases(table, headerKey = 'th'):
    return scrapeTable(table, headerKey)

def scrapeComplianceCitations(table, headerKey = 'td'):
    pass
    #print(table.find(div, class = ))

def scrape_public_health_data():
    url = "http://publichealth.lacounty.gov/media/coronavirus/locations.htm#case-summary"
    r = requests.get(url)
    #create object by parsing the raw html content of the url
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.findAll('table')
    s = 0
    printCCSDB(scrapeCountyCaseSummary(tables[0]))
    s+= printDB(scrapeCityCommunityCaseSummary(tables[1]))
    s+= printDB(scrapeLACDPHT25(tables[2]))
    s+= printDB(scrapeLACDPHLACounty(tables[3]))
    s+= printDB(scrapeLACDPHCities(tables[4]))
    '''
    SKIPPED TABLE 5 -
    Residential Congregate and Acute Care Settings Meeting the
    Criteria of (1) At Least One Laboratory-confirmed Resident
    or (2) Two or More Laboratory-confirmed Staff in Long-Term Care
    Facilities that are not Skilled Nursing Facilities, or (3) Three
    or More Laboratory-Confirmed Staff in Shared Housing

    NO NEED FOR INFO
    '''

    s+= printDB(scrapeNonResCases(tables[6]))
    s+= printDB(scrapeLACHomelessSettingCovidCases(tables[7]))
    s+= printDB(scrapeLACEducationalSettingCovidCases(tables[8]))
    #s+= printDB(scrapeComplianceCitations(tables[9]))
    print (s)




'''print (len(tables))
for table in tables:
    for td in table.findAll('td'):
        print (td.text)
    print ("NEXT TABLE")'''
