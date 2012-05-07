# Srubs data by filtering all clicks not from the united states
# Filters data not from a twitter redirect
# Gets total clicks from a bitly global hash using the bitly api
# Downloads the src of a webpage from said link
# Finds all meaningful text (Assumed to be in the title and <p> tags)
# Removes puncation, all superflous white space
# Organizes data based on total number of clicks into 5 categories
# saves into separate tsv files for each with url, location, clicks, and 
# cleaned words from said webpage

import bitly_api
import lxml.html
import string, re, json, codecs, os, glob, csv 
import sys
import unicodedata
import socket
timeout = 10
socket.setdefaulttimeout(timeout)

c = bitly_api.Connection('o_2epmte81bk','R_2fd504831c77c1ecf9518e6bcbcbb92a')

stop_words = set(line.strip() for line in open('../requirements/stopwords.txt'))
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']
files = ['low','medium','high','popular','insane']
path = '../tsv/'
data_path = '../usagov_data/'


def write_states(d):
  for state in states:
    lists = []
    for k in d[state]:
      print k
      clicks = d[state][k]['clicks']
      lists.append([k,clicks])
    lists = sorted(lists, key = lambda x: x[1])
    length = len(lists)/5
    x, i, n, p = 1, 0, 0, 0
    file = files[0]
    d[state]['file'] = {}
    d[state]['writer'] = {}
    for file in files:
      d[state]['file'][file] = open(path+state+'/'+file+'.tsv','w')
      d[state]['writer'][file] = csv.writer(d[state]['file'][file], delimiter='\t')
    while x < (len(lists) - length):
      k = lists[n][0]
      print k
      if not d[state].has_key(k):
        continue
      clicks = d[state][k]['clicks']
      content = d[state][k]['content']
      d[state]['writer'][file].writerow([k,state,clicks,content])
      if p == length:
        x +=  length 
        i += 1
        file = files[i]
        d[state]['file'][file].close()
        p = 0
      else:
        p += 1
      n += 1


def clean_string(str):
  str = str.translate(string.maketrans("",""), string.punctuation) 
  re.sub('\d',"",str)
  str = filter_stop(str)
  return ' '.join(str.split())


def deunicode(str):
  return unicodedata.normalize('NFKD', str).encode('ascii','ignore')


def body_to_string(para):
  para = [p.text_content() for p in para]
  para = [clean_string(p) for p in para]
  para = [p.split() for p in para]
  para = [item for sublist in para for item in sublist]
  return ' '.join(para)


def filter_stop(l):
  s = set(l.lower().split())
  s -= stop_words
  return ' '.join(s)


def get_clicks(hash):
  return c.clicks(hash=hash)[0]['global_clicks']


def get_content_as_list(hash):
  url = "http://www.bit.ly/" + hash
  try:
    soup = lxml.html.parse(url)
    title = clean_string(soup.find(".//title").text)
    body = body_to_string(soup.xpath('//p')) 
    sys.stdout.write("D")
    return (title+" "+body).split() 
  except:
    return ["Error"]

def state_setup():
  d = dict() 
  for state in states:
    d[state] = {}
    if not os.path.exists(path+state):
      os.makedirs(path+state)
  return d


def main():
  #out = open('../log/current.log', 'w')
  #sys.stdout = out
  d = state_setup()
  for infile in glob.glob(os.path.join(data_path, 'usagov_bitly_data*')):
    print "current file is: " + infile
    data_file = codecs.open(infile,'r','utf-8')
    for line in data_file:
      try:
        dict = json.loads(line.strip())
        location = dict['gr']
        if not location in states:
          continue
        hash = dict['g'] 
        location = dict['gr']
        if hash in d[location]:
          print "x"
          d[location][hash]['clicks'] += 1
        else:
          if hash in d['global']:
            d[location][hash]['content'] = d['global'][hash]['content']
            d[location][hash]['clicks'] = 1
          else:
            content = get_content_as_list(hash)
            if content <= 50: 
              sys.stdout.write("-")
              continue
            content = ' '.join(content[:20])
            g_clicks = get_clicks(hash)
            d['global'][hash]['clicks'] = g_clicks
            d['global'][hash]['content'] = content 
            d[location][hash]['clicks'] = 1
            d[location][hash]['content'] = content
            sys.stdout.write(".")
      except: 
        continue
  write_states(d)


if __name__ == "__main__":
  main()
