import json
import bitly_api
import codecs
import os
import glob
import string
import csv
c = bitly_api.Connection('o_2epmte81bk','R_2fd504831c77c1ecf9518e6bcbcbb92a')

import lxml.html
 
stop_words = set(line.strip() for line in open('stopwords.txt'))
STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NV', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
def remove_white_punc(str):
  #exclude = set(string.punctuation)
  #str = ''.join(ch for ch in str if ch not in exclude)
  str = str.translate(string.maketrans("",""), string.punctuation)
  return ' '.join(str.split())


def fix_paragraphs(para):
  para = [p.text_content() for p in para]
  para = [remove_white_punc(p) for p in para]
  para = [p.split() for p in para]
  para = [item for sublist in para for item in sublist]
  return para


def filter_stop(l):
  text = ' '.join(l)
  text = set(text.lower().split())
  text -= stop_words
  return list(text)

def op_line(line, low, medium, high, popular, insane):
  dict = json.loads(line.strip())
  location =  dict['gr']
  if location in STATES:
    hash = dict['g'] 
    url = "http://www.bit.ly/" + hash
    clicks = c.clicks(hash=hash)[0]['global_clicks']
    soup = lxml.html.parse(url)
    title =  soup.find(".//title").text
    title = remove_white_punc(title).split()
    para = soup.xpath('//p')
    para = fix_paragraphs(para)
    content = title + para
    content = filter_stop(content)
    print content
    if len(content) > 6:
      if 100 > clicks:
        low.writerow([url,location,clicks,' '.join(content)])
      else:
        if 1000 > clicks and 100 < clicks:
          medium.writerow([url,location,clicks,' '.join(content)])
        else:
          if 10000 > clicks and 1000 < clicks:
            high.writerow([url,location,clicks,' '.join(content)])
          else:
            if 50000 > clicks and 25000 < clicks:
              popular.writerow([url,location,clicks,' '.join(content)])
            else:
              if clicks > 50000:
                insane.writerow([url,location,clicks,' '.join(content)])

def main():
  path = 'usagov_data/'
  low = csv.writer(open('../low' + '.tsv', 'wb'), delimiter='\t')
  medium = csv.writer(open('../medium' + '.tsv', 'wb'), delimiter='\t')
  high = csv.writer(open('../high' + '.tsv', 'wb'), delimiter='\t')
  popular = csv.writer(open('../popular' + '.tsv', 'wb'), delimiter='\t')
  insane = csv.writer(open('../insane' + '.tsv', 'wb'), delimiter='\t')
  low.writerow(['URL','Location','Clicks','Content'])
  medium.writerow(['URL','Location','Clicks','Content'])
  high.writerow(['URL','Location','Clicks','Content'])
  popular.writerow(['URL','Location','Clicks','Content'])
  insane.writerow(['URL','Location','Clicks','Content'])
  for infile in glob.glob(os.path.join(path, 'usagov_bitly_data*')):
    print "current file is: " + infile
    file = codecs.open(infile,'r','utf-8')
    for line in file:
      try:
        op_line(line, low, medium, high, popular, insane)
      except:
        continue

if __name__ == "__main__":
  main()
#soup = BeautifulSoup(doc)
# text = soup.get_test()
## f = c.clicks(hash='HASH')
# NUM = f[0]['global_clicks']
