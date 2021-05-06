# WebappSecurityResearch

##Deployment
### Build and run as docker container
```
docker build -t app .
docker run --name app -p 5000:5000 app
```

### Build and run with python and flask
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app
export FLASK_ENV=development
flask init-db
flask run
```
