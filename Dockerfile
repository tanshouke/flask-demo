FROM jxe-acr-registry.cn-shenzhen.cr.aliyuncs.com/ops/v2-base/python:3.9.10
WORKDIR /Project/demo

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]