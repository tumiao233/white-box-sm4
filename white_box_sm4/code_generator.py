from abc import ABC
from abc import abstractmethod


class CodeGenerator(ABC):
    _WORD_TYPES = {
        32: "uint32_t",
    }

    _WORD_IN_TYPES = {
        32: "SCNx32",
    }

    _WORD_OUT_TYPES = {
        32: "PRIx32",
    }

    _INCLUDE_INTTYPES = "#include <inttypes.h>\n"
    _INCLUDE_STDDEF = "#include <stddef.h>\n"
    _INCLUDE_STDIO = "#include <stdio.h>\n"
    _INCLUDE_STRING = "#include <string.h>\n"
    _INCLUDE_STDLIB = "#include <stdlib.h>\n"
    _INCLUDE_TIME="#include <time.h>\n"

    _FROM_BITS = (
        "void from_bits(uint8_t bits[BLOCK_SIZE], WORD_TYPE *x1, WORD_TYPE *x2,WORD_TYPE *x3,WORD_TYPE *x4) {\n"
        "    *x1 = 0;\n"
        "    *x2 = 0;\n"
        "    *x3 = 0;\n"
        "    *x4 = 0;\n"
        "    for (size_t i = 0; i < WORD_SIZE; i++) {\n"
        "        *x1 |= ((WORD_TYPE) bits[i]) << i;\n"
        "        *x2 |= ((WORD_TYPE) bits[WORD_SIZE + i]) << i;\n"
        "        *x3 |= ((WORD_TYPE) bits[WORD_SIZE*2 + i]) << i;\n"
        "        *x4 |= ((WORD_TYPE) bits[WORD_SIZE*3 + i]) << i;\n"  
        "    }\n"
        "}\n"
    )

    _TO_BITS = (
        "void to_bits(WORD_TYPE x1, WORD_TYPE x2,WORD_TYPE x3,WORD_TYPE x4, uint8_t bits[BLOCK_SIZE]) {\n"
        "    for (size_t i = 0; i < WORD_SIZE; i++) {\n"
        "        bits[i] = (x1 >> i) & 1;\n"
        "        bits[WORD_SIZE + i] = (x2 >> i) & 1;\n"
        "        bits[WORD_SIZE*2+i] = (x3 >> i) & 1;\n"
        "        bits[WORD_SIZE*3+i] = (x4 >> i) & 1;\n"
        "        bits[WORD_SIZE*4+i] = 0;\n"
        "        bits[WORD_SIZE*5+i] = 0;\n"
        "    }\n"
        "}\n"
    )

    _MATRIX_VECTOR_PRODUCT = (
        "void matrix_vector_product(uint8_t matrix[BLOCK_SIZE][BLOCK_SIZE], uint8_t x[BLOCK_SIZE], uint8_t res[BLOCK_SIZE]) {\n"
        "    for (size_t i = 0; i < BLOCK_SIZE; i++) {\n"
        "        for (size_t j = 0; j < BLOCK_SIZE; j++) {\n"
        "            res[i] ^= matrix[i][j] * x[j];\n"
        "        }\n"
        "    }\n"
        "}\n"
    )

    _VECTOR_ADDITION = (
        "void vector_addition(uint8_t vector[BLOCK_SIZE], uint8_t x[BLOCK_SIZE]) {\n"
        "    for (size_t i = 0; i < BLOCK_SIZE; i++) {\n"
        "        x[i] ^= vector[i];\n"
        "    }\n"
        "}\n"
    )

    _MODULAR_ADDITION = (
        "void modular_addition(uint8_t x[BLOCK_SIZE]) {\n"
        "    uint8_t carry = 0;\n"
        "    for (size_t i = 0; i < WORD_SIZE; i++) {\n"
        "        x[i] = x[i] + x[WORD_SIZE + i] + carry;\n"
        "        carry = x[i] > 1;\n"
        "        x[i] &= 1;\n"
        "    }\n"
        "}\n"
    )

    _ENCRYPT = (
        "void encrypt(WORD_TYPE p[4], WORD_TYPE c[4]) {\n"
        "    uint8_t x[BLOCK_SIZE];\n"
        "    uint8_t res[BLOCK_SIZE];\n"
        "    to_bits(p[0], p[1], p[2], p[3], x);\n"
        "    for (size_t i = 0; i < ROUNDS; i++) {\n"
        "        memset(&res, 0, BLOCK_SIZE * sizeof(uint8_t));\n"
        "        matrix_vector_product(MATRICES[i], x, res);\n"
        "        vector_addition(VECTORS[i], res);\n"
        "        \n"
        "        memcpy(&x, &res, BLOCK_SIZE * sizeof(uint8_t));\n"
        "    }\n"
        "\n"
        "    memset(&res, 0, BLOCK_SIZE * sizeof(uint8_t));\n"
        "    matrix_vector_product(MATRICES[ROUNDS], x, res);\n"
        "    vector_addition(VECTORS[ROUNDS], res);\n"
        "    from_bits(res, &c[0], &c[1],&c[2],&c[3]);\n"
        "}\n"
    )



    def _includes(self):
        return self._INCLUDE_INTTYPES + \
            self._INCLUDE_STDDEF + \
            self._INCLUDE_STDIO + \
            self._INCLUDE_STDLIB + \
            self._INCLUDE_STRING +\
            self._INCLUDE_TIME

    def _define_block_size(self, block_size):
        return f"#define BLOCK_SIZE {block_size}\n"

    def _define_word_size(self, word_size):
        return f"#define WORD_SIZE {word_size}\n"

    def _define_word_type(self, word_size):
        assert word_size in self._WORD_TYPES, f"Invalid or unsupported word size {word_size}"

        return f"#define WORD_TYPE {self._WORD_TYPES[word_size]}\n"

    def _define_word_in_type(self, word_size):
        assert word_size in self._WORD_IN_TYPES, f"Invalid or unsupported word size {word_size}"

        return f"#define WORD_IN_TYPE {self._WORD_IN_TYPES[word_size]}\n"

    def _define_word_out_type(self, word_size):
        assert word_size in self._WORD_OUT_TYPES, f"Invalid or unsupported word size {word_size}"

        return f"#define WORD_OUT_TYPE {self._WORD_OUT_TYPES[word_size]}\n"

    def _define_rounds(self, rounds):
        return f"#define ROUNDS {rounds}\n"

    def _defines(self, block_size, word_size, rounds):
        return self._define_block_size(block_size) + \
            self._define_word_size(word_size) + \
            self._define_word_type(word_size) + \
            self._define_word_in_type(word_size) + \
            self._define_word_out_type(word_size) + \
            self._define_rounds(rounds)



    def _functions(self, block_size, word_size, rounds):
        return self._FROM_BITS + \
            "\n" + \
            self._TO_BITS + \
            "\n" + \
            self._MATRIX_VECTOR_PRODUCT + \
            "\n" + \
            self._VECTOR_ADDITION + \
            "\n" + \
            self._MODULAR_ADDITION + \
            "\n" + \
            self._ENCRYPT

    def _main(self):
        return (
            f"int main(int argc, char *argv[]) {{\n"
            f"    if (argc < 2) {{\n"
            f"        return -1;\n"
            f"    }}\n"
            f"    WORD_TYPE p[4];\n"
            f"    WORD_TYPE c[4];\n"
            f"    if (argc < 3) {{\n"
            f"        size_t iterations;\n"
            f"        sscanf(argv[1], \"%zu\", &iterations);\n"
            f"        clock_t begin = clock();"
            f"        for (int i = 0; i < iterations; i++) {{\n"
            f"            p[0] = (((WORD_TYPE) rand()) << (WORD_SIZE / 2)) | ((WORD_TYPE) rand());\n"
            f"            p[1] = (((WORD_TYPE) rand()) << (WORD_SIZE / 2)) | ((WORD_TYPE) rand());\n"
            f"            p[2] = (((WORD_TYPE) rand()) << (WORD_SIZE / 2)) | ((WORD_TYPE) rand());\n"
            f"            p[3] = (((WORD_TYPE) rand()) << (WORD_SIZE / 2)) | ((WORD_TYPE) rand());\n"
            f"            encrypt(p, c);\n"
            f"        }}\n"
            f"        clock_t end = clock();"
            f"        double time_consumption = (double)(end-begin) / CLOCKS_PER_SEC;"
            f"        printf(\"%f\",time_consumption);"
            f"    }} else {{\n"
            f"        sscanf(argv[1], \"%\" WORD_IN_TYPE, &p[0]);\n"
            f"        sscanf(argv[2], \"%\" WORD_IN_TYPE, &p[1]);\n"
            f"        sscanf(argv[3], \"%\" WORD_IN_TYPE, &p[2]);\n"
            f"        sscanf(argv[4], \"%\" WORD_IN_TYPE, &p[3]);\n"
            f"        p[0] += 0x34215687;\np[1]+=0x90875643;\np[2]+=0x78965031;\np[3]+=67941304;\n"
            f"        printf(\"%\" WORD_OUT_TYPE \" %\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE "
            f"\"\\n\", p[0], p[1],p[2],p[3]);\n "
            f"    }}\n"
            f"}}\n"
        )

    def setKey(self,key):
        self.key=key

    def _matrices(self, matrices):
        s = "uint8_t MATRICES[ROUNDS + 1][BLOCK_SIZE][BLOCK_SIZE] = {\n"
        for k, matrix in enumerate(matrices):
            s += "    {\n"
            for i in range(192):
                s += "        {"
                for j in range(192):
                    s += str(matrix[i][j])
                    if j + 1 < 192:
                        s += ", "
                s += "}"
                if i + 1 < 192:
                    s += ","
                s += "\n"
            s += "    }"
            if k + 1 < 33:
                s += ","
            s += "\n"
        s += "};\n"
        return s

    def _vectors(self, vectors):
        s = "uint8_t VECTORS[ROUNDS + 1][BLOCK_SIZE] = {\n"
        for k, vector in enumerate(vectors):
            s += "    {"
            for i in range(len(vector)):
                s += str(vector[i])
                if i + 1 < len(vector):
                    s += ", "
            s += "}"
            if k + 1 < 33:
                s += ","
            s += "\n"
        s += "};\n"
        return s

    def generate_code(self, matrices, vectors):
        assert len(matrices) > 0
        assert len(vectors) > 0
        assert len(matrices) == len(vectors)

        block_size = 192
        word_size = 32
        rounds = 32

        return self._includes() + \
            "\n" + \
            self._defines(block_size, word_size, rounds) + \
            "\n" + \
            self._matrices(matrices) + \
            "\n" + \
            self._vectors(vectors) + \
            "\n" + \
            self._functions(block_size, word_size, rounds) + \
            "\n" + \
            self._main()



