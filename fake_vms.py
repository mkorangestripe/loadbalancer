class Fake_VMs(object):
    """These methods emulate virtual machines that the load balancer distrubutes traffic to."""

    def __init__(self):
        pass
        
    def vm1(self):
        self.content = "cheetah"

    def vm2(self):
        self.content = "ocelot"

    def vm3(self):
        self.content = "lynx"

    def vm4(self):
        self.content = "jaguarundi"
