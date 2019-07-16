FROM python:3.7.4-alpine

RUN pip install flask requests gunicorn
WORKDIR /Bxework
COPY * /Bxework
ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-b", "0.0.0.0:8800", "bxework:app"]