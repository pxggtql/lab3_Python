import _thread
import time
import socket
import select



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

    def get_frame(self):
        return bin(self.crc)

    def get_wrong_frame(self):
        wrong_frame = bin(self.crc)
        wrong_char = str(0 & eval(wrong_frame[-1]))
        wrong_frame = wrong_frame[1: -1] + wrong_char
        return wrong_frame

    def show_information(self):
        print("Send data :  {}".format(bin(self.send)))
        print("Generate poly in crc-ctitt style: 0x% x "% self.poly)
        print("CRC CODE :  {}" .format(bin(self.crc_remain)))
        print("Frame :  {}" .format(bin( self.crc)))
        print("Receive : {}" .format(bin(self.crc >> 16)))


def Sender(Threadname, FilterError, FilterLost):
    num = 7
    s = socket.socket()
    host = socket.gethostname()  # 获取本地主机名
    port = 8888  # 设置端口
    s.bind((host, port))
    s.listen(1)
    next_frame_to_send = 65534
    print("Sender is working.")
    c, addr = s.accept()
    print(Threadname + ": " + str(addr) + " has connected.")
    while True:
        if num % FilterError == 0:
            frame_id = bin(next_frame_to_send)
            crc = CRC(frame_id)
            crc.get_crc()
            ori = next_frame_to_send
            if next_frame_to_send == 65534:
                next_frame_to_send = 65535
            else:
                next_frame_to_send = 65534
            # pdb.set_trace()
            pkt = crc.get_wrong_frame().encode(encoding='UTF-8', errors='strict')
            c.send(pkt)
            num += 1
            print('Frame ' + str(ori) + ' has been sent. Now next_frame_to_send is ' + str(next_frame_to_send))
        elif num % FilterLost == 0:
            ori = next_frame_to_send
            if next_frame_to_send == 65534:
                next_frame_to_send = 65535
            else:
                next_frame_to_send = 65534
            num += 1
            print('Frame ' + str(ori) + ' will be lost. Now next_frame_to_send is ' + str(next_frame_to_send))
        else:
            frame_id = bin(next_frame_to_send)
            crc = CRC(frame_id)
            crc.get_crc()
            Msg = crc.get_frame()
            ori = next_frame_to_send
            if next_frame_to_send == 65534:
                next_frame_to_send = 65535
            else:
                next_frame_to_send = 65534
            pkt = Msg.encode(encoding='UTF-8', errors='strict')
            c.send(pkt)
            num += 1
            print('Frame ' + str(ori) + ' has been sent. Now next_frame_to_send is ' + str(next_frame_to_send))
        Ack = b''
        c.setblocking(0)
        ready = select.select([c], [], [], 5)
        if ready[0]:
            Ack = c.recv(1024)
        if Ack != b'':
            Ack_id = int(Ack.decode(encoding='UTF-8', errors='strict'), 2)
            if next_frame_to_send == 65534:
                flag = 65535
            else:
                flag = 65534
            if Ack_id == next_frame_to_send:
                print('Frame ' + str(flag) + ' has been accepted.')
            else:
                # wrong frame
                next_frame_to_send = Ack_id
                print('Frame ' + str(Ack_id) + ' is error, it will be resent later.')
        else:
            if next_frame_to_send == 65534:
                next_frame_to_send = 65535
            else:
                next_frame_to_send = 65534
            print("Frame " + str(next_frame_to_send) + " has been lost, it will be resent later.")
        time.sleep(8)


class WaitForAck(object):
    def __init__(self, frame_id):
        self.timelimited = 5
        self.frame_id = frame_id


if __name__ == "__main__":
    _thread.start_new_thread(Sender, ("Thread-1", 11, 7, ))
    while True:
        pass
