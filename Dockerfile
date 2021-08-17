FROM registry.access.redhat.com/ubi8/ubi-minimal:latest
EXPOSE 8081
RUN microdnf update -y && \
  microdnf install -y \
        curl \
        lsof \
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
