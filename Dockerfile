FROM python:3.7.11-alpine

RUN apk --no-cache add gcc libc-dev py3-gunicorn py3-gevent
RUN pip install flask requests pycryptodome redis kubernetes kafka-python
RUN apk add --no-cache tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
ENV TZ Asia/Shanghai
WORKDIR /Bxework
COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY datacollect/ ./datacollect
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]