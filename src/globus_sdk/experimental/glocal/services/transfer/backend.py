
from globus_sdk.experimental.glocal.core import BaseBackend

class TransferBackend(BaseBackend):

    service_name = "timers"
    base_url = "https://transfer.api.globus.org/"
