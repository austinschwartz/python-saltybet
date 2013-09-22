First create a Salty object.
```python
username = xxxx@gmail.com
password = hunter2
salty = new Salty(username, password)
```

To generate and access tournament information:
```python
salty.setTournamentList()
```
then either of these
```python
print salty.tournaments
salty.printTournamentList()
```
and you'll get something like
```javascript
{'start': u'September 05, 2013', 'games': u'41', 'end': u'September 06, 2013', 'id': u'85', 'name': u'Shaker Classic 7'}
{'start': u'August 30, 2013', 'games': u'3255', 'end': u'September 06, 2013', 'id': u'84', 'name': u"Salty's Dream Cast Casino 10"}
```

To generate and access stats:
```python
salty.addTournamentStats('81')
salty.addTournamentStats('82')
```
then either
```python
print salty.tournys[id]
salty.printTournamentStats(81)
```
and you'll get something like
```javascript
{
    "81": [
        {
            "bets": [
                "1160958",
                "3738143"
            ],
            "end": "12:16am",
            "winner": "Tiger + Ghetto",
            "start": "12:11am",
            "fighters": [
                "Claps + Uppercut",
                "Tiger + Ghetto"
            ],
            "betters": "1761",
            "id": "18508"
        },
        {
            "bets": [
                "901671",
                "937162"
            ],
            "end": "12:07am",
            "winner": "Killer Whale",
            "start": "12:03am",
            "fighters": [
                "Mike Tyson",
                "Killer Whale"
            ],
            "betters": "1608",
            "id": "18507"
        }
    ]
}
```
