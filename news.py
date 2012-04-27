import urllib.request
import smtplib
import json
import random

fromaddr = 'Daniel Lubarov <daniel@lubarov.com>'
toaddrs = [
  'Ozzie Gooen <Ozzie_Gooen@hmc.edu>',
  'Rahul Swaminathan <xyxyxz@gmail.com>',
  'Fiona Foo <zooplankton@gmail.com>',
  'Paul Hobbs <ida.noeman@gmail.com>',
  #'Sonja Bohr <sonja314@gmail.com>',
  'Daniel Lubarov <daniel@lubarov.com>'
]

username = 'daniel@lubarov.com'
with open('password.txt', 'r') as f:
  password = f.read().strip()

def get_item():
  response = urllib.request.urlopen('http://api.ihackernews.com/page')
  response = response.read()
  response = str(response, 'utf-8')
  j = json.loads(response)
  return j['items'][random.randint(0, 3)]

def mail(subject, body):
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username, password)
  server.sendmail(fromaddr, toaddrs, body)
  server.quit()

def run():
  item = get_item()
  subject = item['title']
  url = item['url']
  body = "Subject: {0}\nFrom: {1}\nTo: {2}\n\nHey, I thought you might be interested:\n\n{3}\n\nCheers,\nDaniel".format(subject, fromaddr, ', '.join(toaddrs), url)
  mail(subject, body)
  print("All done.")

if __name__ == '__main__':
  run()
