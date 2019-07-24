FROM python:3.7.4-alpine

RUN pip install flask requests gunicorn pycryptodome
WORKDIR /Bxework
COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]