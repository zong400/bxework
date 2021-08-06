FROM python:3.7.11-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone
ENV TZ Asia/Shanghai

WORKDIR /Bxework
COPY requirements.txt requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY datacollect/ ./datacollect
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]