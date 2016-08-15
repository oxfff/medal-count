#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2


class Event:
    def __init__(self, event_name, sport, g = "", s = "", b = "", started = False):
        self.name = event_name
        self.sport = sport
        self.g = g
        self.s = s
        self.b = b
        self.started = started

    def stat(self):
        return {"name": name, "sport": sport, "g": g, "s": s, "b": b, "started": started}

class Country:
  
    def __init__(self, name):

        self.name = name
        self.g = 0
        self.s = 0
        self.b = 0
        self.events = None

        self.g_list = []
        self.s_list = []
        self.b_list = []


    def add_g(self, event):
        g_list.append(event)
        self.g += 1

    def add_s(self, event):
        s_list.append(event)
        self.s += 1
    
    def add_b(self, event):
        b_list.append(event)
        self.b += 1

    def g_count(self):
        return self.g

    def s_count(self):
        return self.s

    def b_count(self):
        return self.b

class Sport:



    def __init__(self, sport):
        self.events = []
        self.sport = sport
        self.empty_event = 0
        self.empty_events = []
        self.finished_events = 0

    def empty_events(self):
        return empty_events;

    def get_events(self):
        return events

    def event_count(self):
        return len(events)

    #event = {name: "", medal: ["", "" , ""]"}
    def add_event(self, event):
        self.events.append(event)

    def event_count(self):
        return len(self.events)

    def get_name(self):
        return self.sport


    def print_event_count(self):
        print self.sport, ': ', self.event_count()

    def finished_events_count(self):
        return self.finished_events

    def empty_event_count(self):
        return self.empty_event

    def print_helper(self):
        tmp = {}
        for i in xrange(0, len(self.events)):
            if self.events[i] and self.events[i]['medal']:
                self.finished_events += 1
                gold = self.events[i]['medal'][0]

                if gold and tmp.get(gold) is None:
                    tmp[gold] = 1
                else:
                    tmp[gold] += 1
            else:
                self.empty_event += 1
                self.empty_events.append(self.events[i].get('name'))

       # sort dictionary according to value 
        retval = sorted(tmp.items(), key=lambda x: x[1], reverse = True)
        return retval

    def print_winner(self):
        retval = self.print_helper()
        country  = "N/A"
        if len(retval) > 0:
            country, count = retval[0]
        print country 

    def get_winner(self):
        retval = self.print_helper()
        country  = "N/A"
        if len(retval) > 0:
            country, count = retval[0]
        return country 


    def print_all(self): 
        rank = self.print_helper()
        if len(rank) > 0:
            for i in rank:
                country, count = i
                print country, ': ', count
            

def main():
    url= 'http://www.rio2016.com/en/medal-count-sports'
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html, "xml")


    sports_set = []

    tables = soup.find_all("table", {"class":"table-medal-sports__table"})

    for i in xrange(0, len(tables)):
        table = tables[i]
        sport_name = table.th.get_text().strip()
        #print '==============' , sport_name, '=============='
        temp_sport = Sport(sport_name)

        rows = table.findChildren(['th', 'tr'])

        for row in rows:
            cells = row.findChildren('td')

            event_stat = {"name": "", "medal": []}
            medals = []
            event = row.find_all('td', {"class": "event"})

            if len(event) > 0:
                for e in event:
                    event_stat['name'] = unicode(e.text)
            
                if len(cells) > 0:
                    for i in cells:
                        d_set = i.find_all("span", {"class":"country"})
                        if len(d_set) > 0:
                            for c in d_set:
                                medals.append(unicode(c.text))

                if len(medals) > 0: 
                    event_stat['medal'] = medals

                    #add event to sports
                temp_sport.add_event(event_stat)
        
        #done with one sport
        sports_set.append(temp_sport)


    tmp = {}
    tmp2 = {}
    total_gold = 0
    for i in sports_set:
        #print i.get_name(), i.event_count(), i.finished_events_count()
        country_name = i.get_winner()
        sport_name = i.get_name()

        if(tmp.get(country_name)):
            tmp[country_name] += 1
        else:
            tmp[country_name] = 1

        if(tmp2.get(country_name)):
            tmp2[country_name].append(sport_name)
        else:
            tmp2[country_name] = []
            tmp2[country_name].append(sport_name)


    final = sorted(tmp.items(), key=lambda x: x[1], reverse = True)
    for i in xrange(1, len(final)):
        country, count = final[i]
        total_gold += count
        l = ""
        for z in tmp2.get(country):
            l = "%s, %s" %(l, z )
        print country, count, l
   
    print 'so far %d sports have started' % total_gold

    print '%d sports to be started: '% tmp.get('N/A') 
    for x in tmp2.get('N/A'):
        print '\t', x

    
    for i in sports_set:
        print i.get_name(), i.event_count(), i.finished_events_count()
    
    print 'done'


if __name__ == '__main__':
    main()
