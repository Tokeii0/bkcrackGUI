from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from ui.Ui_main import Ui_Form
import subprocess
import sys

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.compressedZipPath = ''  # 用于存储被加密的压缩包路径
        self.plainFilePath = ''  # 用于存储明文路径
        self.bind()

    def bind(self):
        # 选择被加密的压缩包
        self.SelectCompressedFile.clicked.connect(lambda: self.UpdateCompressedFilePath(str(QFileDialog.getOpenFileName(self, "请选择被加密的压缩包", "", "Zip Files (*.zip)")[0])))
        # 查看被加密的压缩包信息
        self.CompressedZipInfo.clicked.connect(self.GetCompressedZipInfo)
        # 选择明文路径
        self.SelectPlainFile.clicked.connect(lambda: self.UpdatePlainFilePath(str(QFileDialog.getOpenFileName(self, "请选择明文路径", "")[0])))
        self.StartAttack.clicked.connect(self.Attak)
        self.ExportZip.clicked.connect(self.DoExportZip)
    
    def UpdatePlainFilePath(self, path):
        self.plainFilePath = path
        self.ViewPlainFile.setPlainText(path)
    
    def UpdateCompressedFilePath(self, path):
        self.compressedZipPath = path
        self.ViewCompressedZip.setPlainText(path)

    def GetCompressedZipInfo(self):
        command = "bkcrack.exe -L " + self.ViewCompressedZip.toPlainText()
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
        self.OutPutArea.setPlainText(result.stdout)

    def Attak(self):
        plainname = self.PlainName.toPlainText()
        if not plainname:
            self.OutPutArea.setPlainText("请先输入明文文件名称")
            return
        command = "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -p " + self.ViewPlainFile.toPlainText()
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.OutPutArea.setPlainText(result.stdout)

    def DoExportZip(self):
        key = self.InputKey.toPlainText()
        if not key:
            self.OutPutArea.setPlainText("请先输入密钥")
            return
        plainname = self.PlainName.toPlainText()
        if not plainname:
            self.OutPutArea.setPlainText("请先输入明文文件名称")
            return
        command = "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -k " + key + " -D " + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip"
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
        self.OutPutArea.setPlainText(result.stdout + '\n' + "导出成功！无密码压缩包路径：" + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()