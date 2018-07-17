from requests import *
import re
from json import loads
from argparse import ArgumentParser as DAK
from bs4 import BeautifulSoup

parser = DAK()
parser.add_argument('-a','--action',help = 'Action (chal / submit)')
parser.add_argument('--id',default = '',help = 'Chall ID')
parser.add_argument('-f','--flag',default = '',help = 'Your Flag')
args = parser.parse_args()

#config
name = 'your_team'
passwd = 'your_password'

#made session and declaration url
s = Session()
url = 'https://ctf.url/'

#made connection to get token
a = s.get(url+'login')
sc = a.text
nonce = re.findall(r'<input type="hidden" name="nonce" value="(.+)">',sc,re.I | re.M)[0]

#send login
s.post(url+'login',data = {'name' : name, 'password' : passwd, 'nonce' : nonce}, cookies = a.cookies, allow_redirects = False)

if (args.action == 'chal'):
    chal = s.get(url+'chals').text
    chal = loads(chal)
    print '[+] Getting Chall Name'
    for data in chal['game']:
        #data = loads(data)
        print ' [+] ID : {0} \n [+] Category : {1} \n [+] Chall Name : {2} \n'.format(data['id'],data['category'],data['name'])
elif (args.action == 'submit'):
    if (args.id != '' and args.flag != ''):
        #getting new nonce
        scc = s.get(url+'challenges').text
        nonce =  re.findall(r'<input id="nonce" type="hidden" name="nonce" value="(.+)">',scc,re.I | re.M)[0]
        pd = {'key' : args.flag, 'nonce' : nonce}
        try:
            submit = s.post(url+'chal/'+str(int(args.id)),data = pd).text
            result = loads(submit)['message']
            print "[+] " + result
        except:
            print '[!] 404 Not Found !!!'
    else:
        print '[!] ID / Flag still empty'
elif (args.action == 'scoreboard'):
    score = s.get(url+'scoreboard').text
    bs = BeautifulSoup(score,'html.parser')
    for tr in bs.findAll("tr"):
        try:
            rank = re.findall(r'>(.+)</th>',str(tr.findAll('th')),re.I | re.M)[0]
            team = re.findall(r'>(.+)</a>',str(tr.findAll('a')), re.I | re.M)[0]
            if (name.lower() == team.lower()):
                team += ' (You)'
            point = re.findall(r'>(.+)</td>',str(tr.findAll('td')[1]), re.I | re.M)[0]
            print '['+rank+']', team, '=>', point
        except:
            continue

else:
    print 'Use -h to show help menu !!!'
