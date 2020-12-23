FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install \
  -y --no-install-recommends \
        curl \
        lsof \
        python-cherrypy \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel

# Install dependencies:
COPY requirements.txt .
ADD . /pulpito
RUN pip3 install -r requirements.txt
RUN pip3 install /pulpito/.

# Run the application:
COPY config.py.in /pulpito/prod.py
WORKDIR /pulpito
CMD python3 run.py
