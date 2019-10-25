FROM zong4/py37:v0.4
WORKDIR /Bxework
COPY bxework/ ./bxework
COPY weixinapi/ ./weixinapi
COPY datacollect/ ./datacollect
COPY app.py ./
USER nobody
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]