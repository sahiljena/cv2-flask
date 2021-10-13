# Cv2 flask
A small project built to learn cv2 integration with Flask, host it on the college network so that it can be accessed anywhere within the college campus.

## What it does
It has a login and logout page(so that only I can access the camera feed), once after login the camera switches on and the video feed is visible with face detection.

## Built With
| Software/ Language | Version |
|----------|---------|
| Python | 3.8 |
| Flask | 2.0.2 |
| opencv-python | 4.5.3.56 |

## How to get started
To use this project, follow these steps:

* Make a `.env` file using the command `virtualenv env`
* Clone this repository 
```
git clone https://github.com/sahiljena/cv2-flask.git
```
* Install dependencies 
```
pip install -r requirements.txt
```
* Run the App  `python app.py` or `flask run`




