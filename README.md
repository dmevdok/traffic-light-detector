# Running

1) Clone the repo:

```

git clone https://github.com/dMeVdok/traffic-light-detector.git
cd traffic-light-detector

```

2) Make sure you have `ffmpeg` installed

### Please use conda environment while working with the project

`conda env create -f environment.yml` to create environment

`conda activate tldetector` to activate environment

Make sure you can use `ffmpeg` inside `tldetector` environment

### Use `make`:

`make downloads` to download data & trained models

`make docker` to build docker image

### Cleanup:

`make clean` to remove data & trained models

# Inference

### In Google Colab

You can easily inference traffic light detection in google colab -- just copy it to your google drive and run `experiments/the_pipeline.ipynb` notebook

### On your PC

Switch to `tldetector` conda environment and run `python test.py PATH_TO_VIDEO`

Don't forget to add ffmpeg's binary folder to your $PATH (eg. when using homebrew)

Please use Mac or Linux, WSL is not tested

### In docker

`make docker` to build docker image `tldetector`

```
docker run -v `pwd`/data:/data -it tldetector PATH_TO_VIDEO`
```

where PATH_TO_VIDEO is relative to ./data folder (eg 'data/phase_I/video_0.mp4')

# Developing

1) choose a task from ToDo https://github.com/dMeVdok/traffic-light-detector/projects/1 and move it to "In progress"

2) create a branch for this task:

```
git checkout -b yournickname/short_task_description
```

`yournickname` is your nickname (one word)

`short_task_description` is a task description in a couple of words -- it's up to you

3) make your changes

4) commit your changes

look for an issue number of your task

```
git add .
git commit -m "close #ISSUENUMBER"
```

(you can do it multiple times, if you've forgotten smth or made a mistake)

5) push your changes

```
git push origin yournickname/short_task_description
```

6) make a pull request from `yournickname/short_task_description` to `master`, **write `closes #ISSUENUMBER` to your pull request description**

wait for approval from the other team member

### Adding a new task

1) add a task to ToDo

2) if it requires code writing, don't forget to convert it to issue
