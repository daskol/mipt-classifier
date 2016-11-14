# mipt-classifier

*Classify MIPT students*

## Instalation and Usage

Get source code with commands
```bash
    git clone https://github.com/daskol/mipt-classifier.git
    pip install -r mipt-classifier/requirements.txt
```

First of all change work directory and make new directory for models
```bash
    cd mipt-classifier
    mkdir -p var/models
```
Then one should create database scheme
```bash
    alembic upgrade head
```
In order to open admin panel in browser run
```bash
    gunicorn --access-logfile - --error-logfile - -t 600 -b 0.0.0.0:80 miptclass.wsgi:app
```
Mine user profiles, form dataset and fit model.
```bash
    flask mine
    python miptclass/dataset.py
    python miptclass/baseline
```
