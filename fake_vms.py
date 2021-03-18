class FakeVMs:
    """
    These methods emulate virtual machines that the load balancer distrubutes traffic to.
    The bigger cats can take more traffic.
    """

    def __init__(self):
        self.content = ""

    def vm1(self):
        self.content = "cheetah"

    def vm2(self):
        self.content = "ocelot"

    def vm3(self):
        self.content = "mountain lion"

    def vm4(self):
        self.content = "jaguarundi"
