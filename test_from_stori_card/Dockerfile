FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY ./test_from_stori_card/ /app/test_from_stori_card/
COPY docker-compose.yml /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y libpq-dev
RUN pip install pydevd # for pycharm debugger

CMD ["/app/entrypoint.sh"]
