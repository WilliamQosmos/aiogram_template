# Simple Aiogram 3.x template

## How to run

Required launched PostgreSQL and installed Python3.10

* copy config template
```bash
cp -r config_dist config
```
* Fill config/config.yml in with required values 
* Create and activate venv
```bash
python -m venv venv
source venv/bin/activate
```
* install dependencies
```bash
pip install -r requirements.txt
```
* Fill in alembic.ini (probably only db url)
* apply migrations
```bash
alembic upgrade head
```
* ... and run
```bash
python -m app
```
