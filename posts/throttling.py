from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ObjectThrottle(AnonRateThrottle):
    rate = "1000/m"

class ObjectAnonThrottle(AnonRateThrottle):
    rate = "1/s"