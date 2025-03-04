
from globus_sdk.experimental.glocal.core import BaseBackend

class TimersBackend(BaseBackend):

    service_name = "timers"
    base_url = "https://timer.automate.globus.org/"
