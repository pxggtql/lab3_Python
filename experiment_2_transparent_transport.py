
class transprent_transport():
    def __init__(self,packet):
        self.bit_flag = "01111110"
        self.byte_flag = '~'
        self.escape = '}'
        self.escape_bit = '0'
        self.one_bit = '1'
        self.max_sucessive_ones = 5
        self.count_ones = int(0)
        self.packet = packet
        self.message = packet

    def isMaxSeccessOnes(self, bit):
        if bit == self.one_bit:
            self.count_ones = self.count_ones + 1
        else:
            self.count_ones = 0

        return self.count_ones == self.max_sucessive_ones

    def bit_suffing(self,packet):
        self.count_ones
        frame = []
        for i in self.bit_flag:
            frame.append(i)
        for i in packet:
            frame.append(i)
            if self.isMaxSeccessOnes(i):
                frame.append(self.escape_bit)
                self.count_ones = 0

        frame.append(self.bit_flag)
        frame_str = "".join(frame)

        return frame_str

    def byte_stuffng(self,packet):
        frame = []
        frame.append(self.byte_flag)
        for i in packet:
            if i == self.byte_flag:
                frame.append(self.escape)
            elif i == self.escape:
                frame.append(self.escape)
                frame.append("]")
            else :
                frame.append(i)
        frame.append(self.byte_flag)
        frame_str = "".join(frame)

        return frame_str
    def de_bit_stuffing(self,packet):
        ss = packet
        start = ss.index("01111110")
        ss = ss[start+8: ]
        end = ss.index("01111110")
        ss = ss[:end]
        if "01111110" in ss:
            index = ss.index("01111110")
        while "01111110" in ss:
            ss = ss[:index+4] +ss[index+6:]
            index = ss.index("01111110")
        return str(ss)

    def de_byte_stuffing(self,packet):
        if len(packet) % 8 !=0 :
            print("Frame Error!")
            return
        ls = []
        for i in range(int(len(packet)/8)):
            ls.append(packet[i * 8 :i * 8 + 8])
        ss = ""
        for i in ls:
            ss += self.decode(i)
        if '~' in ss:
            start = int(ss.index('~'))
            ss = ss[start + 1:]
        if '~' in ss:
            end = int(ss.index('~'))
            ss = ss[:end]
        if "}^" in ss:
            index = int(ss.index("}^"))
        while "}^" in ss:
            ss += "~"
            ss = ss[:index + 1] + ss[index+3 : ]
            index = int(ss.index("}^"))

        tran_s_b = self.str_to_binstr(ss)
        return tran_s_b

    def decode(self,s):
        # 实现二进制表示转换成字符串表示
        # 二进制表示 -> ASCII码数值 -> 字符串表示
        bin_str = ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

        return bin_str


    def str_to_binstr(self,string):

        # 实现字符串转换成二进制表示
        # 字符串 -> ASCII码数值 -> 二进制表示
        ###str_bin = ' '.join([bin(ord(c)).replace('0b', '') for c in s]) 该代码可转换成裁开的for 循环，如下四行代码：

        tmp = []
        for c in string:
            tmp.append(bin(ord(c)).replace('0b', ''))

        str_bin = ""
        for i in tmp:
            tmp = i
            length = len(i)
            while len(tmp)<8:
                tmp = '0'+tmp
            str_bin = str_bin +tmp
        #print(str_bin)
        return str_bin



    def test_bit_stuffing(self):
        send_copy = self.packet
        print("定界符： {}".format(self.byte_flag))
        print("帧数据信息： {}".format(send_copy))
        after_send = self.bit_suffing(send_copy)
        #after_send_bin = self.str_to_binstr(after_send)
        print("比特填充后的帧： {}".format(after_send))
        tran_s_b = self.de_bit_stuffing(after_send)
        print(tran_s_b)

    def test_byte_stuffing(self):

        send_bi = self.str_to_binstr(self.message)
        print("定界符： {}".format(self.byte_flag))
        print("转义符： {}".format(self.escape))
        print("帧数据信息： {}".format(send_bi))
        after_send = self.byte_stuffng(self.message)
        after_send_bin = self.str_to_binstr(after_send)
        print("字节填充后的帧： {}".format(after_send_bin))
        trans_s_b = self.de_byte_stuffing(after_send_bin)

        print("字节删除后的帧： {}".format(trans_s_b))

if __name__ == '__main__':
    send_message = input("Please input your message :\n")
    TransparentTransport = transprent_transport(send_message)
    TransparentTransport.test_bit_stuffing()
    TransparentTransport.test_byte_stuffing()








