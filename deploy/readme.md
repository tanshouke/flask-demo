```shell
# 开发
python -m venv .venv
pip install -r  requirements.txt

# 启动
flask --app start.py run --debug
flask --app app.py run --debug

# 发布
pip freeze > requirements.txt
docker build -t test:v3  .
docker rm -f flask-demo 
docker run -itd --name flask-demo -p 5000:80  test:v3
docker logs  -f flask-demo
```