import copy
import ipaddress
import socket
import urllib.request
import ssl
import whois
import requests
from datetime import date, datetime, timedelta


class ExtractFeatues:


    def __init__(self, url, N ,featureslist):
        self.url =  url
        self.features = [0] * N
        self.featuresnames = featureslist
        self.checkFeatures(self.url)


    def checkFeatures(self, url):
        i = 0
        urlcopy = copy.copy(url)


        i = self.checkIfIP(i, urlcopy)
        i = self.checkLength(i, urlcopy)
        # i = self.checkShortened(i, urlcopy)
        i = self.checkat(i, urlcopy)
        i = self.checkredirection(i, urlcopy)
        i = self.checkdash(i, urlcopy)
        i = self.checksubdomains(i, urlcopy)
        i = self.checkcertificate(i, urlcopy)
        i = self.checkregistrationdate(i, urlcopy)
        i = self.nonStandardPort(i, urlcopy)
        i = self.httpsInsidename(i, urlcopy)

        #Na sam koniec musi być walidacja czy link pshishingowy czy nie 
        print(self.features)


    def checkIfIP(self, i, url):
        urlparts = url.split('/')

        for part in urlparts:
            try:
                if socket.inet_aton(part):
                    self.features[i] = 1
                    return i + 1
            except socket.error:
                continue

        return i + 1


    def checkLength(self, i, url):

        if len(url) > 54:
            self.features[i] = 0.5

        if len(url) >= 75:
            self.features[i] += 0.5


        return i + 1


    def checkShortened(self, i, url):
        resp = urllib.request.urlopen(url)

        if resp != url:
            self.checkFeatures(resp.url)
            print('Redirection!')

        return i + 1


    def checkat(self, i, url):
        if url.find('@') != 1:
            self.features[i] = 1

        return i + 1


    def checkredirection(self, i, url):
        if url.find('//', 7):
            self.features[i] = 1

        return i + 1

    def checkdash(self, i, url):
        start = url.find('//')
        stop = url.find('/', start + 2)

        if url.find('-', start, stop):
            self.features[i] = 1

        return i + 1


    def checksubdomains(self, i, url):
        wwwpos = url.find('www.')
        name = url.find('.', wwwpos + 4)
        stop = url.find('/', name + 1)
        numberofsubdomains = 0
        start = name + 1

        for j in range(stop):
            if url.find('.', start):
                numberofsubdomains += 1
                start = url.find('.', start) + 1


        if numberofsubdomains > 1:
            self.features[i] = 1

        return i + 1


    def checkcertificate(self, i, url):
        try:
            response = requests.get(url, verify = True)
            if response.status_code != 200:
                self.features[i] = 1
        except:
            self.features[i] = 1

        return i + 1


    def checkregistrationdate(self, i , url):
        w = whois.whois(url)
        today = date.today().strftime("%Y-%m-%d %H:%M:%S")
        date_today_obj = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
        difference = date_today_obj - w.creation_date

        if difference < timedelta(days=365):
            self.features[i] = 1

        return i + 1


    def faviconsource(self, i, url):
        #Work in proggress
        exit()


    def nonStandardPort(self, i, url):
        sus_ports = [21, 22, 23, 80, 445, 1433, 1521, 3306, 3389]
        ports = [80, 443]
        final_est = 0

        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((url, int(port)))
                s.shutdown(2)
            except:
                final_est += 0.5

        for sus_port in sus_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((url, int(sus_port)))
                s.shutdown(2)
                final_est += 0.5
            except:
                continue

        self.features[i] = final_est
        return i + 1


    def httpsInsidename(self, i, url):
        start = url.find('//')
        stop = url.find('https', start + 2)

        if stop != -1:
            self.features[i] = 1
        
        return i + 1


    def externalSourceContent(self, i, url):
        print('Hello')

ExtractFeatues('https://expired.badssl.com/', 30, 's')