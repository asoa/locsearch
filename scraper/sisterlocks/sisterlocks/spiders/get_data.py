#!/usr/bin/env python

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import os
import requests
import sys


class SisterLocks(scrapy.Spider):
    def __init__(self, **kwargs):
        self.name = 'base'
        self.kwargs = {k:v for k,v in kwargs.items()}
        super().__init__(name=self.name)

        # urls = ['http://www.sisterlocks.com/certified-consultant-registry-ne-nv-nj-nm--ny.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-ma-mi-mn-ms--mo.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-sc-sd-tn-tx--ut.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-international.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-al-az--ca.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-ga-hi--il.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-co-ct-de--fl.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-in-ks-ky-la--md.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-va-dc-wa--wi.html',
        #      'http://www.sisterlocks.com/certified-consultant-registry-nc-oh-ok-or-pa--ri.html']

        # urls = ['http://www.sisterlocks.com/trainee-registry-al-ar-az-ak-and-ca.html',
        #          'http://www.sisterlocks.com/trainee-registry-al-ar-az-ak-and-ca.html',
        #          'http://www.sisterlocks.com/trainee-registry-fl.html',
        #          'http://www.sisterlocks.com/trainee-registry-ga-hi-id--il.html',
        #          'http://www.sisterlocks.com/trainee-registry-in-ia-ks-ky--la.html',
        #          'http://www.sisterlocks.com/trainee-registry-md.html',
        #          'http://www.sisterlocks.com/trainee-registry-ma-mi--mn.html',
        #          'http://www.sisterlocks.com/trainee-registry-ms-mo-ne--nv.html',
        #          'http://www.sisterlocks.com/trainee-registry-nh-nj-nm--ny.html',
        #          'http://www.sisterlocks.com/trainee-registry-nc-nd-oh-ok--or.html'
        #          'http://www.sisterlocks.com/trainee-registry-nc-nd-oh-ok--or.html',
        #          'http://www.sisterlocks.com/trainee-registry-pa-ri-sc--tn.html',
        #          'http://www.sisterlocks.com/trainee-registry-tx.html']

        urls = ['http://www.sisterlocks.com/approved-trainees.html']

        self.start_urls = urls
        # no kwargs were passed in to constructor
        # print('What type of consultant do you want to crawl?')
        # sys.exit(1)

    def parse(self, response):
        """ iterate over each url in self.urls and parse xpath """
        # consultants and trainees sites
        self.divs = response.xpath('//*[@class="wsite-multicol"]')

        # consultant registry
        # fname = response.url.split('/')[3].replace('certified-consultant-registry-', 'consultant-').replace('.html', '')

        # trainee registry
        # fname = response.url.split('/')[3].replace('trainee-registry-','trainee-').replace('.html','')

        # approved trainees
        self.divs = response.xpath('/html/body/div[3]/div/div')
        fname = response.url.split('/')[3].replace('.html', '')

        with open(f"{fname}.txt", 'w') as f:
        # with open(f"{fname}-trainee.txt", 'w') as f:
            [f.write(x.extract()) for x in self.divs]


