# djangoStazh
Django application about buildings
## Steps to start project:
#### 1) Create and activate virtual environment for Python
    python -m venv .venv
    .venv/Scripts/activate      # windows
    source .venv/bin/activate   # linux
#### 2) Update `pip`
    python -m pip install --upgrade pip # windows
    pip install -U pip                  # linux
#### 2) Install Python requirements
    pip install -r requirements.txt
#### 3) Go to project folder (if you are not in the project folder)
    cd building
#### 4) Create the `.env` file using the `.env_example` file as an example
    cp .env_example .env
    nano .env
#### 5) Create `SECRET_KEY`
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
#### 6) Compile localization files
    python manage.py compilemessages -l <languages>
#### 6) Run tests to check installed project functionality
    python manage.py test
#### 7) Run server
    python manage.py runserver
