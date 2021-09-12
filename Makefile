.PHONY: create build

create:
	cd ../FIT2082 && make build >> ../FIT2082MAPF/FIT2082VisualizerNew/test_50.txt

build:  
	cd FIT2082VisualizerNew && python run.py test_50.txt warehouse-10-20-10-2-1.map.ecbs
