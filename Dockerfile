# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /pokeapi
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
# CMD [ "python", "./pokeapi/aiohttp_pokeapi/main.py"]
