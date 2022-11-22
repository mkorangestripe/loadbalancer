# Load Balancer

This simulates a load balancer that distributes requests between multiple virtual machines.

To start this application directly with **Flask**:

```
export FLASK_APP=load_balancer.py
flask run
```

To start this application directly with **Gunicorn**:
```
gunicorn -b 0.0.0.0:80 load_balancer:app
```

To start this application with **Docker**, any of the following:

```shell script
docker-compose up -d
docker run -d --name cat_loadbalancer --network host mkorangestripe/loadbalancer:latest  # Linux
docker run -d --name cat_loadbalancer -p 80:80 mkorangestripe/loadbalancer:latest  # macOS
```

To get the content from the fake VMs, use curl or a browser.  Run the curl command or reload the page multiple times to see unique content from each VM.

```shell script
curl 127.0.0.1:5000  # Flask
curl 127.0.0.1  # Gunicorn, Docker
```

For deployments to **AWS ECS** with terraform, see the [terraform](terraform) directory.
