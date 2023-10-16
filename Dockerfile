FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code


#RUN pip install -r requirements.txt

COPY . /code/

RUN "cd core"

CMD ["python","server"]
