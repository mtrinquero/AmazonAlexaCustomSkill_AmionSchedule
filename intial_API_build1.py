# Mark Trinquero
# Amion Schedule - Get Data
# Note: written in pyton 3


# http://www.amion.com/cgi-bin/ocs?Lo=nwem&Rpt=619


# "http://www.amion.com/cgi-bin/ocs?Lo=#{password}&Rpt=619&Month=#{month}&Year=#{year}")
# {password}
# {month}
# {year}


import csv
import urllib.request
import codecs


def skip_first(seq, n):
    for i,item in enumerate(seq):
        if i >= n:
            yield item

name = "Paul Trinquero"
url = "http://www.amion.com/cgi-bin/ocs?Lo=nwem&Rpt=619"

ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))

schedule_attributes = next(csvfile)
print (schedule_attributes)


for line in skip_first(csvfile, 6):
	if line[0] == name:
		print(line)
	else:
		print("Not working today")

