class FakeVMs:
    """
    With version 2 of this load balancer this class is no longer being used.
    These methods emulate virtual machines that the load balancer distrubutes traffic to.
    The bigger cats take more traffic.
    """

    def __init__(self):
        self.content_list = ["Load balancer simulator. The bigger cats take more traffic.<br/><br/>\n", ""]
        self.content = ""
        self.listToStr = ""

    def vm1(self):
        self.content_list[1] = "cheetah"
        self.content = self.listToStr.join(self.content_list)

    def vm2(self):
        self.content_list[1] = "ocelot"
        self.content = self.listToStr.join(self.content_list)

    def vm3(self):
        self.content_list[1] = "mountain lion"
        self.content = self.listToStr.join(self.content_list)

    def vm4(self):
        self.content_list[1] = "jaguarundi"
        self.content = self.listToStr.join(self.content_list)
