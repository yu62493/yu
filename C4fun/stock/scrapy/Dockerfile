FROM python:3.7.0
MAINTAINER TinyYu
LABEL description="Test in YUSCO"
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN mkdir /tiny_scrapy
WORKDIR /tiny_scrapy
COPY . /tiny_scrapy/
CMD ["python", "test.py"]
