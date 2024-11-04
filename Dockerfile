FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN export $(cat ./.env | xargs)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["python", "start.py"]