class Clean():
    def __init__(self, **kwargs):
        self.kwargs = {k:v for k,v in kwargs.items()}
        self.state = self.kwargs.get('state')

    @staticmethod
    def clean(self, line):
        pattern = re.compile(r""" 
            <div\sclass="paragraph"\sstyle="text-align:left;">
            | <u><strong>
            | </strong></u><br/>
            | <strong\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)">
            | </strong>-
            | <font\ssize="\d">
            | <div\sclass="paragraph">
            | <a\shref="https://sisterlocks.weebly.com/(\w+-\w?\w+?-?\w+).html">?\s?(target="_blank">)?(<strong>)?\w+\s\w+
            | </?strong> | </?u> | </font> | <em> | </?span> | '?</?a> 
            | <span\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)
            | <font\scolor="\#\w\d+(\w\d\w)?">
            | <font\scolor="\#\d\w\d\w\d\w"
            | style="font-weight:bold">
    
        """, re.VERBOSE)

        print(re.sub(pattern, '', str(line)))

    def get_fields(self, consultant):
        """ parse name, email, and phone number fields """
        try:
            if '<city>' in consultant:
                name = str(consultant.split('(')[0]).strip().split('<city>')[1].strip()
            else:
                name = str(consultant.split('(')[0]).strip()
            number = re.search(r'\d+-\d+-\d+', consultant).group()
            email = re.search(r'\w+@.*\.\w+', consultant).group()
            return name, number, email
        except Exception as e:
            print(f'Failed to parse {consultant}')
            return '**', '**', '**'

    def find_number(self, s):
        if re.search(r'\d+-\d+-\d+', s):
            return True

    def print_output(self, fields, city, state, ambassador='0', r_certified='0', website='NA'):
        fmt = "{{'name':'{}','phone':'{}','email':'{}','city':'{}','state':'{}','approved':'1', 'r_certified':'{}','ambassador':'{}', 'website':'{}'}}"
        print(fmt.format(fields[0].strip(), fields[1].strip(), fields[2].strip(), city.strip(), state.strip(), r_certified, ambassador, website))

    def parse_consultants(self, state_and_consultants):
        """ loop over split items and build a dict of city/consultant """
        city_pattern = re.compile(r'([A-Z]\w+\s?)*:')
        try:
            city = city_pattern.match(state_and_consultants[0]).group()
        except Exception as e:
            # print(e, state_and_consultants[0])
            print(e, state_and_consultants)
            city = 'Fix'
        # city = current_city

        for item in state_and_consultants:
            ambassador_link = re.compile(r'<a\shref="(.*weebly\.com.*\.html)"')
            if ambassador_link.search(item):
                try:
                    # ambassador code block
                    ambassador_link_pattern = re.compile(r'<a\shref="(.*weebly\.com.*\.html)"')
                    if ambassador_link_pattern.search(item):
                        link = ambassador_link_pattern.search(item).group(1)
                        html = requests.get(link).text
                        html_lines = [x for x in html.split() if len(x) > 1 and x is not None]
                        soup = BeautifulSoup(html, 'html.parser')
                        name = soup.find('title').text
                        try:
                            number = re.search(r'\(?\d{3}\)?\s?-?\d{3}-\d{4}', html).group()
                            email = re.search(r'(\w+@.*?\.\w+)', html)
                            if email:
                                _email = email.group()
                            else:
                                _email = 'NA'
                            # print(number, email)
                        except Exception as e:
                            print(e)

                    ambassador_name_pattern = re.compile(r'([A-Z]\w+\s+[A-Z]?\.?\s?[A-Z]\w+-?([A-Z]\w+)?)')
                    if ambassador_name_pattern.search(item):
                        # print(ambassador_name_pattern.search(item).group())
                        skills = self.get_skills(item)
                        if skills:
                            self.print_output((name,number,_email), city, self.state, r_certified=skills.get('r'), ambassador='1', website=link)
                except Exception as e:
                    print(e)
                # case 1 just a city
            if city_pattern.match(item) and len([x for x in item.split('<city>') if x is not '']) == 1:
                city = city_pattern.match(item).group()
                continue

            # case 2: a city and 1 or more consultants
            if city_pattern.match(item) and len([x for x in item.split('<city>') if x is not '']) > 1:
                city = city_pattern.match(item).group()
                for _item in [x for x in item.split('<br/>') if
                              x is not '<br/>' and '<a' not in x and len(x) > 5 and self.find_number(
                                      x)]:  # loop through multiple consultants/city
                    # print(city, self.state, self.get_fields(_item))
                    skills = self.get_skills(_item)
                    if skills:
                        self.print_output(self.get_fields(_item), city, self.state, r_certified=skills.get('r'))
                    else:
                        self.print_output(self.get_fields(_item), city, self.state)


            # case 3: no city and 1 or more consultants
            else:
                for _item in [x for x in item.split('<br/>') if
                              x is not '<br/>' and '<a' not in x and len(x) > 5 and self.find_number(
                                      x)]:  # loop through multiple consultants/city
                    # print(city, self.state, self.get_fields(_item))
                    skills = self.get_skills(_item)
                    if skills:
                        self.print_output(self.get_fields(_item), city, self.state, r_certified=skills.get('r'))
                    else:
                        self.print_output(self.get_fields(_item), city, self.state)

    def get_skills(self, consultant):
        """  determine if consultant is r certified, ambassador, Trichology """
        status = {'r':0, 'ambassador':0, 'trichology':0}
        r_certified_pattern = re.compile(r'''
            "R"\s+Certified"?
            | "R"\s+-\s+Certified?
            | "R"\s+CERTIFIED
        ''', re.VERBOSE)
        ambassador_pattern  = re.compile('''
            r'BRAND\s+AMBASSADOR'
            | AMBASSADOR
        ''', re.VERBOSE)

        try:
            if re.search(r_certified_pattern, consultant):
                status['r'] = 1
            if re.search(ambassador_pattern, consultant):
                status['ambassador'] = 1
            return status
        except Exception as e:
            return False

    def split_city(self, items):
        """ make a list split on cities """
        consultant_dict = {}
        # city_pattern = re.compile(r'([A-Z]\w+\s?(\w+)?\s?(\w+)?:)')
        # city_pattern = re.compile(r'([A-Z]\w+\s?:)')
        state_and_consultants = [x for x in re.split('<br/>', items) if x is not '' and x is not None]
        # print(state_and_consultants)
        self.parse_consultants(state_and_consultants)


    def pre_process(self, consultants):
        """ clean content for later parsing """

        # pattern = re.compile(r"""
        #             <div\sclass="paragraph"\sstyle="text-align:left;">
        #             | <u><strong>
        #             | </strong></u><br/>
        #             | <strong\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)">
        #             | </strong>-
        #             | <font\ssize="\d">
        #             | <div\sclass="paragraph">
        #             | <a\shref="https://sisterlocks.weebly.com/(\w+-\w?\w+?-?\w+).html">?\s?(target="_blank">)?(<strong>)?
        #             | </?strong> | </?u> | </font> | </?em> | </?span> | '?</?a> | "> | \u200b | </div> |
        #             | <span\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)
        #             | <font\scolor="\#\w\d+(\w\d\w)?">
        #             | <font\scolor="\#\d\w\d\w\d\w"
        #             | <font\scolor="\#\w+\d+
        #             | style="font-weight:bold">
        #
        #         """, re.VERBOSE)
        pattern = re.compile(r""" 
                    <div\sclass="paragraph"\sstyle="text-align:left;">
                    | <u><strong>
                    | </strong></u><br/>
                    | <strong\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)">
                    | </strong>-
                    | <font\ssize="\d">
                    | <div\sclass="paragraph">
                    | </?strong> | </?u> | </font> | </?em> | </?span> | '?</?a>  | \u200b | </div> | 
                    | <span\sstyle="color:rgb\(\d+,\s\d+,\s\d+\)
                    | <font\scolor="\#\w\d+(\w\d\w)?">
                    | <font\scolor="\#\d\w\d\w\d\w"
                    | <font\scolor="\#\w+\d+
                    | style="font-weight:bold">

                """, re.VERBOSE)
        pattern2 = re.compile(r"\xa0")
        pattern3 = re.compile(r'([A-Z]\w+\s?)([A-Z]\w+\s?)?([A-Z]\w+\s?)?:')

        for consultant in consultants:
            # clean2(consultant)
            # print(consultants)
            # city = consultant.find_all('u')
            # print(city)
            # print(consultants)
            _consultants = re.sub(pattern, '', str(consultant))
            _consultants = re.sub(pattern2,' ', _consultants)
            # \1\2\3 include the first 3 capture groups
            _consultants = pattern3.sub(r'\1\2\3:<city>', _consultants)
            # print(_consultants)
            self.split_city(_consultants)

    def prod(self):
        """ entrypoint into class; iterates over each state html container """

        BASE_DIR = 'scraper/sisterlocks/sisterlocks/spiders'

        # consultants
        # for file in ['consultant-al-az--ca.txt', 'consultant-co-ct-de--fl.txt', 'consultant-ga-hi--il.txt', 'consultant-in-ks-ky-la--md.txt', 'consultant-international.txt', 'consultant-ma-mi-mn-ms--mo.txt', 'consultant-nc-oh-ok-or-pa--ri.txt', 'consultant-ne-nv-nj-nm--ny.txt', 'consultant-sc-sd-tn-tx--ut.txt', 'consultant-va-dc-wa--wi.txt']:

        # trainees
        for file in ['trainee-al-ar-az-ak-and-ca.txt', 'trainee-fl.txt', 'trainee-ga-hi-id--il.txt', 'trainee-in-ia-ks-ky--la.txt', 'trainee-ma-mi--mn.txt', 'trainee-md.txt', 'trainee-ms-mo-ne--nv.txt', 'trainee-nh-nj-nm--ny.txt', 'trainee-pa-ri-sc--tn.txt', 'trainee-tx.txt']:
            with open(os.path.abspath(file), 'r') as f:
                # lines = [x for x in f.readlines()]
                soup = BeautifulSoup(f.read(), features="lxml")

                containers = soup.find_all('tr', attrs={'class': 'wsite-multicol-tr'})

                for container in containers:
                    try:
                        state = container.find('h2').text
                        consultants = [x for x in container.find_all('div', attrs={'class': 'paragraph'}) if len(x.text) > 0]
                        self.state = state
                        self.pre_process(consultants)

                    except Exception as e:
                        print(e)


    def dev(self):
        """ parse content from html using class tags; used for testing """

        with open('website_data.txt', 'r') as f:
            # lines = [x for x in f.readlines()]
            soup = BeautifulSoup(f.read(), features="lxml")

        containers = soup.find_all('tr',attrs={'class':'wsite-multicol-tr'})

        for container in containers:
            try:
                state = container.find('h2').text
                consultants = [x for x in container.find_all('div',attrs={'class':'paragraph'}) if len(x.text) > 0]
                # print(state.find('h2').text, state.find_all('div',attrs={'class':'paragraph'}))
                # print(_state, cities)
                self.state = state
                self.pre_process(consultants)

            except Exception as e:
                print(e)


