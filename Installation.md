## Installation and Configuration
1. Clone the repository
```terminal
git clone https://github.com/21Gxme/ku-polls.git
```
2. Change directory to `ku-polls`
```terminal
cd ku-polls
```

3. Create virtual environment
```terminal
python -m venv venv
```

4. Activate virtual environment

```terminal
On MacOS or Linux:
. venv/bin/activate
```
```terminal
On Windows:
.venv\Scripts\activate
```

5. Install required packages
```terminal
pip install -r requirements.txt
```

6. Create a file named `.env` in the same directory as `manage.py`:
```terminal
On Linux/MacOS:
cp sample.env .env
```
```terminal
On Windows:
copy sample.env .env
```

7. Run database migration
```terminal
python manage.py migrate
```

8. Load initial data
```terminal
python manage.py loaddata data/polls-no-vote.json 
python manage.py loaddata data/users.json
```

9. Run test
```terminal
python manage.py test polls
```

10. Run server
```terminal
python manage.py runserver
```
