[![Django CI](https://github.com/21Gxme/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/21Gxme/ku-polls/actions/workflows/django.yml)
## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Requirements

- Python 3.9+ and packages listed in [requirements.txt](requirements.txt)
## Install and Configure

Check from [Install and Configure](Installation.md)

## How to Run

#### On MacOS or Linux:

1. Activate virtual environment
```terminal
. venv/bin/activate
```

2. Start the Django development server
```terminal
python manage.py runserver
```
3. Open the web browser and go to http://localhost:8000

4. To stop the server, press `Ctrl + C`

5. To deactivate virtual environment
```terminal
deactivate
```

#### On Windows:

1. Activate virtual environment
```terminal
.venv\Scripts\activate.bat
```

2. Start the Django development server
```terminal
python manage.py runserver
```

3. Open the web browser and go to http://localhost:8000
4. To stop the server, press `Ctrl + C`
5. To deactivate virtual environment
```terminal
deactivate
```

## Demo Admin Account
| Username | Password |
|----------|----------|
| admin    | 1234     |

## Demo User Account
| Username | Password |
|----------|----------|
| bob      | bob1234  |
| Game     | Game1234 |

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)
- [Domain Model]((../../wiki/Domain-model))
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Iteration 3 Plan](../../wiki/Iteration-3-Plan)
- [Iteration 4 Plan](../../wiki/Iteration-4-Plan)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/
