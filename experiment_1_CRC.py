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
            else :
                self.receive = self.receive << 1
            self.receive = self.receive & 0xffffffff

        if self.receive == 0:
            return True
        else:
            return False

    def set_receive(self, s):
        self.receive = int(s, 2)

    def show_information(self):
        print("Send data :  {}".format(bin(self.send)))
        print("Generate poly in crc-ctitt style: 0x% x "% self.poly)
        print("CRC CODE :  {}" .format(bin(self.crc_remain)))
        print("Frame :  {}" .format(bin(self.crc)))
        print("Receive : {}" .format(bin(self.crc >> 16)))




if __name__ == '__main__':
    send = input("Please input your sending data.\n")
    crc = CRC(send)
    crc.get_crc()
    crc.crc_verify()
    crc.show_information()
    crc.set_receive('0b10000000000000001')
    print(crc.crc_verify())



















