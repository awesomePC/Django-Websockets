from channels.routing import route
from .consumer import ws_resolver, ws_connect, ws_disconnect
 

channel_routing = [
    route("websocket.receive", ws_resolver),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
]