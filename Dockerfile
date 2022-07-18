FROM python:3.8.9

WORKDIR /codebase

COPY ./requirements.txt /codebase/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /codebase/requirements.txt

COPY ./app /codebase/app

CMD ["python", "main.py"]
