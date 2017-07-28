import asyncio
import websockets

#async def receive(m):
#    print(str(m))
#
#async def receiver_handler(websocket):
#    while True:
#        message = await websocket.recv()
#        await receive(message)
#        await websocket.send(message)


async def sender_handler(websocket):
    while True:
        message = send()
        await websocket.send(message)


async def handler(websocket, path):
    #receiver_task = asyncio.ensure_future(receiver_handler(websocket))
    sender_task = asyncio.ensure_future(sender_handler(websocket))
    
    done, pending = await asyncio.wait(
        [sender_task],
        return_when = asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

start_server = websockets.serve(handler, '127.0.0.1', 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
