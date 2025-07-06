FROM python:3.12

WORKDIR /root
COPY . .

RUN cd .github && pip install -r requirements.txt
CMD python3 main.py http