class CleanApproved(Clean):
    """ class inherits from Clean and processes the approved trainees """
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = {k:v for k,v in kwargs.items()}
        files = self.kwargs.get('files')

        # for file in ['approved-trainees.txt']:
        for file in files:
            with open(os.path.abspath(file), 'r') as f:
                # lines = [x for x in f.readlines()]
                soup = BeautifulSoup(f.read(), features="lxml")

                containers = soup.find_all('div', attrs={'class': 'paragraph'})

                for container in containers:
                    try:
                        state_pattern = re.compile(r'([A-Z]{2,}\w+\s?)+')
                        if state_pattern.search(str(container)):
                            state = state_pattern.search(str(container)).group().strip('<,>')
                            # print(state, container)
                            for item in re.split(r'<br/>', str(container))[1:]:
                                try:
                                    if state_pattern.search(str(item)):
                                        state = state_pattern.search(str(item)).group().strip('>,<')
                                        continue
                                    # print(item)
                                    city_pattern = re.compile(r'[A-Z]\w+\s?([A-Z]\w+)?:')
                                    # city_pattern = re.compile(r'[A-Z]\w+:|[A-Z]\w+,\s\w\.\w\.')
                                    if city_pattern.search(str(item)):
                                        # print(city.search(str(item)))
                                        city = city_pattern.search(str(item)).group().strip('>,:<')
                                        continue
                                    # consultant
                                    # if '(' in item:
                                    name = re.search(r'[A-Z]\w+\s+[A-Z]?\.?\s?[A-Z]\w+-?([A-Z]\w+)?', item).group()
                                    if name:
                                        # name = item.split('(')[0].strip()
                                        number = re.search(r'\d+-\d+-\d+', item).group()
                                        email = re.search(r'\w+@.*\.\w+', item).group().split('>')[1]
                                        fields = (name, number, email)
                                        self.print_output(fields,city,state)
                                        # print(state,city,name,number,email)
                                    else:
                                        continue
                                except Exception as e:
                                    print(f'Failed to parse {item, state}')
                    except Exception as e:
                        print(e)


def main():
    # # inits spider to crawl website and create raw data html files
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(SisterLocks)  # call the base spider
    # process.start()  # the script will block here until the crawling is finished

    #cleans raw html files and outputs input files to data model
    # obj = Clean()
    # # obj.dev()
    # obj.prod()

    # clean approved trainees
    obj = CleanApproved(files=['approved-trainees.txt'])



if __name__ == "__main__":
    main()
