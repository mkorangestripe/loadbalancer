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

import os
import sys
import yaml
from flask import Flask
from fake_vms import FakeVMs


class LoadBalancerMethod:
    """Load balancer methods"""

    def __init__(self, vms):
        self.vm_hostnames = list(vms.keys())
        self.vm_count = len(self.vm_hostnames)
        self.ratio_i = 1
        self.target_vm_i = 0
        self.ratio = vms[self.vm_hostnames[self.target_vm_i]][self.ratio_i]

    def round_robin_selector(self):
        """Select the vm to take traffic with respect to ratio"""
        vm = self.vm_hostnames[self.target_vm_i]
        if self.ratio > 1:
            self.ratio -= 1
        elif self.target_vm_i == self.vm_count - 1:
            self.target_vm_i = 0
            self.ratio = vms[self.vm_hostnames[self.target_vm_i]][self.ratio_i]
        else:
            self.target_vm_i += 1
            self.ratio = vms[self.vm_hostnames[self.target_vm_i]][self.ratio_i]
        return vm


host_list_file = 'vm_hostlist.yaml'

if os.path.exists(host_list_file) is False:
    print("\n" + str(host_list_file), "not found")
    sys.exit(1)

with open(host_list_file, 'r') as f:
    vms_yaml = f.read()

vms = yaml.safe_load(vms_yaml)

fake_vms = FakeVMs()
load_balancer_method = LoadBalancerMethod(vms)

app = Flask(__name__)

@app.route('/')
def distrubute():
    """Distribute the load"""
    vm = load_balancer_method.round_robin_selector()
    call_vm_method = getattr(fake_vms, vm)
    call_vm_method()
    return str(fake_vms.content + '\n')