def generateSM4():
        a = "#define SM4_ENCRYPT     1    \n" \
            "#define SM4_DECRYPT     0   \n" \
            "typedef struct\n" \
            "{\n" \
            "int mode;\n" \
            "unsigned long sk[32];\n" \
            "}\n" \
            "sm4_context;\n" \
            "void sm4_setkey_enc( sm4_context *ctx, unsigned char key[16] );\n" \
            "void sm4_setkey_dec( sm4_context *ctx, unsigned char key[16] );\n" \
            "void sm4_crypt_ecb( sm4_context *ctx,int mode,int length, unsigned char *input,unsigned char *output);\n"
        b='''
        #ifndef GET_ULONG_BE    
        #define GET_ULONG_BE(n,b,i)                             \\    
        {                                                       \\    
            (n) = ( (unsigned long) (b)[(i)    ] << 24 )        \\    
                | ( (unsigned long) (b)[(i) + 1] << 16 )        \\    
                | ( (unsigned long) (b)[(i) + 2] <<  8 )        \\    
                | ( (unsigned long) (b)[(i) + 3]       );       \\    
        }    
        #endif           
        #ifndef PUT_ULONG_BE    
        #define PUT_ULONG_BE(n,b,i)                             \\    
        {                                                       \\    
            (b)[(i)    ] = (unsigned char) ( (n) >> 24 );       \\   
            (b)[(i) + 1] = (unsigned char) ( (n) >> 16 );       \\    
            (b)[(i) + 2] = (unsigned char) ( (n) >>  8 );       \\    
            (b)[(i) + 3] = (unsigned char) ( (n)       );       \\    
        }    
        #endif 
        #define  SHL(x,n) (((x) & 0xFFFFFFFF) << n)    
        #define ROTL(x,n) (SHL((x),n) | ((x) >> (32 - n)))    
        #define SWAP(a,b) { unsigned long t = a; a = b; b = t; t = 0; }
        static const unsigned char SboxTable[16][16] =     
        {    
        {0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05},    
        {0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99},    
        {0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62},    
        {0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6},    
        {0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8},    
        {0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35},    
        {0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87},    
        {0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e},    
        {0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1},    
        {0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3},    
        {0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f},    
        {0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51},    
        {0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8},    
        {0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0},    
        {0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84},    
        {0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48}    
        };
        static const unsigned long FK[4] = {0xa3b1bac6,0x56aa3350,0x677d9197,0xb27022dc};
        static const unsigned long CK[32] =    
        {    
        0x00070e15,0x1c232a31,0x383f464d,0x545b6269,    
        0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,    
        0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,    
        0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,    
        0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,    
        0x30373e45,0x4c535a61,0x686f767d,0x848b9299,    
        0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,    
        0x10171e25,0x2c333a41,0x484f565d,0x646b7279    
        };
        static unsigned char sm4Sbox(unsigned char inch)    
        {    
            unsigned char *pTable = (unsigned char *)SboxTable;    
            unsigned char retVal = (unsigned char)(pTable[inch]);    
            return retVal;    
        }
        static unsigned long sm4Lt(unsigned long ka)    
        {    
            unsigned long bb = 0;    
            unsigned long c = 0;    
            unsigned char a[4];    
            unsigned char b[4];    
            PUT_ULONG_BE(ka,a,0)    
            b[0] = sm4Sbox(a[0]);    
            b[1] = sm4Sbox(a[1]);    
            b[2] = sm4Sbox(a[2]);    
            b[3] = sm4Sbox(a[3]);    
            GET_ULONG_BE(bb,b,0)    
            c =bb^(ROTL(bb, 2))^(ROTL(bb, 10))^(ROTL(bb, 18))^(ROTL(bb, 24));    
            return c;    
        }
        static unsigned long sm4F(unsigned long x0, unsigned long x1, unsigned long x2, unsigned long x3, unsigned long rk)    
        {    
            return (x0^sm4Lt(x1^x2^x3^rk));    
        }
        static unsigned long sm4CalciRK(unsigned long ka)    
        {    
            unsigned long bb = 0;    
            unsigned long rk = 0;    
            unsigned char a[4];    
            unsigned char b[4];    
            PUT_ULONG_BE(ka,a,0)    
            b[0] = sm4Sbox(a[0]);    
            b[1] = sm4Sbox(a[1]);    
            b[2] = sm4Sbox(a[2]);    
            b[3] = sm4Sbox(a[3]);    
            GET_ULONG_BE(bb,b,0)    
            rk = bb^(ROTL(bb, 13))^(ROTL(bb, 23));    
            return rk;    
        }
        static void sm4_setkey( unsigned long SK[32], unsigned char key[16] )    
        {    
            unsigned long MK[4];    
            unsigned long k[36];    
            unsigned long i = 0;    
            GET_ULONG_BE( MK[0], key, 0 );    
            GET_ULONG_BE( MK[1], key, 4 );    
            GET_ULONG_BE( MK[2], key, 8 );    
            GET_ULONG_BE( MK[3], key, 12 );    
            k[0] = MK[0]^FK[0];    
            k[1] = MK[1]^FK[1];    
            k[2] = MK[2]^FK[2];    
            k[3] = MK[3]^FK[3];    
            for(; i<32; i++)    
            {    
                k[i+4] = k[i] ^ (sm4CalciRK(k[i+1]^k[i+2]^k[i+3]^CK[i]));    
                SK[i] = k[i+4];    
            }     
        }
        static void sm4_one_round( unsigned long sk[32],    
                        unsigned char input[16],    
                        unsigned char output[16] )    
        {    
            unsigned long i = 0;    
            unsigned long ulbuf[36];    
            
            
            memset(ulbuf, 0, sizeof(ulbuf));    
            GET_ULONG_BE( ulbuf[0], input, 0 )    
            GET_ULONG_BE( ulbuf[1], input, 4 )    
            GET_ULONG_BE( ulbuf[2], input, 8 )    
            GET_ULONG_BE( ulbuf[3], input, 12 )    
            while(i<32)    
            {    
                ulbuf[i+4] = sm4F(ulbuf[i], ulbuf[i+1], ulbuf[i+2], ulbuf[i+3], sk[i]);    
                i++;    
            }    
            PUT_ULONG_BE(ulbuf[35],output,0);    
            PUT_ULONG_BE(ulbuf[34],output,4);    
            PUT_ULONG_BE(ulbuf[33],output,8);    
            PUT_ULONG_BE(ulbuf[32],output,12);    
        }
        void sm4_setkey_enc( sm4_context *ctx, unsigned char key[16] )    
        {    
            ctx->mode = SM4_ENCRYPT;    
            sm4_setkey( ctx->sk, key );    
        }
        void sm4_setkey_dec( sm4_context *ctx, unsigned char key[16] )    
        {    
            int i;    
            ctx->mode = SM4_ENCRYPT;    
            sm4_setkey( ctx->sk, key );    
            for( i = 0; i < 16; i ++ )    
            {    
                SWAP( ctx->sk[ i ], ctx->sk[ 31-i] );    
            }    
        }
        void sm4_crypt_ecb( sm4_context *ctx,    
                        int mode,    
                        int length,    
                        unsigned char *input,    
                       unsigned char *output)    
        {    
            while( length > 0 )    
            {    
                sm4_one_round( ctx->sk, input, output );    
                input  += 16;    
                output += 16;    
                length -= 16;    
            }           
        }
        '''
        return a+b

