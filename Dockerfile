FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install \
  -y --no-install-recommends python python-pip python-setuptools python-wheel curl lsof python-cherrypy

# Install dependencies:
COPY requirements.txt .
ADD . /pulpito
RUN pip install -r requirements.txt
RUN pip install /pulpito/.

# Run the application:
COPY config.py.in /pulpito/prod.py
WORKDIR /pulpito
CMD python run.py
