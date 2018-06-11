
from protobuf import Register_pb2 as register
import struct
import ctypes
import binascii


register_ = register.MobileRegister()
protocolHeader2 = register_.protocolHeader
protocolHeader2.uid="uid001"
protocolHeader2.eid="eid001"

register_.uid = "wwfdfadfawngdao802300001"

data_result = [0]*3
data_result[0]=0x1001
daba_body =  register_.SerializeToString()
data_result[1]=len(daba_body)
data_result[2]=daba_body


print(register_)
print(register_.SerializeToString())
print(data_result)

print("=============")

#data.append(0X1100)
#data_body = register_.SerializeToString()
#data.append(len(data_body))
#data.append(data_body)

print("bytes & bytearray")
protocolType = 0X1100
headerType = struct.pack('<h',protocolType)
body = register_.SerializeToString()
bodyLength = struct.pack('<i',len(body))

data = (protocolType,len(body),body)

len_body = len(body)

print(type(body))
dataStruct = struct.Struct("hi"+str(len_body)+"s")

databuffer = ctypes.create_string_buffer(dataStruct.size)

print(binascii.hexlify(databuffer))
dataStruct.pack_into(databuffer,0,*data)
print(binascii.hexlify(databuffer))
print(data)

temp = struct.pack('!his',protocolType,len(body),body)

tempstr = struct.pack('@hip',protocolType,len(body),body)

token  = struct.pack("h",protocolType)
token+= struct.pack("i",len_body)

print(token)



