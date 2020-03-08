FROM python:3
WORKDIR /usr/shengji/py
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./
CMD ["python", "main.py", "--store_path=/var/www/rw"] 