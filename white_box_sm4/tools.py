import zipfile


class Tools:

    SBOX = ['d6', '90', 'e9', 'fe', 'cc', 'e1', '3d', 'b7', '16', 'b6', '14', 'c2', '28', 'fb', '2c', '05',
                   '2b', '67', '9a', '76', '2a', 'be', '04', 'c3', 'aa', '44', '13', '26', '49', '86', '06', '99',
                   '9c', '42', '50', 'f4', '91', 'ef', '98', '7a', '33', '54', '0b', '43', 'ed', 'cf', 'ac', '62',
                   'e4', 'b3', '1c', 'a9', 'c9', '08', 'e8', '95', '80', 'df', '94', 'fa', '75', '8f', '3f', 'a6',
                   '47', '07', 'a7', 'fc', 'f3', '73', '17', 'ba', '83', '59', '3c', '19', 'e6', '85', '4f', 'a8',
                   '68', '6b', '81', 'b2', '71', '64', 'da', '8b', 'f8', 'eb', '0f', '4b', '70', '56', '9d', '35',
                   '1e', '24', '0e', '5e', '63', '58', 'd1', 'a2', '25', '22', '7c', '3b', '01', '21', '78', '87',
                   'd4', '00', '46', '57', '9f', 'd3', '27', '52', '4c', '36', '02', 'e7', 'a0', 'c4', 'c8', '9e',
                   'ea', 'bf', '8a', 'd2', '40', 'c7', '38', 'b5', 'a3', 'f7', 'f2', 'ce', 'f9', '61', '15', 'a1',
                   'e0', 'ae', '5d', 'a4', '9b', '34', '1a', '55', 'ad', '93', '32', '30', 'f5', '8c', 'b1', 'e3',
                   '1d', 'f6', 'e2', '2e', '82', '66', 'ca', '60', 'c0', '29', '23', 'ab', '0d', '53', '4e', '6f',
                   'd5', 'db', '37', '45', 'de', 'fd', '8e', '2f', '03', 'ff', '6a', '72', '6d', '6c', '5b', '51',
                   '8d', '1b', 'af', '92', 'bb', 'dd', 'bc', '7f', '11', 'd9', '5c', '41', '1f', '10', '5a', 'd8',
                   '0a', 'c1', '31', '88', 'a5', 'cd', '7b', 'bd', '2d', '74', 'd0', '12', 'b8', 'e5', 'b4', 'b0',
                   '89', '69', '97', '4a', '0c', '96', '77', '7e', '65', 'b9', 'f1', '09', 'c5', '6e', 'c6', '84',
                   '18', 'f0', '7d', 'ec', '3a', 'dc', '4d', '20', '79', 'ee', '5f', '3e', 'd7', 'cb', '39', '48', ]
    FK = ['a3b1bac6', '56aa3350', '677d9197', 'b27022dc']
    CK = []
    for i in range(32):
        CK.append([])
        for j in range(4):
            CK[i].append(((4*i+j)*7) % 256)

    def __int__(self):
        pass

    def oct_2_bin(self,oct):
        k = []
        for i in range(32):
            k.append((oct>>i)&1)
        k.reverse()
        return k

    def zipSM4(*file,mode):
        if mode== 'e':

            zippp=zipfile.ZipFile("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/white_box_sm4_encrypt.key",'w',zipfile.ZIP_DEFLATED)
            keys=file[0][3]
            del file[0][3]
            for f in file[0]:
                zippp.write(f)
            zippp.close()
            with open("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/white_box_sm4_encrypt.key",'r+',encoding='utf-8',errors='ignore') as f:
                content=f.read()
                f.seek(0,0)
                f.write(keys+'\n'+content)

        elif mode=='d':
            zippp = zipfile.ZipFile(
                "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesDecrypt/white_box_sm4_decrypt.key",'w',zipfile.ZIP_DEFLATED)
            keys = file[0][3]
            del file[0][3]
            for f in file[0]:
                zippp.write(f)
            zippp.close()
            with open(
                    "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesDecrypt/white_box_sm4_decrypt.key",
                    'r+',encoding='utf-8',errors='ignore') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(keys + '\n' + content)

    def key_hex_2_bin(self,str):
        """
        高位在前
        :param str:
        :return:一个list
        """
        length = len(str)//8
        bound =32
        if length==0:
            length=1
            bound = len(str)*4
        hex = int(str,16)

        k=[]

        if length ==1:
            for i in range(bound):
                k.append((hex>>i)&1)
            k.reverse()
        else:
            for i in range(length):
                k.append([])
                for j in range(bound):
                    k[i].append((hex>>(j+length*i))&1)
                k[i].reverse()
            k.reverse()

        return k

    def xor_x_y(self,x,y):
        length = len(x)
        for i in range(length):
            x[i] = x[i]^y[i]

    def bin_2_hex(self,k):
        num = 0
        for i in range(32):
            num = num + k[i]*2**(31-i)
        hex_num=hex(num).strip('0x')
        l=len(hex_num)
        if l<8:
            for i in range(8-l):
                hex_num='0'+hex_num
        return hex_num

    def key_bin_2_hex(self,k):
        hk=[]
        for i in range(4):
            hk.append([])
            num = 0
            for j in range(32):
                num = num + k[i][j]*2**(31-i)
            hk[i].append(hex(num).strip('0x'))
        return hk

    # s盒变换，一次处理一个字，共用4个S盒
    # 输入一个8位16进制的字符串，如'abcd1234'
    def S_box(self, str:str):
        # 将8位字符串分成4组
        A = list(str)
        a = [0, 0, 0, 0]
        Out = [0, 0, 0, 0]
        a[0] = [A[0], A[1]]  # a0=['a','b']
        a[1] = [A[2], A[3]]
        a[2] = [A[4], A[5]]
        a[3] = [A[6], A[7]]
        # 高位的16进制转换成10进制*16+低位的16进制转换成10进制
        for j in range(4):
            for i in range(2):
                a[j][i] = int(a[j][i], 16)
            b = int(a[j][0] * 16 + a[j][1])
            Out[j] = Tools.SBOX[b]
        # for i in range(4):
        #     Out[i] = '{:02x}'.format(Out[i])
        S_out = ''.join(Out)
        return S_out

    def extend_key(self,key:str):
        k = self.key_hex_2_bin(key)
        fk=[[],[],[],[]]
        ck = []
        for i in range(4):
            fk[i]=self.key_hex_2_bin(self.FK[i])
            self.xor_x_y(k[i],fk[i])
        for i in range(32):
            ck.append([])
            for j in range(4):
                ck[i].extend(self.oct_2_bin(self.CK[i][j]))
        rk=[]
        for i in range(32):
            b=[]
            for j in range(len(k[0])):
                b.append(k[1][j]^k[2][j]^k[3][j]^ck[i][j])
            b=self.key_hex_2_bin(self.S_box(self.bin_2_hex(b)))
            b_13=b[13:]+b[:13]
            b_23=b[23:]+b[:23]
            for j in range(len(k[0])):
                b[j]=b[j]^b_13[j]^b_23[j]^k[0][j]
            rk.append(b)
            k[0]=k[1]
            k[1]=k[2]
            k[2]=k[3]
            k[3]=b
        return rk


    def rk_to_hex(self,rk):
        rk_hex=[]
        for i in range(32):
            rk_hex.append(self.bin_2_hex(rk[i]))
        print(rk_hex)
        return rk_hex

