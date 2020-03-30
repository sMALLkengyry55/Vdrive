# Vdrive #

1. [General Information](#general-information)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [How to run and use](#how-to-run-and-use)
5. [Development](#development)
6. [Links to servers](#links)


## General Information ##

[vdrive]() is a REST API for [vdrive].
Vdrive is an app for import videos from google drive and google photos to youtube channel.

## Dependencies ##

Take a look at *requirements.txt* for Python dependencies.

## Installation ##

Go to https://uagit.akvelon.net/python/vdrive and copy ssh for making a clone of the project

Go to cmd, type command that will clone the project and create a new folder, for example "project"
 ```
 $ git clone ssh://git@uagit.akvelon.net:2015/python/vdrive.git project
```
Go to the dir with the project
```
$ cd project
```
Run the docker container with the command
```
$ docker-compose -f docker-compose.yml up
```

## How to run and use ##

1. Open a browser and go to the localhost address http://localhost:8000/ or http://127.0.0.1:8000/
2. Logging via google in your google account.
3. Wait a minute until app scanning your google drive and google photos and reload the page.
4. Choose several videos and press the button Upload, after that you will be redirected to the page with statuses of processings of your videos.
5. On the page “Import list” you will see videos that you have chosen to upload with their current status (the page will be reloaded automatically and statuses will be updated ).
6. go to the channel connected with your Google account and open the Youtube studio tab. You will see your videos in processing by Youtube, after a couple of minutes it will be finished.
7. If you want, you can delete uploaded videos on another page “Delete” in the app( now you can delete only videos from Google Drive ).

## Development ##

If you use Docker Django app will be exposing on 8000 port by default. It's up to you to change settings.

run docker compose:
```sh
$ make docker_dev
```

get docker containers status:
```sh
$ make docker_dev_status
```


run tests in *web* container:
```sh
$ make test
```

Test coverage: 0%

## API ##

For the API description go to:
`api/v1/docs/`

Try API:
`api/v1/swagger/`

Generate OpenAPI schema:
`api/v1/swagger|.json|.yml/`

## Links ##

### Testing server ###

url: *test@example.com*


Generated with [AC's cookiecutter template](https://gl.atomcream.com/boilerplates/templates/django-api-template) version 0.0.1
