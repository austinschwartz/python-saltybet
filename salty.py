import sys, requests, io, json
from BeautifulSoup import BeautifulSoup

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
        self.tournys = {}
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
                tourn['id'] = indx[indx.find('=')+1::]
                tourn['name'] = x[0].getText()
                tourn['start'] = x[1].getText()
                tourn['end'] = x[2].getText()
                tourn['games'] = x[3].getText()
                tournaments.append(tourn)
        self.tournaments = tournaments

    def printTournamentList(self):
        for tournament in self.tournaments:
            print tournament

    def addTournamentStats(self, id):
        id = str(id)
        newTourny = Tournament(self.session, id)
        self.tournys[id] = newTourny

    def printTournamentStats(self, id):
        id = str(id)
        print self.tournys[id].stats

    def saveTournamentStats(self):
        tournyStats = {}
        for key in self.tournys:
            tournyStats[key] = self.tournys[key].stats
        saveJSON("stats.json", tournyStats)

class Tournament:
    def __init__(self, session, id):
        self.id = str(id)
        self.session = session
        self.stats = []
        self.getStats()

    def getStats(self):
        num = 1
        page = self.session.get("http://www.saltybet.com/stats?tournament_id=" + self.id)
        soup = BeautifulSoup(page.text)
        nextButton = [u'Next']
        tempStats = []
        while nextButton and nextButton[0] == "Next":
            page = self.session.get("http://www.saltybet.com/stats?tournament_id=" + self.id + ("&page=" + str(num) if num != 1 else ""))
            soup = BeautifulSoup(page.text)
            divs = soup.findAll("div", attrs="right")
            if divs:
                div = divs[0]
                nextButton = div.findAll("a", text="Next", attrs={"class":"graybutton"})
            else:
                nextButton = []
            tempStats += self.scrapeStats(soup)
            num += 1
        self.stats = tempStats

    def scrapeStats(self, soup):
        rows = soup.findAll("tr")
        pageStats = []
        for i in xrange(len(rows)):
            if (i != 0):
                ele = rows[i].findAll("td")
                match = {}
                url = ele[0].find("a")['href']
                fightbets = ele[0].getText().split(",")
                if len(fightbets) > 2:
                    if ("$" in fightbets[0]):
                        fightbetsa = fightbets[0]
                        fightbetsb = fightbets[1] + "," + fightbets[2]
                    else:
                        fightbetsa = fightbets[0] + "," + fightbets[1]
                        fightbetsb = fightbets[2]
                    fightbets = [fightbetsa, fightbetsb]
                fighter1 = fightbets[0].split("- $")[0]
                fighter2 = fightbets[1].split("- $")[0]
                bet1 = fightbets[0].split("- $")[1]
                bet2 = fightbets[1].split("- $")[1]
                match['id'] = url[(url.find("=")+1)::]
                match['fighters'] = [fighter1, fighter2]
                match['bets'] = [bet1, bet2]
                match['start'] = ele[2].getText()
                match['end'] = ele[3].getText()
                match['betters'] = ele[4].getText()
                if (ele[1].find("span")):
                    match['winner'] = ele[1].find("span").getText()
                    pageStats.append(match)
        return pageStats

def saveJSON(filename, contents):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(contents, ensure_ascii=False)))