def generate_matrix():
    import random,datetime
    random.seed(datetime.datetime.now())
    m = []
    for i in range(192):
        m.append([])
        for j in range(192):
            m[i].append(random.randint(0,1))
    return m

def generate_vector():
    import random,datetime
    random.seed(datetime.datetime.now())
    v=[]
    for i in range(192):
        v.append(random.randint(0,1))
    return v



class inputReverse(CodeGenerator):
    def _functions(self, block_size, word_size, rounds):
        return self._MATRIX_VECTOR_PRODUCT + \
            "\n" + \
            self._VECTOR_ADDITION + \
            "\n" + \
            self._MODULAR_ADDITION + \
            "\n"

    def _main(self):
        return (
            f"int main(int argc, char *argv[]) {{\n"
            f"    WORD_TYPE x[4];\n"
            f"    WORD_TYPE res[4];\n"
            f"    if (argc < 3) {{\n"
            f"        return -1;\n"
            f"    }} else {{\n"
            f"        sscanf(argv[1], \"%\" WORD_IN_TYPE, &x[0]);\n"
            f"        sscanf(argv[2], \"%\" WORD_IN_TYPE, &x[1]);\n"
            f"        sscanf(argv[3], \"%\" WORD_IN_TYPE, &x[2]);\n"
            f"        sscanf(argv[4], \"%\" WORD_IN_TYPE, &x[3]);\n"
            f"        x[0] += 0x34215687;\nx[1]+=0x90875643;\nx[2]+=0x78965031;\nx[3]+=67941304;\n"
            f"        printf(\"%\" WORD_OUT_TYPE \" %\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE "
            f"\"\\n\", x[0], x[1],x[2],x[3]);\n "
            f"    }}\n"
            f"}}\n"
        )

    def generate_code_inverse_input_external_encoding(self):
        matrix=generate_matrix()
        vector=generate_vector()
        return self.generate_code([matrix], [vector])

