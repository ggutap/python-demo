import websocket
import protobuf.Register_pb2 as register
import struct
import ctypes,binascii

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


    protocolType = 0X1100
    headerType = struct.pack('<h',protocolType)
    body = register_buf.SerializeToString()
    body_length = len(body);

    data = (protocolType,body_length,body)

    data_struct = struct.Struct("hi"+str(body_length)+"s")
    data_buffer = ctypes.create_string_buffer(data_struct.size)


    data2 = [struct.pack('h',protocolType),struct.pack('i',body_length),body]
    #print(binascii.b2a_hex(data2))

    print(binascii.b2a_hex(struct.pack('hip',protocolType,body_length,body)))
    #ws.send(data_struct.pack_into(data_buffer,0,*data))
    ws.send(binascii.b2a_hex(struct.pack('hip',protocolType,body_length,body)))
    #ws.send(data)



if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.0.222:8001",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()