FROM python:3.9.15
LABEL maintainer="mkorangestripe@gmail.com"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "load_balancer:app"]
