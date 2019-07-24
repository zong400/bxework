FROM zong4/py37:v0.2
WORKDIR /Bxework
COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]