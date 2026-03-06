# computacional-vision-project-api
source .venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

alembic revision --autogenerate -m ""

alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --reload


# docker

docker build -t api .
docker run -d --env-file .env -p 8000:8000 --name api api

docker stop api
docker rm api
docker logs -f api