FROM alpine:3.10
RUN apk add --no-cache python3 py3-pip py3-gunicorn py3-gevent py3-pycryptodome py3-flask py3-requests py3-redis
RUN pip install kubernetes kafka-python
RUN apk add --no-cache tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
ENV TZ Asia/Shanghai

COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY datacollect/ ./datacollect
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]