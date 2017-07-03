import socket
import six.moves.cPickle as cPickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
conn, addr = s.accept()

while True:
    data = conn.recv(4096)
    data = cPickle.loads(data)
    print(data)

    if(data[2]):
        print("Game over")
        #break
    
    x = 1
    x = cPickle.dumps(x)
    conn.send(x)