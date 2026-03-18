```shell
pip 代理设置

# 开发
python -m venv .venv
pip install -r  requirements.txt
pip install gunicorn


pdm add
# 防止run --debug 报错
pdm add watchdog


# 启动
flask --app app.py run --debug
flask --app app.py run --debug

# 发布
pip freeze > requirements.txt

python.exe -m pip install --upgrade pip
pip install -r  requirements.txt
docker build -t test:v3  .
docker rm -f flask-demo 
docker run -itd --name flask-demo -p 5000:80  test:v3
docker logs  -f flask-demo
```