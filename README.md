# Load Balancer

This simulates a load balancer that distributes requests between multiple virtual machines.

To start this application directly with Flask:

```shell script
export FLASK_APP=load_balancer.py
flask run
```

To start this application with Docker:

```shell script
docker run --rm -it --network host -p 5000:5000 mkorangestripe/loadbalancer:1.0
```

To get the content from the fake VMs, use curl or a browser.  Run the curl command or reload the page multiple times to see unique content from each VM.

```shell script
curl 127.0.0.1:5000
```
