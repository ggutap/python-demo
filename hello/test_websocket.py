import websocket
import protobuf.Register_pb2 as register
import struct

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        send_register(ws)
        #ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

def send_register(ws):

    register_buf =register.MobileRegister()
    register_buf.protocolHeader.uid="uid001"
    register_buf.protocolHeader.eid="eid001"
    register_buf.uid="uid001"

    data = [0,0,0]
    data[0] = bytearray(0X1100)
    daba_body = register_buf.SerializeToString()
    data[1] = bytearray(len(daba_body))
    data[2] = daba_body



    ws.send(data)



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8001",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()