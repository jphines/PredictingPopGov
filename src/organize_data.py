import csv
import os

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY']

files = ['low','medium','high','popular','insane']
path = '../tsv/total/'
spath = '../tsv/states/'

global_set = set()

def state_setup(file):
  d = dict() 
  for state in states:
    d[state] = {}
    if not os.path.exists(spath+state):
      os.makedirs(spath+state)
    d[state]  = {}
    d[state]['writer'] = csv.writer(open(spath + state +'/'+ file+ '.tsv', 'w'), delimiter='\t')
    d[state]['hash'] = {}
    d[state]['content'] = {}
  return d

def main():
  for file in files:
    if not os.path.exists(path):
      os.makedirs(path)
    global_reader = csv.DictReader(open('../tsv/'+file+'.tsv'), delimiter='\t')
    global_writer = csv.writer(open(path+file+'.tsv', 'wb'), delimiter ='\t')
    d = state_setup(file)
    try:
      for row in global_reader:
        url = row['URL']
        location = row['Location']
        clicks = row['Clicks']
        content = row['Content']
        hash = url[-6:]
        if d[location]['hash'].has_key(hash):
          d[location]['hash'][hash] += 1
        else:
          d[location]['hash'][hash] = 1 
          d[location]['content'][hash] = content
        if hash in global_set:
          continue
        else:
          global_set.add(hash)   
          global_writer.writerow([url,clicks,content])    
    except:
      continue
    for state in states:
      for k,v in d[state]['hash'].iteritems():
        c = d[state]['content'][k]
        d[state]['writer'].writerow([k,v,c])

if __name__ == "__main__":
  main()
