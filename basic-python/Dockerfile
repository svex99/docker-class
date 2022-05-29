FROM docker.uclv.cu/python:3.9.5

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt \
    --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ \
    --trusted-host nexus.prod.uci.cu

CMD ["python3", "main.py"]