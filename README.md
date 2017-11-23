# profbit
[![Circle CI](https://circleci.com/gh/joshblum/profbit.svg?maxAge=2592000&style=shield)](https://circleci.com/gh/joshblum/profbit)
[![Requirements Status](https://requires.io/github/joshblum/profbit/requirements.svg?branch=master)](https://requires.io/github/joshblum/profbit/requirements/?branch=master)

Track your bitcoin, ethereum, and litecoin gains and losses in one place.

| | |
|:-------------------------:|:-------------------------:|
|<img width="300" alt="profbit preview" src="https://github.com/joshblum/profbit/blob/master/profbit/static/img/carousel-0.png"> | <img width="300" alt="profbit preview" src="https://github.com/joshblum/profbit/blob/master/profbit/static/img/carousel-1.png"> | |
<img width="300" alt="profbit preview" src="https://github.com/joshblum/profbit/blob/master/profbit/static/img/carousel-2.png"> | <img width="300" alt="profbit preview" src="https://github.com/joshblum/profbit/blob/master/profbit/static/img/carousel-3.png"> |

## Development/Self-hosted Server Setup

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


### Requirements
We use [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to
manage requirements. Note that Python 3.6.3 is required to [incorporate a
fix](https://bugs.python.org/issue26721) for using [gevent and werkzeug
together](https://github.com/pallets/werkzeug/issues/920).

```bash
pip install pipenv
pipenv install
pipenv shell
```

### Server Config
You will first have [register an application on
Coinbase](https://coinbase.com/oauth/applications/new). When registering your app
be sure to add the redirect url i.e.
https://app-name.herokuapp.com/complete/coinbase/. Then `export` the following
configuration variables and create the database:

```bash
cd profbit

export SECRET_KEY="super-secret-key"
export SOCIAL_AUTH_COINBASE_KEY="coinbase-key"
export SOCIAL_AUTH_COINBASE_SECRET="coinbase-secret"
export FLASK_APP=app.py
export FLASK_DEBUG=1

flask syncdb
```


## Donate

Profbit is an open source side project. To support development and keep
our server running, you can donate using Bitcoin or Ethereum:

- Bitcoin: `19UsnMKjhm22mFEYKKNHjxdFCfnShTcbPM`
- Ethereum: `0x97A3D535391A5a87f8362935B26f252E68C25Aca`
