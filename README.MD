## Goal
- The purpose of the app is to receive a tender ID of the DNCP, and return the complaint posibility on it.

## How it works
It works like this:

- Receives the id
- Calls DNCP API
- Parses the data
- Transform the data to Pandas Dataframe
- Calls the model
- Returns the result

## Dependencies
- It's a Python Flask app.
- This project uses pipenv as a virtual environment and to manage the required dependencies.


## To run (Without docker)

```pipenv install```

```pipenv shell```

```flask --app scorer.py --debug run```

After everything is installed, you can run the app with:

```pipenv run flask --app scorer.py --debug run```

## To run (With docker)

## DOCKER PRODUCTION COMMANDS
```docker build . -t prod_flask```
```docker run -p 80:80 --name prod_flask_cont prod_flask```
<!-- ```docker build . -t flask_waitress_img``` -->
<!-- ```docker run --name flask_prod_container -p 80:80 flask_waitress_img``` -->
	
## AWS ECR DEPLOYMENT
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 339712859235.dkr.ecr.sa-east-1.amazonaws.com
docker tag prod_flask 339712859235.dkr.ecr.sa-east-1.amazonaws.com/complaint-scorer
docker push 339712859235.dkr.ecr.sa-east-1.amazonaws.com/complaint-scorer:latest


ECR TAG NAME on AWS: 339712859235.dkr.ecr.sa-east-1.amazonaws.com/complaint-scorer:latest