import requests

class HTTPClient:
    def get(self, url, params=None):
        raise NotImplementedError
    
class RequestsHTTPClient(HTTPClient):
    def get(self, url, params=None):
        return requests.get(url, params=params)    