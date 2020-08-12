# TCPSimpleServer

## Example
``` python
import asyncio

from TCPSimpleServer import create_tcp_server

loop = asyncio.get_event_loop()

@create_tcp_server(loop, ('', 5000))
def callback(data):
    print(data)

loop.run_forever()

```