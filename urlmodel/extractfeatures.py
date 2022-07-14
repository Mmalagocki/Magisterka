from calendar import c
from cmath import nan
import copy
import ipaddress
from platform import release
import socket
import urllib.request
import ssl
import whois
import requests
from datetime import date, datetime, timedelta
import favicon
from bs4 import BeautifulSoup
import urllib.request as urllib2
import urllib3
import re
import validators
import time
import hashlib
from urllib.request import urlopen, Request
import pandas as pd

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import timedelta
import dns.resolver
import json
from pandas import json_normalize


from client import RestClient
import advertools as adv
from tld import get_tld

class ExtractFeatues:

    def __init__(self, N = 30):
        self.features = [0] * N
        self.api_key = '53eafd91810c4892b7b869d60928ac98'


################################ UTILS ################################


    def getReponseGoogle(self, url):
        return 0
        client = RestClient("216832@edu.p.lodz.pl", "d6d724224f05d4bf")
        post_data = dict()
        # You can set only one task at a time
        post_data[len(post_data)] = dict(
            target=url
        )
        # POST /v3/traffic_analytics/similarweb/live
        response = client.post("/v3/traffic_analytics/similarweb/live", post_data)
        # you can find the full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
        if response["status_code"] == 20000:
                print(response)
        # do something with result
        else:
            print("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))


    def getContentFromPage(self, elem, attribute, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html_page = urllib2.urlopen(url, context=ctx)

        soup = BeautifulSoup(html_page, features="html5lib")
        elems = []
        for img in soup.findAll(elem,  limit=None, recursive=True):
            elems.append(img.get(attribute))
        
        return elems


    def getBaseUrl(self, url):
            urln_start = url.find('//')
            url_stop = url.find('/', urln_start + 2)
            desired_url = url[0:url_stop]

            return desired_url

    def checkHeadElem(self, elems, site_name):
        sus_elems = 0

        for elem in elems:
            if elem == None:
                continue

            if validators.url(elem):
                result = elem.find(site_name)
                if result == -1:
                    sus_elems += 1
                else:
                    continue

            else:
                continue

        return sus_elems



###########################################################################


    def checkFeatures(self, url):
        i = 0
        urlcopy = copy.copy(url)

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        i = self.checkIfIP(i, urlcopy)
        i = self.checkLength(i, urlcopy)
        i = self.checkShortened(i, urlcopy)
        i = self.checkat(i, urlcopy)
        i = self.checkredirection(i, urlcopy)
        i = self.checkdash(i, urlcopy)
        i = self.checksubdomains(i, urlcopy)
        i = self.checkcertificate(i, urlcopy)
        i = self.checkregistrationdate(i, urlcopy)
        i = self.nonStandardPort(i, urlcopy)
        i = self.httpsInsidename(i, urlcopy)
        i = self.faviconsource(i, urlcopy)
        i = self.externalSourceContent(i, urlcopy)
        i = self.CheckLinks(i, urlcopy)
        i = self.CheckHead(i, urlcopy)
        i = self.CheckForms(i, urlcopy)
        i = self.CheckIfMailing(i, urlcopy)
        i = self.CheckAbnormalURL(i, urlcopy)
        i = self.CheckRedirection(i, urlcopy)
        i = self.CheckStatusBar(i, urlcopy)
        i = self.CheckRightClickDisabled(i, urlcopy)
        i = self.CheckPopup(i, urlcopy)
        i = self.CheckIFrameRedirection(i, urlcopy)
        i = self.CheckAgeOfDomain(i, urlcopy)
        i = self.CheckDNSRecord(i, urlcopy)
        i = self.CheckPageRank(i, urlcopy)
        i = self.CheckPageTraffic(i, urlcopy)
        i = self.CheckGoogleIndex(i, urlcopy)
        i = self.CheckLinksPointingtoPage(i, urlcopy)
        i = self.StatisticalReportsBased(i, urlcopy)

        #Na sam koniec musi być walidacja czy link pshishingowy czy nie 
        print(self.features)
        return self.features



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
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib.request.urlopen(url, context=ctx)

        if resp != url:
            # self.checkFeatures(resp.url)
            self.features[i] += 1

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
        icons = favicon.get(url, verify=False)

        if not icons:
            self.features[i] = 1
            return i + 1

        else:
            icon_url = icons[0].url
            start = url.find('//')
            stop = url.find('/', start + 2)
            desired_url = url[0:stop]

            icon_start = icon_url.find('//')
            icon_stop = icon_url.find('/', icon_start + 2)
            icon_base_url = icon_url[0:icon_stop]

            if desired_url != icon_base_url:
                self.features[i] = 1
                return i + 1
            
            else:
                self.features[i] = 0
                return i + 1


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
        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE
        # html_page = urllib2.urlopen(url, context=ctx)

        # soup = BeautifulSoup(html_page, features="html5lib")
        # images = []
        # for img in soup.findAll('img',  limit=None, recursive=True):
        #     images.append(img.get('src'))


        images = self.getContentFromPage('img', 'src', url)
        base_url = self.getBaseUrl(url)
        number_of_links = 0
        external_links = 0
        if images:
            for img in images:
                base_img_url = self.getBaseUrl(img)
                if base_url != base_img_url:
                    external_links += 1
                else:
                    continue

            result = external_links / number_of_links
            if result < 0.22:
                self.features[i] = 0
                return i + 1
            if (result > 0.22) and (result < 0.61):
                self.features[i] = 0.5
                return i + 1
            if result > 0.61:
                self.features[i] = 1
                return i + 1
            else:
                print('Something went wrong!')
                return i + 1
        else:
            self.features[i] = 1
            return i + 1


    def CheckLinks(self, i, url):
        links = self.getContentFromPage('a', 'href', url)
        base_url = self.getBaseUrl(url)
        number_of_links = len(links)
        external_links = 0

        if links:
            for img in links:
                base_img_url = self.getBaseUrl(img)
                if base_url != base_img_url:
                    external_links += 1
                else:
                    continue

            result = external_links / number_of_links
            if result < 0.31:
                self.features[i] = 0
                return i + 1
            if (result > 0.31) and (result < 0.67):
                self.features[i] = 0.5
                return i + 1
            if result > 0.67:
                self.features[i] = 1
                return i + 1
            else:
                print('Something went wrong!')
                return i + 1
        else:
            self.features[i] = 1
            return i + 1


    def CheckHead(self, i, url):
        meta = self.getContentFromPage('meta', 'content', url)
        script = self.getContentFromPage('script', 'src', url)
        link = self.getContentFromPage('link', 'href',  url)

        is_www = url.find('www.')
        if is_www == -1:
            urln_start = url.find('//')
            url_stop = url.find('.', urln_start + 2)
            site_name = url[urln_start+2:url_stop]
        else:
            urln_start = url.find('www.')
            url_stop = url.find('.', urln_start + 4)
            site_name = url[urln_start+4:url_stop]

        N_elems = len(meta) + len(script) + len(link)
        sus_elems = 0
        sus_elems += self.checkHeadElem(meta, site_name)
        sus_elems += self.checkHeadElem(meta, site_name)
        sus_elems += self.checkHeadElem(meta, site_name)

        if sus_elems != 0:
            result = sus_elems/N_elems
            if result < 0.17:
                self.features[i] = 0
            if result > 0.17 and result <0.81:
                self.features[i] = 0.5
            else:
                self.features[i] = 1

        return i + 1


    def CheckForms(self, i, url):
        forms = self.getContentFromPage('form', 'action', url)
        base_url = self.getBaseUrl(url)

        if forms != None:
            for form in forms:
                base_action_url = self.getBaseUrl(form)
                if base_url == base_action_url:
                    self.features[i] = 0
                else:
                    self.features[i] = 1
        return i + 1


    def CheckIfMailing(self, i, url):
        forms = self.getContentFromPage('form', 'action', url)
        if forms:
            if forms[0].find('mailto:'):
                self.features[i] = 1
            else:
                self.features[i] = 0
        return i + 1


    def CheckAbnormalURL(self, i, url): 
        domain = whois.whois(url)
        is_www = url.find('www.')
        if is_www == -1:
            urln_start = url.find('//')
            url_stop = url.find('.', urln_start + 2)
            site_name = url[urln_start+2:url_stop]
        else:
            urln_start = url.find('www.')
            url_stop = url.find('.', urln_start + 4)
            site_name = url[urln_start+4:url_stop]
        found = False

        if domain:
            for name in domain.domain_name:
                result = name.find(site_name)
                if result != -1:
                    found = True

        if found == True:
            self.features[i] = 0
        else:
            self.features[i] = 1

        return i + 1


    def CheckRedirection(self, i, url):
        responses = requests.get(url, verify=False)

        if responses.history:
            if len(responses.history) <= 1:
                self.features[i] = 0
            if len(responses.history) >= 2 and len(responses.history) <= 4:
                self.features[i] = 0.5
            else:
                self.features[i] = 1
        else:
            self.features[i] = 0

        return i + 1


    def CheckStatusBar(self, i, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urlopen(url, context=ctx).read()
        currentHash = hashlib.sha224(response).hexdigest()
        time.sleep(10)
        response = urlopen(url, context=ctx).read()
        newHash = hashlib.sha224(response).hexdigest()

        if newHash == currentHash:
            self.features[i] = 0
        else:
            self.features[i] = 1

        return i + 1


    def CheckRightClickDisabled(self, i, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html_page = urllib2.urlopen(url, context=ctx)

        soup = BeautifulSoup(html_page, "html.parser")
        html_url = str(soup.find("html"))
        out = re.search("event.button==2", html_url)
        if out is not None:
            self.features[i] = 1
            return i + 1
        else:
            self.features[i] = 0
            return i + 1


    def CheckPopup(self, i, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors");
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        driver.get("http://www.google.com/")
        driver.get(url)
        elements = driver.find_elements(By.TAG_NAME, "div")
        time.sleep(5)

        new_elements = driver.find_elements(By.TAG_NAME, "div")
        if elements != new_elements:
            print('Smth new')
            self.features[i] = 1
        else:
            print('Nothing new')
            self.features[i] = 0

        return i + 1


    def CheckIFrameRedirection(self, i, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors");
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        driver.get(url)
        elements = driver.find_elements(By.TAG_NAME, "iframe")
        if not elements:
            self.features[i] = 0
        else:
            self.features[i] = 1
        
        return i + 1


    def CheckAgeOfDomain(self, i, url):
        w = whois.whois(url)
        now = datetime.now()

        if w.creation_date < now + timedelta(days=-183):
            self.features[i] = 0
        else:
            self.features[i] = 1

        return i + 1


    def CheckDNSRecord(self, i, url):
        try:
            answers = dns.resolver.resolve(url,'NS')
            if answers:
                self.features[i] = 0
        except:
            self.features[i] = 1

        return i + 1


    def CheckPageRank(self, i , url):
        is_www = url.find('www.')
        if is_www == -1:
            urln_start = url.find('//')
            url_stop = url.find('.com', urln_start + 2)
            site_name = url[urln_start+2:url_stop+4]
        else:
            urln_start = url.find('www.')
            url_stop = url.find('.com', urln_start + 4)
            site_name = url[urln_start+4:url_stop+4]

        response = self.getReponseGoogle(site_name)
        with open('my_data.json') as json_file:
            dict = json.load(json_file)
            df = pd.DataFrame(dict['tasks'])
        ranking = pd.DataFrame(df['result'][0])
        global_rank = ranking['global_rank'][0]['rank']

        if global_rank == 0:
            self.features[i] = 1
        else:
            self.features[i] = 0

        return i + 1 


    def CheckPageTraffic(self, i, url):
        is_www = url.find('www.')
        if is_www == -1:
            urln_start = url.find('//')
            url_stop = url.find('.com', urln_start + 2)
            site_name = url[urln_start+2:url_stop+4]
        else:
            urln_start = url.find('www.')
            url_stop = url.find('.com', urln_start + 4)
            site_name = url[urln_start+4:url_stop+4]

        response = self.getReponseGoogle(site_name)
        with open('my_data.json') as json_file:
            dict = json.load(json_file)
            df = pd.DataFrame(dict['tasks'])
        ranking = pd.DataFrame(df['result'][0])
        traffic = ranking['traffic'][0]['value']

        if traffic > 100000:
            self.features[i] = 0
        elif traffic > 50000:
            self.features[i] = 0.5
        else:
            self.features[i] = 1

        return i + 1 


    def CheckGoogleIndex(self, i, url):
        cx = '8808f52f17927371a'
        key = 'AIzaSyCfg8zEmQMGw0FYqHdnOJqMEJQYQzfXRog'
        link_to_analyze = 'site:' + url

        result = adv.serp_goog(cx=cx, key=key, q=link_to_analyze)

        if 'rank' in result:
            rank = str(result['rank'][0])
            if rank == 'nan':
                self.features[i] = 1
            else:
                self.features[i] = 0
        else:
            self.features[i] = 1

        return i + 1 

    def CheckLinksPointingtoPage(self, i, url):
        links = self.getContentFromPage('a', 'href', url)
        base_url = self.getBaseUrl(url)
        number_of_links = len(links)
        external_links = 0

        if links:
            for img in links:
                base_img_url = self.getBaseUrl(img)
                if base_url != base_img_url:
                    external_links += 1
                else:
                    continue
        if (external_links - number_of_links) <= 2:
            self.features[i] = 0.5
        elif (external_links - number_of_links) == 0:
            self.features[i] = 1
        else:
            self.features[i] = 0

        return i + 1 


    def StatisticalReportsBased(self, i, url):
        res = get_tld(url, as_object=True)
        sus_tld = ['com', 'ml', 'tk', 'io', 'org', 'ga', 'cf', 'gq', 'net', 'me']
        if res.tld in sus_tld:
            self.features[i] = 1
        else:
            self.features[i] = 0

        return i + 1 

######################################################
object = ExtractFeatues(30)
# object.checkFeatures('https://expired.badssl.com/')
object.checkFeatures('https://bt-email-log-in.weeblysite.com/')