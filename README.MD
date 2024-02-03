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

```flask --app api_tagger.py --debug run```

After everything is installed, you can run the app with:

```pipenv run flask --app api_tagger.py --debug run```

## To run (With docker)

### Build
```docker build --tag python-docker .```

### Run
```docker run -p 5050:5050 --rm python-docker```