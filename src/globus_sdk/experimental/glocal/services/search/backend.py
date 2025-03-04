
from globus_sdk.experimental.glocal.core import BaseBackend

class SearchBackend(BaseBackend):

    service_name = "search"
    base_url = "https://search.api.globus.org/"
