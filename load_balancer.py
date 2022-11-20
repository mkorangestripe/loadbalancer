#!/usr/bin/env python3

"""
This load balancer distributes requests between multiple Docker containers.
"""

import os
import sys
import requests
import yaml
from flask import Flask


class LoadBalancerMethod:
    """Load balancer methods"""

    def __init__(self, vms):
        self.vms = vms
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
            self.ratio = self.vms[self.vm_hostnames[self.target_vm_i]][self.ratio_i]
        else:
            self.target_vm_i += 1
            self.ratio = self.vms[self.vm_hostnames[self.target_vm_i]][self.ratio_i]
        return vm


host_list_file = 'vm_hostlist.yaml'

if os.path.exists(host_list_file) is False:
    print("\n" + str(host_list_file), "not found")
    sys.exit(1)

with open(host_list_file, 'r', encoding="utf-8") as f:
    vms_yaml = f.read()

vms_dict = yaml.safe_load(vms_yaml)

load_balancer_method = LoadBalancerMethod(vms_dict)

app = Flask(__name__)

@app.route('/')
def distrubute():
    """Distribute the load"""
    vm = load_balancer_method.round_robin_selector()
    r = requests.get('http://' + vm, timeout=5)
    return str(r.text)
