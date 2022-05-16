FROM python:3.9 as requirements-stage
#For single Docker file use:
# docker build -t test_fastapi_image . builds the image [dont forget the dot]
# 1079  docker run -d --name fastapi_test_container -p 8000:8000 test_fastapi_image run the Container
#  1102  docker ps -a gets the container and their output
#  1103  docker-compose -f docker-compose.local.yml up -d #Run the container compose


# 
WORKDIR /tmp

# Must be installed on python?
RUN pip3 install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.9

# for the alembic 
WORKDIR /backend

#
COPY . /backend

# 
# WORKDIR /backend/app

# 
COPY --from=requirements-stage /tmp/requirements.txt backend/app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r backend/app/requirements.txt

#
# CMD alembic upgrade head

# WORKDIR /backend/app

# 
# COPY ./app /app

# 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ls,"python3","main.py"]
CMD ["alembic", "upgrade", "head"]


