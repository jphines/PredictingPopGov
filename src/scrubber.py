# Srubs data by filtering all clicks not from the united states
# Filters data not from a twitter redirect
# Gets total clicks from a bitly global hash using the bitly api
# Downloads the src of a webpage from said link
# Finds all meaningful text (Assumed to be in the title and <p> tags)
# Removes puncation, all superflous white space
# Organizes data based on total number of clicks into 5 categories
# saves into separate tsv files for each with url, location, clicks, and 
# cleaned words from said webpage

import unicodedata
import bitly_api
import lxml.html
import string, re, json, codecs, os, glob, csv 
import sys
import socket
timeout = 7
socket.setdefaulttimeout(timeout)
global_set = set()
c = bitly_api.Connection('justinhines','R_8b65a446e3b9794aa021967762a34a50') 

stop_words = set(line.strip() for line in open('../requirements/stopwords.txt'))
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']
files = ['low','medium','high','popular','insane']
path = '../tsv/'
data_path = '../usagov_data/'

def chunks(l, n):
  return [l[i:i+n] for i in range(0, len(l), n)]

def write_states(d):
  for state in states:
    lists = []
    for hash, v in d[state].iteritems():

      clicks = v['l']
      lists.append([hash,clicks])
    lists = sorted(lists, key = lambda x: x[1])
    d[state]['file'] = {}
    d[state]['writer'] = {}
    for file in files:
      d[state]['file'][file] = open(path+state+'/'+file+'.tsv','w')
      d[state]['writer'][file] = csv.writer(d[state]['file'][file], delimiter='\t')
    chunked = chunks(lists, 5)
    file_count = 0
    for chunk in chunked:
      file = files[file_count]
      for tup in chunk:
        hash = tup[0]
        content = d[state][hash]['c']
        d[state]['writer'][file].writerow([hash, tup[1], state, content])
      d[state]['file'][file].close()
      file_count += 1


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
  out = open('../log/current.log', 'w')
  sys.stdout = out
  d = state_setup()
  count = 1534
  for infile in glob.glob(os.path.join(data_path, 'usagov_bitly_data*')):
    count
    print "current file is: " + infile
    data_file = codecs.open(infile,'r','utf-8')
    for line in data_file:
      try:
        dict = json.loads(line.strip())
        location = dict['gr']
      except:
        continue
      if dict['g'] in global_set:
        continue
      if not dict['gr'] in states:
        continue
      hash = dict['g']
      hash = unicodedata.normalize('NFKD', hash).encode('ascii','ignore')
      location = dict['gr']
      location = unicodedata.normalize('NFKD', location).encode('ascii','ignore') 
      if hash in d[location]:
        d[location][hash]['l'] += 1
        sys.stdout.write("l")
      else:
        if hash in d['global']:
          d[location][hash] = {}
          d[location][hash]['c'] = d['global'][hash]['c']
          d[location][hash]['l'] = 1
          sys.stdout.write("g")
        else:
          content = get_content_as_list(hash)
          if len(content) <= 50:
            global_set.add(hash)
            continue
          content = ' '.join(content[:50])
          d['global'][hash] = {}
          d[location][hash] = {}
          g_clicks = get_clicks(hash)
          d['global'][hash]['l'] = g_clicks
          d['global'][hash]['c'] = content 
          d[location][hash]['l'] = 1
          d[location][hash]['c'] = content
          sys.stdout.write(".")
    count -= 1
    log = open('../log/'+count+'_left.log','w')
    log.close()
      
  write_states(d)


if __name__ == "__main__":
  main()
