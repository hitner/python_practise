FROM python:3

WORKDIR /usr/src/long_poll

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py ./
COPY ../server_common/http_base_handler.py ./

CMD [ "python3", "main.py" ]