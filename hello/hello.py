
from protobuf import Register_pb2 as register


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
data = [0x0, 0x1, 0x2]
data[0] = bytearray(0X1100)
daba_body = register_.SerializeToString()
data[1] = bytearray(len(daba_body))
data[2] = daba_body

print(data)



