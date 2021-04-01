all: data train test docker

.PHONY : all

downloads::
	bash utils/download_data.sh
	bash utils/download_pretrained.sh

docker::
	docker build . -t tldetector

clean:
	rm -rf data
	mkdir data
	rm -rf pretrained
	mkdir pretrained
	touch data/.gitignore
	touch pretrained/.gitignore