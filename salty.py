import sys, requests
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

    def addGameStats(self, id):
        newGame = Game(self.session, id)
        self.games[id] = newGame

    def printGameStats(self, id):
        print self.games[id].stats

    def printGamesList(self):
        for game in self.games:
            print game

class Game:
    def __init__(self, session, id):
        self.id = id
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
            tempStats.append(self.scrapeStats(soup))
            num += 1
        return tempStats

    def scrapeStats(self, soup):
        rows = soup.findAll("tr")
        for row in rows:
            print row, "\n"
        return "asd"

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "need args bro"
        quit()

    salty = Salty(sys.argv[1], sys.argv[2])
    #salty.setTournamentList()
    #salty.printTournamentList()

    salty.addGameStats('80')
    salty.printGamesList()
    salty.printGameStats('80')


    #a = something.get("http://www.saltybet.com/stats")
    #print a.text
