from channels.routing import route
from .consumer import ws_message, ws_status, ws_kill, ws_connect, ws_disconnect
 

channel_routing = [
    route("websocket.receive", ws_message, path=r"^/request"),
    route("websocket.receive", ws_status, path=r"^/serverStatus"),
    route("websocket.receive", ws_kill, path=r"^/kill"),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
]