class outputRevrse(CodeGenerator):
    def _functions(self, block_size, word_size, rounds):
        return self._MATRIX_VECTOR_PRODUCT + \
               "\n" + \
               self._VECTOR_ADDITION + \
               "\n" + \
               self._MODULAR_ADDITION + \
               "\n" + \
               generateSM4()

    def _main(self):
        return (
            f"int main(int argc, char *argv[]) {{\n"
            f"    WORD_TYPE x[4];\n"
            f"    WORD_TYPE res[2];\n"
            f"    if (argc < 3) {{\n"
            f"        return -1;\n"
            f"    }} else {{\n"
            f"        sscanf(argv[1], \"%\" WORD_IN_TYPE, &x[0]);\n"
            f"        sscanf(argv[2], \"%\" WORD_IN_TYPE, &x[1]);\n"
            f"        sscanf(argv[3], \"%\" WORD_IN_TYPE, &x[2]);\n"
            f"        sscanf(argv[4], \"%\" WORD_IN_TYPE, &x[3]);\n"
            f"        x[0] += 0x3ff15687;\nx[1]+=0x90875fe3;\nx[2]+=0x78f65e31;\nx[3]+=0x6fe41104;\n"
            f"        printf(\"%\" WORD_OUT_TYPE \" %\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE \"%\" WORD_OUT_TYPE "
            f"\"\\n\", x[0], x[1],x[2],x[3]);\n "
            f"    }}\n"
            f"}}\n"
        )

    def generate_code_inverse_output_external_encoding(self):
        matrix = generate_matrix()
        vector = generate_vector()
        return self.generate_code([matrix], [vector])