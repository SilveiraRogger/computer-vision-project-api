# computacional-vision-project-api
source .venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

alembic revision --autogenerate -m ""

alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --reload

# computer-vision-project-api