from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import binascii
import base64


class SM4:
    def __init__(self):
        self.crypt_sm4 = CryptSM4()

    def str_to_hexStr(self, hex_str):
        hex_data = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hex_data)
        return str_bin.decode('utf-8')

    def encrypt(self, encrypt_key, value):
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(encrypt_key.encode(), SM4_ENCRYPT)
        date_str = str(value)
        encrypt_value = crypt_sm4.crypt_ecb(date_str.encode())
        return base64.b64encode(encrypt_value)

    def decrypt(self, decrypt_key:str, encrypt_value):
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(decrypt_key.encode(), SM4_DECRYPT)
        decrypt_value = crypt_sm4.crypt_ecb(base64.b64decode(encrypt_value))
        return self.str_to_hexStr(decrypt_value.hex())

    def encryptImage(self,encrypt_key,value):
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(encrypt_key.encode(), SM4_ENCRYPT)
        encrypt_value=crypt_sm4.crypt_ecb(value)
        return encrypt_value

    def decryptImage(self,encrypt_key,encrypt_value):
        crypt_sm4 = self.crypt_sm4
        crypt_sm4.set_key(encrypt_key.encode(), SM4_DECRYPT)
        decrypt_value=crypt_sm4.crypt_ecb(encrypt_value)
        return decrypt_value


if __name__ == '__main__':
    #tools=Tools()
    #tools.rk_to_hex(tools.extend_key('0123456789abcdeffedcba9876543210'))

    key='1234567890123456'
    text='abcdsdafadsfasdfdsfdasfadsfasdfasdfdasfadsfasfadsfas'
    c='SNxVNMAoOQ0pgLdrtGyNGUZSiw+HbyAEQ7pWwtPdtXjg8gTlGKvngIXUTaPdafTvjAJMk79S0POhbUqm9lrO4Q=='
    SM4=SM4()
    print(SM4.encrypt(key,text))
    print(SM4.decrypt(key,c))







