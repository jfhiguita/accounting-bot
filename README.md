# Build & Deploy a Telegram's ChatBot To write in Gsheets.
I'm using Flask, Google Cloud Run, the Telegram API & Google Sheets API for this. The bot can be hosted for free.

Watch how this bot works: 



## Quickstart:
### Create virtual env
```console
python3 -m venv venv
Activate (on Mac):
. venv/bin/activate
```

## Set up environment variables
look at this [article](https://dev.to/jfhiguita/manage-environment-variables-with-decouple-in-python-h20)

## Heroku start
```console
heroku login -i
heroku create your_app_name
```

add config vars:
```console
heroku config:set CONSUMER_KEY=xxx
heroku config:set CONSUMER_SECRET=xxx
heroku config:set ACCESS_TOKEN=xxx
heroku config:set ACCESS_SECRET=xxx
heroku config:set INTERVAL=1200
heroku config:set DEBUG=0
```

Scale worker:
```console
heroku ps:scale worker=1
```

Test locally:
```console
heroku local
```

Push to Heroku:
```console
git init
heroku git:remote -a your_app_name
git add .
git commit -m "initial commit"
git push heroku master
```

and later your secret.json:
```console
git checkout -b secret-branch
  --> remove secret.json from *.gitignore* on new branch
git add .
git commit -m "add credentials"
git push heroku secret-branch:master
```
