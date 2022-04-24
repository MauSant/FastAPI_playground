FROM python:3.9 as requirements-stage

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


