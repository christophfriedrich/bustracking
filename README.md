# Bustracking
This is a tool to track buses and their delays in Würzburg. Have a look at: https://bustracking.chrfrd.uber.space/

## Data Source
This is achieved by accesing the public API at https://whitelabel.bahnland-bayern.de/efa/, for which I stumbled across [some documentation](https://www.vrn.de/opendata/sites/default/files/2023-11/EFA_JSON_API_Training_EN_2.1.pdf).

## Architecture
The system consists of:
- a Python crawler that runs every minute, queries the API and stores information into a MySQL database: `crawler.py`
- a Python web server that gets aggregated data from the MySQL database and pipes it out as an API: `server.py`
- a HTML/CSS/JavaScript/Vue.js frontend that consumes that API and visualises the data: `index.html`

## Setup
The thing is deployed on my [Uberspace](https://uberspace.de/) account. Setup included:

Installing Python dependencies:
```
pip3.7 install mysql-connector-python --user   # for crawler
pip3.7 install flask --user                    # for frontend
pip3.7 install flask_mysqldb --user            # for frontend
```

Scheduling the crawler: `crontab -e` and put:
```
* * * * * python3.7 /home/chrfrd/srv/bustracking/crawler.py >> /home/chrfrd/logs/crawler.log
```

Setting up the subdomain and port forwarding:
```
uberspace web domain add bustracking.chrfrd.uber.space
uberspace web backend set bustracking.chrfrd.uber.space --http --port 5000
```

Running the webserver as a service:

1. Create the ini file `/home/chrfrd/etc/services.d/bustracking-frontend.ini` and give it the following content:

```
[program:bustracking-frontend]
command=python3.7 /home/chrfrd/srv/bustracking/server.py
startsecs=60
```

2. Then execute `supervisorctl reread` and `supervisorctl update`.
3. Bam, it's running already! Check with `supervisorctl status`.
4. If needed, use `supervisorctl <command> bustracking-frontend`, where `<command>` can be one of `start`, `stop`, `restart`. Check the [corresponding Uberspace manual section](https://manual.uberspace.de/daemons-supervisord/) for more info, including deleting the service.

Voilà!

## Contact
Christoph Friedrich <christoph ät friedrich minus whv dot de> http://cfriedrich.de/
