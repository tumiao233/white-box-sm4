import logging

from sage.all import GF
from sage.all import matrix
from sage.all import vector

import tools

gf2 = GF(2)

class WhiteBoxSM4:
    """
    生成白盒密码的矩阵和向量
    """

    def __init__(self,key):
        self.block_size = 128
        self.key_size = 32
        self.word_size = 32
        self.key_words = 4
        self.rounds = 32



        self._k = self._key_expansion(key)

    def _key_expansion(self,key):
        tool=tools.Tools()
        return tool.extend_key(key)

    def _rotate_left_matrix(self,pos):
        m = matrix(gf2,192)
        for i in range(self.word_size):
            for j in range(5):
                m[i+j*self.word_size,i+j*self.word_size]=1
            m[i+5*self.word_size,5*self.word_size+(i+pos)%self.word_size]=1
        return m

    def l_xor(self):
        m = matrix(gf2,192)

        for i in range(self.word_size):
            for j in range(6):
                m[i + j * self.word_size, i + j * self.word_size] = 1
            m[i+4*self.word_size,i+5*self.word_size]=1
        return m

    def r_xor(self):
        m = matrix(gf2, 192)

        for i in range(self.word_size):
            for j in range(6):
                m[i + j * self.word_size, i + j * self.word_size] = 1
            m[i + 4 * self.word_size, i] = 1
        return m

    def xor(self,n):
        m = matrix(gf2, 192)
        for i in range(self.word_size):
            for j in range(5):
                m[i + j * self.word_size, i + j * self.word_size] = 1
            m[i+5*self.word_size,i+self.word_size]=1
            m[i + 5 * self.word_size, i + 2*self.word_size] = 1
            m[i + 5 * self.word_size, i + 3*self.word_size] = 1

        v = vector(gf2, 192)
        for i in range(self.word_size):
            v[6*self.word_size-i-1]=(self._k[n][31-i])&1

        return m,v

    def lt(self):
        m = matrix(gf2, 192)
        for i in range(128):
            m[i,i+32]=1
        return m

    def random_affine_layers(self):
        import random,datetime
        random.seed(datetime.datetime.now())
        ms = [[[]*192]*192]*33
        for i in range(33):
            for j in range(192):
                for k in range(192):
                    ms[i][j][k]=random.randint(0,1)
        vs=[[]*192]*33
        for i in range(33):
            for j in range(192):
                vs[i][j]=random.randint(0,1)
        return ms,vs

    def affine_layers(self):
        lt = self.lt()
        xor=[]
        for i in range(32):
            xor.append(self.xor(i))
        r_xor=self.r_xor()
        l_xor=self.l_xor()
        rotate_left_matrix=[self._rotate_left_matrix(2),self._rotate_left_matrix(8),self._rotate_left_matrix(8),self._rotate_left_matrix(6)]

        (m_first,v_first)=xor[0]
        m_mid = rotate_left_matrix[0]*l_xor*rotate_left_matrix[1]*l_xor*rotate_left_matrix[2]*l_xor*rotate_left_matrix[3]*l_xor*r_xor*lt*xor[0][0]
        m_last = rotate_left_matrix[0]*l_xor*rotate_left_matrix[1]*l_xor*rotate_left_matrix[2]*l_xor*rotate_left_matrix[3]*l_xor*r_xor*lt

        matrices = []
        vectors = []

        matrices.append(m_first)
        vectors.append(v_first*m_first)

        print(v_first)
        for i in range(1,32):
            matrices.append(m_mid)
            vectors.append(xor[i][1]*m_mid)
        matrices.append(m_last)
        return matrices,vectors

if __name__ == '__main__':
    wihteBox=WhiteBoxSM4("0123456789abcdeffedcba9876543210")
    m,v=wihteBox.affine_layers()
    print(m[12])
    print(v[14])
