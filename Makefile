all: data bayes

data:
	cd src/
	python listing.py
	python organize.py
	python scrubber.py jan1
	python scrubber.py jan2
	python scrubber.py jan3
	python scrubber.py jan4
	python scrubber.py jan5
	python scrubber.py jan6
	python scrubber.py feb1
	python scrubber.py feb2
	python scrubber.py feb3
	python scrubber.py feb4
	python scrubber.py feb5
	python scrubber.py feb6
	python scrubber.py mar1
	python scrubber.py mar2
	python scrubber.py mar3
	python scrubber.py mar4
	python scrubber.py mar5
	python scrubber.py mar6
	python scrubber.py apr1
	python scrubber.py apr2
	python scrubber.py apr3
	python scrubber.py apr4
	python scrubber.py apr5
	python scrubber.py apr6
	python filter.py
	python compress.py
	python delete.py

bayes:
	cd src
	python bayes.py
