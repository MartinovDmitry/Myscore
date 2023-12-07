FROM python:3.11

WORKDIR /myscore

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /myscore/docker/*.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]