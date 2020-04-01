import _thread
import socket
import pdb


class CRC(object):
    def __init__(self,send):
        self.send = int(send,2)
        self.receive = int(send,2)
        self.crc_remain = int(send,2)
        self.poly = 0x1021
        self.crc = int(send,2) << 16

    def get_crc(self):
        self.crc = int(self.send) << 16
        for i in range(16):
            if((self.crc_remain & 0x8000)!=0):
                self.crc_remain = int(self.crc_remain << 1)
                self.crc_remain = int(self.crc_remain ^ self.poly)
            else:
                self.crc_remain = (int)(self.crc_remain << 1)

            self.crc_remain = self.crc_remain & 0x0000ffff
        self.crc = self.crc ^ self.crc_remain

    def crc_verify(self):
        for i in range(32):
            if((self.receive & 0x80000000)!= 0):
                self.receive = self.receive << 1
                self.receive = self.receive ^ (self.poly << 16)
            else:
                self.receive = self.receive << 1
            self.receive = self.receive & 0xffffffff

        if self.receive == 0:
            return True
        else:
            return False

    def set_receive(self, s):
        if s[0] == 'b':
            s = '0' + s
        self.receive = int(s, 2)

    def show_information(self):
        print("Send data :  {}".format(bin(self.send)))
        print("Generate poly in crc-ctitt style: 0x% x "% self.poly)
        print("CRC CODE :  {}" .format(bin(self.crc_remain)))
        print("Frame :  {}" .format(bin( self.crc)))
        print("Receive : {}" .format(bin(self.crc >> 16)))


def Receiver(Threadname):
    s = socket.socket()
    host = socket.gethostname()  # 获取本地主机名
    port = 8888  # 设置端口
    s.connect((host, port))
    print('Receiver is working.')
    frame_expected = 65534
    while True:
        # receive_id = 65536
        recv_byte = s.recv(1024)
        recv = recv_byte.decode(encoding='UTF-8', errors='strict')
        # pdb.set_trace()
        crc = CRC('101')
        crc.set_receive(recv)
        # pdb.set_trace()
        if crc.crc_verify():
            receive_id = eval(recv[:-16])
            if receive_id == 65534:
                frame_expected = 65535
            else:
                frame_expected = 65534
            print('Frame ' + str(receive_id) + ' has been accepted.')
            Ack = bin(frame_expected).encode('UTF-8')
            s.send(Ack)
        else:
            print('Frame ' + str(frame_expected) + ' is wrong, it has been asked to be resent.')
            Ack = bin(frame_expected).encode('UTF-8')
            s.send(Ack)


if __name__ == "__main__":
    _thread.start_new_thread(Receiver, ("Thread-2", ))
    while True:
        pass
