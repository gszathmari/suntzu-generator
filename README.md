# suntzu-generator

suntzu-generator is a bogus The Art of War quote generator API.

Run out of quotes from Sun Tzu? Spin this application up in Heroku and start serving fake quotes in JSON format.

## Install

* [Deploy application into Heroku](https://devcenter.heroku.com/articles/python-gunicorn) as it is

## Usage

Get a random bogus quote
```bash
$ curl https://<application>.herokuapp.com/v1/getquote
```

Get quote for Twitter (max. 140 characters)
```bash
$ curl https://<application>.herokuapp.com/v1/gettweet
```

Healthcheck URI for Uptime Robot, Pingdom etc.
```bash
$ curl https://<application>.herokuapp.com/v1/healthcheck
```
