from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox
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
        self.StartAttack.clicked.connect(self.Attack)
        self.ExportZip.clicked.connect(self.DoExportZip)
    
    def UpdatePlainFilePath(self, path):
        self.plainFilePath = path
        self.ViewPlainFile.setPlainText(path)
    
    def UpdateCompressedFilePath(self, path):
        self.compressedZipPath = path
        self.ViewCompressedZip.setPlainText(path)
        # 清空文件名下拉框
        self.PlainName.clear()

    def GetCompressedZipInfo(self):
        # "bkcrack.exe -L " + self.ViewCompressedZip.toPlainText()
        command = ["bkcrack.exe", "-L", self.ViewCompressedZip.toPlainText()]
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
        self.OutPutArea.setPlainText(result.stdout)
        
        # 从输出中提取文件名
        if result.stdout:
            # 清空下拉框
            self.PlainName.clear()
            
            # 按行分割输出
            lines = result.stdout.split('\n')
            filenames = []
            for line in lines:
                # 跳过标题行和空行
                if not line.strip() or "Index Encryption" in line or "-----" in line:
                    continue
                # 检查是否是文件信息行
                parts = line.strip().split()
                if len(parts) >= 7:  # 确保行有足够的部分
                    # 最后一个部分是文件名
                    filename = parts[-1]
                    filenames.append(filename)
            
            # 如果找到了文件名，添加到下拉框中
            if filenames:
                self.PlainName.addItems(filenames)
                # 选择第一个文件
                self.PlainName.setCurrentIndex(0)

    def Attack(self):
        plainname = self.PlainName.currentText()
        if not plainname:
            self.OutPutArea.setPlainText("请先选择明文文件名称")
            return
        # "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -p " + self.ViewPlainFile.toPlainText()
        command = ["bkcrack.exe", "-C", self.ViewCompressedZip.toPlainText(), "-c", plainname, "-p", self.ViewPlainFile.toPlainText()]
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        self.OutPutArea.setPlainText(result.stdout)

    def DoExportZip(self):
        key = self.InputKey.toPlainText()
        if not key:
            self.OutPutArea.setPlainText("请先输入密钥")
            return
        plainname = self.PlainName.currentText()
        if not plainname:
            self.OutPutArea.setPlainText("请先选择明文文件名称")
            return
        # "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -k " + key + " -D " + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip"
        command = ["bkcrack.exe", "-C", self.ViewCompressedZip.toPlainText(), "-c", plainname, "-k", key, "-D", self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip"]
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
        self.OutPutArea.setPlainText(result.stdout + '\n' + "导出成功！无密码压缩包路径：" + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
