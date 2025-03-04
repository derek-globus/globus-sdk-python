
from globus_sdk.experimental.glocal.core import BaseBackend

class ComputeBackend(BaseBackend):

    service_name = "compute"
    base_url = "https://compute.api.globus.org/v2/"
