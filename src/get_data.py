# HACKY -- But Downloads all usagov_bitly_data including archieved 
# from measuredvoice server
import urllib
import re

 
data = urllib.urlopen('http://bitly.measuredvoice.com/bitly_archive/?C=M;O=D').read()    

p = re.compile('../usagov_data/usagov_bitly_data\d{4}-\d{2}-\d{2}-\d{10}')

m=p.findall(data)

for i in range(len(m)):
	if (i%2==0):
		print m[i]
		
print len(m)

for i in range(len(m)):
	if (i%2==0):
		print "downloading ",  m[i]
		clicks = urllib.urlopen('http://bitly.measuredvoice.com/bitly_archive/'+m[i]).read()
		file = open(m[i], "w")
		file.write(clicks)
		file.close()
		print "done"
		
