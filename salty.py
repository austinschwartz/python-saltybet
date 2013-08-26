import os, sys, urllib2, json, requests
from BeautifulSoup import BeautifulSoup
import re

loginurl = "http://www.saltybet.com/authenticate?signin=1"

headers = {
    'Host': 'www.saltybet.com',
    'Connection': 'keep-alive',
    'Content-Length': '61',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Origin': 'http://www.saltybet.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.saltybet.com/authenticate?signin=1',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8,es;q=0.6'
}

class Salty:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = None
        self.tournaments = []
        self.games = {}
        self.login()

    def login(self):
        payload = {}
        payload['email'] = self.email
        payload['pword'] = self.password
        payload['authenticate'] = 'signin'
        session = requests.Session()
        session.post(loginurl, data=payload)
        self.session = session

    def setTournamentList(self):
        page = self.session.get("http://www.saltybet.com/stats")
        soup = BeautifulSoup(page.text)
        rows = soup.findAll('tr')
        tournaments = []
        for i in xrange(len(rows)):
            tourn = {}
            x = rows[i].findAll("td")
            if (len(x) > 3):
                indx = x[0].find("a")['href']
                tourn['index'] = indx[indx.find('=')+1::]
                tourn['name'] = x[0].getText()
                tourn['start'] = x[1].getText()
                tourn['end'] = x[2].getText()
                tourn['games'] = x[3].getText()
                tournaments.append(tourn)
        self.tournaments = tournaments

    class Game:
        def __init__(self, id):
            pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "need args bro"
        quit()

    salty = Salty(sys.argv[1], sys.argv[2])
    salty.setTournamentList()

    for t in salty.tournaments:
        print t

    #a = something.get("http://www.saltybet.com/stats")
    #print a.text
