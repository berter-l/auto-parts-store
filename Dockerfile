FROM python:3.13.12-alpine3.22
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir  -r requirements.txt
