# CS411 Software Engineering Spring 2019

Team 6 Section A3 Repo

Jennie Nguyen         jennien@bu.edu

Vivian Gunawan        vgunawan@bu.edu

Li Sheng Ko      kls0606@bu.edu

Jing Xiao             xjing@bu.edu

Yahui Chang    mollyhui@bu.edu


# Food Friends

Food Friends is a web app designed to connect friends together with dining and activities.

## Installation
First, download the FINAL_VERSION folder of the app to your desktop. Next, you want to be in the app folder.


Create a virtual environment in python. I named my virtual environment "environment"

```bash
python3 -m venv environment
```

Activate virtual environment

```bash
source environment/bin/activate
```

Install necessary packages in the environment

```bash
(environment) $ pip install flask
(environment) $ pip install flask-wtf
(environment) $ pip install flask-sqlalchemy
(environment) $ pip install flask-migrate
(environment) $ pip install flask-login
(environment) $ pip install requests_oauthlib
(environment) $ pip install facebook-sdk
```

Initiate the app

```bash
(environment) $ export FLASK_APP=foodfriends.py
```

Working the database

```bash
(environment) $ flask db init
```

Generate migration script

```bash
(environment) $ flask db migrate -m "users table"
(environment) $ flask db migrate -m "meals table"
```
Apply changes to database

```bash
(environment) $ flask db upgrade
```
Now you are ready to run!

```bash
(environment) $ flask run
```
You should be able to open the app at 

```bash
http://127.0.0.1:5000/ 
```
## Usage

You can make a profile manually or using Facebook. Now you are able to search for a location and then invite someone on your friends list to join you at that location. They will get a notification that you invited them.

## License
[MIT](https://choosealicense.com/licenses/mit/)
