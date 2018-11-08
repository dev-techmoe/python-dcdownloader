import aiohttp
from yarl import URL


class ProxyConnector(aiohttp.connector.TCPConnector):

    def __init__(self, *args, **kwargs):
        if kwargs.get('proxy'):
            self.proxy = kwargs.get('proxy')

        kwargs.pop('proxy')

        super().__init__(*args, **kwargs)

    async def _create_connection(self, req, traces=None, timeout=None):
        if req.proxy == None and 'proxy' in dir(self):
            # req.setdefault('proxy', URL(self.proxy))
            req.proxy = URL(self.proxy)
        
        if req.proxy:
            _, proto = await super()._create_proxy_connection(
                req,
                traces=traces,
                timeout=timeout
            )
        else:
            _, proto = await super()._create_direct_connection(
                req,
                traces=traces,
                timeout=timeout
            )

        return proto
