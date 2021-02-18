all: data train test docker

.PHONY : all

data::
	bash utils/download_data.sh

train::
	echo "No train script yet :("

test::
	echo "No test script yet :("

docker::
	docker build . -t traffic-light-detector

clean-data:
	rm -rf data
	mkdir data
	touch data/.gitignore

clean-logs:
	rm -rf logs
	mkdir logs
	touch logs/.gitignore

clean-models:
	rm -rf models
	mkdir models
	touch models/.gitignore

clean-pretrained:
	rm -rf pretrained
	mkdir pretrained
	touch pretrained/.gitignore