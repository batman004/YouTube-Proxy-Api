FROM python:3.8.9

WORKDIR /codebase

COPY ./requirements.txt /codebase/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /codebase/requirements.txt

COPY . /codebase

ENV PYTHONPATH="$PATH:/codebase"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
