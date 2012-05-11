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
import lxml.html
import string, re, json, codecs, os, glob, csv 
import sys
import socket
import ctypes
timeout = 7
socket.setdefaulttimeout(timeout)

stop_words = set(line.strip() for line in open('../requirements/stopwords.txt'))
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']

path = '../tsv/' 
data_path = '../usagov_data_monthly/' + sys.argv[1] + '/' 
test_set = '/'+sys.argv[1]
global_set = set()

def write_states(d):
  for state in states:
    file = open(path+state+test_set+'/out.tsv', 'w')
    state_writer = csv.writer(file, delimiter = '\t')
    for hash, value in d[state].iteritems():
      clicks = value['l']
      content = d[state][hash]['c']
      state_writer.writerow( [hash, clicks, state, content] )
    file.close()


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
    if not os.path.exists(path+state+test_set):
      os.makedirs(path+state+test_set)
  return d


def main():
  d = state_setup()
  for infile in glob.glob(os.path.join(data_path, 'usagov_bitly_data*')):
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
      hash = deunicode(dict['g'])
      location = deunicode(dict['gr'])
      if hash in d[location]:
        d[location][hash]['l'] += 1
        d['global'][hash]['l'] += 1
      else:
        if hash in d['global']:
          d[location][hash] = {}
          d[location][hash]['c'] = d['global'][hash]['c']
          d[location][hash]['l'] = 1
          d['global'][hash]['l'] += 1
        else:
          content = get_content_as_list(hash)
          if len(content) <= 50:
            global_set.add(hash)
            continue
          content = ' '.join(content[:50])
          d['global'][hash] = {}
          d[location][hash] = {}
          d['global'][hash]['l'] = 1
          d['global'][hash]['c'] = content 
          d[location][hash]['l'] = 1
          d[location][hash]['c'] = content 
  write_states(d)


if __name__ == "__main__":
  main()
  print "Finished"
