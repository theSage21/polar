```bash
pipenv install --deploy
pipenv run db.py positions.csv
pipenv run server.py &
pipenv run pytest test_api.py
```
