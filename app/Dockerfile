FROM python:3.8.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

ENV PYTHONPATH="$PATH:/code"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
