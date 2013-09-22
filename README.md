First create a Salty object.
```python
username = xxxx@gmail.com
password = hunter2
salty = new Salty(username, password)
```

To generate and access tournament information:
```python
salty.setTournamentList()

print salty.tournaments
salty.printTournamentList()
```
```javascript
{'start': u'September 05, 2013', 'games': u'41', 'end': u'September 06, 2013', 'id': u'85', 'name': u'Shaker Classic 7'}
{'start': u'August 30, 2013', 'games': u'3255', 'end': u'September 06, 2013', 'id': u'84', 'name': u"Salty's Dream Cast Casino 10"}
```

To generate and access stats:
```python

```
