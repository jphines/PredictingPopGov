import os

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']

dirs = ['jan1','jan2','jan3','jan4','jan5','feb1','feb4','feb5','mar1','mar2','mar3','mar4','mar5','apr1','apr5']

path = '../tsv/'

def delete():
  for state in states:
    dst = path + state + '/'
    for dir in  dirs:
      f = dst+dir+'/out.tsv'
      fol = dst+dir
      if os.path.exists(f):
        os.remove(dst+dir+'/out.tsv')
      if os.path.exists(fol):
        os.rmdir(dst+dir)

if __name__ == '__main__':
  delete()
