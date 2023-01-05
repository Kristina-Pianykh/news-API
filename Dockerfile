FROM ubuntu:22.04

# install system-wide deps for python and poetry
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg

RUN curl -sL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"
RUN echo "poetry --version"

RUN mkdir app
WORKDIR /app

COPY . .

# fetch app specific deps
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt


# expose port
EXPOSE 80

WORKDIR /app/news_api

# start app
CMD python3 -m uvicorn api:app --reload