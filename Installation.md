## Installation and Configuration
1. Clone the repository
```terminal
git clone https://github.com/21Gxme/ku-polls.git
```

2. Create virtual environment
```terminal
python -m venv venv
```

3. Activate virtual environment

```terminal
On MacOS or Linux:
. venv/bin/activate
```
```terminal
On Windows:
.venv\Scripts\activate
```

4. Install required packages
```terminal
pip install -r requirements.txt
```

5. Create a file named `.env` in the same directory as `manage.py`:
```terminal
On Linux/MacOS:
cp sample.env .env
```
```terminal
On Windows:
copy sample.env .env
```

6. Run database migration
```terminal
python manage.py migrate
```

7. Load initial data
```terminal
python manage.py loaddata data/polls.json 
python manage.py loaddata data/users.json
```

8. Run test
```terminal
python manage.py test polls
```

9. Run server
```terminal
python manage.py runserver
```
