import os

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']

dirs = ['jan1','jan2','jan3','jan4','jan5','jan6','feb1','feb2','feb3','feb4','feb5','feb6','mar1','mar2','mar3','mar4','mar5','mar6','apr1','apr2','apr3','apr5','apr6']

path = '../tsv/'

def delete():
  for state in states:
    dst = path + state + '/'
    for dir in dirs:
      f = dst+dir+'/out.tsv'
      fs = dst+dir
      if os.path.exists(f):
        os.remove(f)
      if os.path.exists(fs): 
        os.rmdir(fs)

if __name__ == '__main__':
  delete()
