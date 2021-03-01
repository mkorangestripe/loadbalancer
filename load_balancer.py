#!/usr/bin/env python3

# Create an application that simulates a load balancer and 
# is able to distribute the requests between 2 or more backend services.
# Assume the most basic balancer algorithm: round robin.

# Extras:
# * Dynamic. The configuration is not hardcoded, it might be changed
# without modifying the actual application code, thus including a config
# file with any well-known markup language like yaml is a plus.
# * Healthcheck. The ability to take off/on or serve the response
# if any of the backend services is alive.
# * Sorry page. If no backends are available avoid sending a "service
# unavailable (503)" response.

"""
This simulates a load balancer that distributes requests between multiple virtual machines.

To start this application with Flask:
export FLASK_APP=load_balancer.py
flask run

To get the content from the fake VMs, use curl or a browser.
Run the curl command or reload the page multiple times to see unique content from each VM.
curl 127.0.0.1:5000
"""

from fake_vms import Fake_VMs
from flask import Flask
import os
import sys
import yaml

host_list_file = 'vm_hostlist.yaml'

if os.path.exists(host_list_file) == False:
    print("\n" + str(host_list_file), "not found")
    sys.exit(1)

with open(host_list_file, 'r') as f:
    vms_yaml = f.read()

vms = yaml.load(vms_yaml)
vm_count = len(vms)

fake_vms = Fake_VMs()

target_vm = -1

def round_robin_selector():
    global target_vm
    if target_vm == vm_count - 1:
        target_vm = 0
    else:
        target_vm += 1

app = Flask(__name__)

@app.route('/')
def distrubute():
    round_robin_selector()
    call_vm_method = getattr(fake_vms, vms[target_vm])
    call_vm_method()
    return str(fake_vms.content + '\n') 
