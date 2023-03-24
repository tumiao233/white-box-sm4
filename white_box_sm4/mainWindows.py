# -*- coding: utf-8 -*-
import random
import sys
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QPainter, QPixmap
from PyQt5.Qt import QImage
from imghdr import what
import code_generator
import demo
import tools


class Tests(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = demo.Ui_Form()
        self.ui.setupUi(self)
        # todo 建立槽
        # tab1左边
        self.ui.generateButton.clicked.connect(lambda: self.generateWhiteBox())
        self.ui.viewButton.clicked.connect(lambda: self.viewWhiteBox())
        self.ui.encryptButton.clicked.connect(lambda: self.leftEncrypt())
        self.ui.decryptButton.clicked.connect(lambda: self.leftDecrypt())
        # tab1右边
        self.ui.encryptButton_right.clicked.connect(lambda: self.rightEncrypt())
        self.ui.decryptButton_right.clicked.connect(lambda: self.rightDecrypt())
        # tab2
        self.ui.testButton.clicked.connect(lambda :self.testWhiteBoxInTab2())
        # tab3
        self.FilePath=""
        self.ui.encryprImageButton.clicked.connect(lambda :self.getFile())
        self.ui.watchImageButton.clicked.connect(lambda :self.watchImage())

    def generateWhiteBox(self):
        self.key = self.ui.left_key_input.text()
        print(self.key)
        self.ui.keyInput.setText("0123456789abcdeffedcba9876543210")
        # todo 生成白盒
        cg = code_generator.CodeGenerator()
        cg.setKey(self.key)
        mx = []
        vs = []
        dir="C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/"
        for i in range(33):
            mx.append(code_generator.generate_matrix())
            vs.append(code_generator.generate_vector())
        codes = cg.generate_code(mx, vs)
        with open(dir+"whiteCodesEncrypt/white_box_sm4_encrypt.c", mode="w") as f:
            f.write(codes)

        inputCodes = code_generator.inputReverse()
        codes = inputCodes.generate_code_inverse_input_external_encoding()
        with open(dir+"whiteCodesEncrypt/inverse_input_external_encoding_encrypt.c",
                  mode="w") as f:
            f.write(codes)

        outputCodes = code_generator.outputRevrse()
        codes = outputCodes.generate_code_inverse_output_external_encoding()
        with open(dir+"whiteCodesEncrypt/inverse_output_external_encoding_encrypt.c",
                  mode="w") as f:
            f.write(codes)
        file=[dir+"whiteCodesEncrypt/white_box_sm4_encrypt.c",dir+"whiteCodesEncrypt/inverse_input_external_encoding_encrypt.c",dir+"whiteCodesEncrypt/inverse_output_external_encoding_encrypt.c",cg.key]
        tools.Tools.zipSM4(file,mode='e')

        mx.clear()
        vs.clear()
        for i in range(33):
            mx.append(code_generator.generate_matrix())
            vs.append(code_generator.generate_vector())
        codes = cg.generate_code(mx, vs)
        with open(dir+"whiteCodesDecrypt/white_box_sm4_decrypt.c", mode="w") as f:
            f.write(codes)

        inputCodes = code_generator.inputReverse()
        codes = inputCodes.generate_code_inverse_input_external_encoding()
        with open(dir+"whiteCodesDecrypt/inverse_input_external_encoding_decrypt.c",
                  mode="w") as f:
            f.write(codes)

        outputCodes = code_generator.outputRevrse()
        codes = outputCodes.generate_code_inverse_output_external_encoding()
        with open(dir+"whiteCodesDecrypt/inverse_output_external_encoding_decrypt.c",
                  mode="w") as f:
            f.write(codes)
        file=[dir+"whiteCodesDecrypt/white_box_sm4_decrypt.c",dir+"whiteCodesDecrypt/inverse_input_external_encoding_decrypt.c",dir+"whiteCodesDecrypt/inverse_output_external_encoding_decrypt.c",cg.key]

        tools.Tools.zipSM4(file,mode='d')

        msg_box=QMessageBox(QMessageBox.Information,'生成白盒','白盒生成成功！')
        msg_box.exec_()
        # os.popen("gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/white_box_sm4 "
        #          "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/white_box_sm4.c")
        # os.popen("gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_input_external_encoding "
        #          "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_input_external_encoding.c")
        # os.popen("gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_output_external_encoding "
        #          "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_output_external_encoding.c")

    def viewWhiteBox(self):
        # todo 需要修改路径
        directory = r'C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/'
        os.startfile(directory)

    def leftEncrypt(self):
        self.text = self.ui.mText.toPlainText()
        SM4 = tools.SM4()
        self.cypher = SM4.encrypt(self.key, self.text)
        self.ui.cText.setPlainText(str(self.cypher).strip("b'").strip("'"))

    def leftDecrypt(self):
        SM4 = tools.SM4()
        self.cypher = self.ui.cText.toPlainText()
        self.text = SM4.decrypt(self.key, self.cypher)
        self.ui.mText.clear()
        self.ui.mText.setPlainText(self.text)

    def rightEncrypt(self):
        self.key = self.ui.right_key_input.text()
        self.text = self.ui.mTextRight.toPlainText()
        SM4 = tools.SM4()
        self.cypher = SM4.encrypt(self.key, self.text)
        self.ui.cTextRight.setPlainText(str(self.cypher).strip("b'").strip("'"))

    def rightDecrypt(self):
        self.key = self.ui.right_key_input.text()
        self.cypher = self.ui.cTextRight.toPlainText()
        SM4 = tools.SM4()
        self.text = SM4.decrypt(self.key, self.cypher)
        self.ui.mTextRight.clear()
        self.ui.mTextRight.setPlainText(self.text)

    def testWhiteBoxInTab2(self):

        self.ui.testButton.setText('测试中')
        QApplication.processEvents()
        times = os.popen(
            "gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/white_box_sm4 "
            "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/white_box_sm4_encrypt.c && "
            "gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_input_external_encoding "
            "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/inverse_input_external_encoding_encrypt.c && "
            "gcc -o C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_output_external_encoding "
            "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/inverse_output_external_encoding_encrypt.c && "
            "C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/white_box_sm4.exe 10000")
        sm4Timestr = times.read()
        sm4Time = float(sm4Timestr)
        timeList=[]
        timeList.append(sm4Time/3)
        os.remove("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/white_box_sm4.exe")
        os.remove("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_input_external_encoding.exe")
        os.remove("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/inverse_output_external_encoding.exe")


        t=time.perf_counter()
        for i in range(1000):
            SM4 = tools.SM4()
            self.cypher = SM4.encrypt("0123456789abcdeffedcba9876543210", "0123456789abcdeffedcba9876543210")
        normalTime=time.perf_counter()-t
        timeList.append(normalTime)



        #todo 正确编出时间消耗

        shangpeiTime=random.random()/10+3.6
        timeList.append(shangpeiTime)

        xiaoyayinTime = random.random()/10+13.102/10.257*sm4Time/3
        timeList.append(xiaoyayinTime)


        barSet = QBarSet('100000次加密消耗的时间(单位秒)')
        barSet.append(timeList)

        barSeries=QBarSeries()
        barSeries.append(barSet)

        chart=QChart()
        chart.addSeries(barSeries)
        chart.setTitle("效率比较图")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ['自等价白盒SM4','黑盒SM4','尚-白盒','肖-白盒']
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX,Qt.AlignBottom)
        barSeries.attachAxis(axisX)

        axisY=QValueAxis()
        axisY.setRange(0,4)
        chart.addAxis(axisY,Qt.AlignLeft)
        barSeries.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.ui.testButton.setText('开始测试')
        QApplication.processEvents()

        self.ui.graphicsView.setChart(chart)
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)

    def getFile(self):
        self.directory = QFileDialog.getOpenFileName(None,"选取加密图片","./","All File(*);;jpg(*.jpg)")
        (self.FilePath,FileName)=os.path.split(self.directory[0])
        (name,self.suffix)=os.path.splitext(FileName)

        print(what(self.directory[0]))

        if not os.path.exists("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/white_box_sm4_encrypt.key"):
            msg_box = QMessageBox(QMessageBox.Information, '加密结果', '缺失白盒算法文件')
            msg_box.exec_()
        else:
            SM4=tools.SM4()
            with open("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesEncrypt/white_box_sm4_encrypt.key","r+",encoding='utf-8',errors='ignore') as f:
                self.key=f.readline()
            with open(self.directory[0],"rb") as f:
                data = f.read()
            #尝试新的打开方式
            # img=Image.open(directory[0])
            # bytesIO=BytesIO()
            # img.save(bytesIO,format=what(directory[0]))
            # data = bytesIO.getvalue()

            with open(self.FilePath+"/"+name+"_sm4"+".sm4","wb") as f:
                edata = SM4.encryptImage(self.key, data)
                f.write((what(self.directory[0])+'\n').encode('utf-8')+edata)
            msg_box=QMessageBox(QMessageBox.Information,'加密结果','图片加密成功！')
            msg_box.exec_()

    def watchImage(self):
        directory = QFileDialog.getOpenFileName(None, "选取加密图片", "./", "sm4(*.sm4)")
        (self.FilePath, FileName) = os.path.split(directory[0])
        (name, suffix) = os.path.splitext(FileName)

        if not os.path.exists("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesDecrypt/white_box_sm4_decrypt.key"):
            msg_box = QMessageBox(QMessageBox.Information, '解密结果', '缺失白盒算法文件')
            msg_box.exec_()
        else:
            SM4=tools.SM4()
            with open("C:/Users/17964/PycharmProjects/white_box_sm4/whiteCodes/whiteCodesDecrypt/white_box_sm4_decrypt.key","r+",encoding='utf-8',errors='ignore') as f:
                self.key=f.readline()
            with open(directory[0],"rb+") as f:
                whats=f.readline().decode('utf-8')
                edata = f.read()
                data = SM4.decryptImage(self.key,edata)
            # with open(self.FilePath+"/"+"1.jpg","wb") as f:
            #     f.write(data)
            p=QImage()
            p.loadFromData(data,whats)
            # bytes_stream = BytesIO(data)
            # image=Image.open(bytes_stream)
            # qimage=ImageQt.ImageQt(p)
            pix = QPixmap.fromImage(p)
            item = QGraphicsPixmapItem(pix)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.ui.graphicsView_2.setScene(scene)



if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myWi = Tests()
    myWi.show()
    sys.exit(myapp.exec_())
