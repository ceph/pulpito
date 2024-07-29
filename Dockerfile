FROM python:3.7-alpine
EXPOSE 8081
RUN apk add \
        curl \
        gcc \
        musl-dev \
        lsof && pip install -U pip

# Install dependencies:
COPY requirements.txt .
ADD . /pulpito
RUN pip3 install -r requirements.txt
RUN pip3 install /pulpito/.

# Run the application:
COPY config.py.in /pulpito/prod.py
WORKDIR /pulpito
CMD python3 run.py
