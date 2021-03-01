FROM python:3.9.2
ENV FLASK_APP=load_balancer.py
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "flask", "run" ]