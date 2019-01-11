FROM python:3.6-alpine

ENV FLASK_APP myBlog.py
ENV FLASK_CONFIG docker

RUN adduser -D myBlog
user myBlog

WORKDIR /home/myBlog

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY myBlog.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]