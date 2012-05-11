
import sys
import os
import csv
import math
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']

files = ['jan1','jan2','jan3','jan4','jan5','feb1','feb4','feb5','mar1','mar2','mar3','mar4','mar5','apr1','apr5']

path = '../tsv/' 

fifths = ['low','medium','high','popular','insane']


def chunks(l, n):
  n = int(math.ceil(len(l)/5.0))
  return [l[i:i+n] for i in range(0, len(l), n)]


def write_state(d, state):
  print "Writing " + state
  lists = []
  for hash, v in d.iteritems():
    clicks = v['c']
    lists.append([hash,clicks])
  lists = sorted(lists, key = lambda x: x[1])
  lists = chunks(lists,5)
  count = 0
  dir = path + state + '/tsvs/'
  if not os.path.exists(dir):
    os.makedirs(dir)
  for list in lists:
    f = open(dir + fifths[count] + '.tsv', 'w')
    count += 1
    state_writer = csv.writer(f, delimiter = '\t')
    for l in list:
      clicks = l[1]
      hash = l[0]
      print clicks
      content = d[hash]['a']
      state_writer.writerow([hash, clicks, state, content])
    f.close()


def main():
  for state in states:
    d = dict()
    print "Working on " + state
    for file in files:
      f = open(path + state + '/' + file + '/out.tsv', 'rb')
      reader = csv.reader(f, delimiter = '\t')
      for hash, clicks, state, content in reader:
        if hash in d:
          d[hash]['c'] += int(clicks)
        else:
          d[hash] = {}
          d[hash]['a'] = content
          d[hash]['c'] = 1 
      f.close()
    write_state(d, state)


if __name__ == "__main__":
  main()
  print "Finished"
