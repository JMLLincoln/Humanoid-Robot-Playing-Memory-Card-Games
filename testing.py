import json
import asyncio
import websockets

class SetupException(Exception):
    pass

def load_json():
        ''' Loads the data file from the camera module '''
        with open('data.json') as data_file:    
            data = json.load(data_file)

        if not data:
            raise SetupException("Empty data file. The data file containing board information is empty.")
        else:
            return data

async def game_handler(websocket):
   
    data = load_json()
    values = []
    flipped = []
    for i in range(len(data)):
        values.append(None)
        flipped.append(None)

    for item in data:
        n = item['index'] - 1
        
        values[n] = item['value']
        
        if item['flipped'] == True:
            flipped[n] = 0
        else:
            flipped[n] = 1

    message = "%s|%s" % (values, flipped)
        
    print("sending %s" % message)
    await websocket.send(message)

async def handler(websocket, path):
    game_task = asyncio.ensure_future(game_handler(websocket))
    
    done, pending = await asyncio.wait([game_task],
        return_when = asyncio.FIRST_COMPLETED,
    )
    
    for task in pending:
        task.cancel()

start_server = websockets.serve(handler, '127.0.0.1', 8888)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
