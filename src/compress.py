import tarfile

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NC', 'NE', 'NH', 'NV', 'NJ', 'NM', 'NY', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY', 'global']

dirs = ['jan1','jan2','jan3','jan4','jan5','jan6','feb1','feb2','feb3','feb4','feb5','feb6','mar1','mar2','mar3','mar4','mar5','mar6','apr1','apr2','apr3','apr5','apr6']

path = '../tsv/'

def compress():
  for state in states:
    print "Compressing " + state
    dst = path + state + '/'
    tar = tarfile.open(dst + "monthly_tsvs.tgz", "w:gz")
    for dir in  dirs:
      tar.add(dst + dir + '/')
  tar.close()

if __name__ == '__main__':
  compress()
