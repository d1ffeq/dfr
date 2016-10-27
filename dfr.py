import sys 
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
from urllib.request import urlopen




class DialogFeedReader:
    def __init__(self):
        self.parse = HTMLParser()
        self.link_list = self.read_feedlinks()
        self.news = []
        self.get_feed()


    def read_feedlinks(self):
        f = open('feed.txt', 'a+').close()
        txt = open('feed.txt', 'rU').read()
        lines = txt.splitlines()
        line_list = [line for line in lines if line]
        return line_list


    def write_feedlinks(self, feedlinks):
        txt = open('feed.txt', 'w')
        for line in feedlinks:
            txt.write('{}\n'.format(line))


    def get_feed(self):
        print('\nFetching news feed\n')
        for link in self.link_list:
            try:
                req = urlopen(link).read()
            except ValueError:
                print('\nInvalid link, skipping\n')
            tree = ET.ElementTree(ET.fromstring(req)).getroot()
            for i in tree.iter('title'):
                source_name = i.text.split('-')[0]
                break
            for e in tree.iter('item'): 
                news_element = []
                news_element.append(self.parse.unescape(e.find('title').text))
                news_element.append(self.parse.unescape(e.find('link').text))
                news_element.append(self.parse.unescape(e.find('description').text.split('<')[0]))
                news_element.append(source_name)
                self.news.append(news_element)


    def print_feedtitles(self):
        print('\nNews Feed:\n')
        for i in range(0, len(self.news)):
            print('[{}] {} - {}'.format(i + 1, self.news[i][0], self.news[i][3]))
        print('\n')


    def add_feedlink(self):
        link = input('Enter link: ')
        try:
            urlopen(link).read()
            if link and not link in self.link_list:
                self.link_list.append(link)
                self.write_feedlinks(self.link_list)
                print('\nLink added!\n')
        except ValueError:
            print('\nInvalid link\n')


    def print_link(self):
        try:
            num = int(input('\nEnter line number of to get link for: '))
            if (num - 1) < len(self.news):
                print('\nLink:\n{}\n'.format(self.news[num - 1][1]))
        except ValueError:
            print('\nWrong number input\n')


    def print_description(self):
        try: 
            num = int(input('\nEnter line number of to get link for: '))
            if (num - 1) < len(self.news):
                print('\Description:\n{}\n'.format(self.news[num - 1][2]))
        except ValueError:
            print('\nWrong number input\n')


root = DialogFeedReader()
help = '''\nAvailable commands: 
(a)dd new RSS feed link
(u)pdate feed 
(p)rint titles
(g)et news link
(r)ead link description
(q)uit\n'''

while(True):
    print(help)
    try:
        command = input('Command: ').upper().rstrip()
        if command == 'A':
            root.add_feedlink()
        elif command == 'P':
            root.print_feedtitles()
        elif command == 'U':
            root.get_feed()
        elif command == 'G':
            root.print_link()
        elif command == 'R':
            root.print_description()
        elif command == 'Q':
            break
        else:
            print('\nUnknown command\n')
    except SystemExit as e:
        pass
    except KeyboardInterrupt:
        sys.exit()
