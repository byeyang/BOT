#基于的基础镜像
FROM python:3.12

# 设置代码文件夹工作目录 /backend
WORKDIR /backendfile

# 复制当前代码文件到容器中 /backend
ADD . /backendfile

# 安装支持
RUN pip install -r requirements.txt

#CMD ["python", "tg_bot.py,tg_bot_Tow.py,web.py"]
CMD ["python", "tg_bot.py"]