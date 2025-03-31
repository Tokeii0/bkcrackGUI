from PySide6 import QtCore
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QComboBox
from ui.Ui_main import Ui_Form
import subprocess
import sys
import threading

# 创建一个工作线程类用于执行耗时操作
class WorkerThread(QThread):
    # 定义信号
    resultReady = Signal(str)
    progressUpdate = Signal(str)  # 新增进度更新信号
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None
        self.terminated = False
        
    def run(self):
        try:
            # 使用Popen代替run，以便能够实时获取输出
            self.process = subprocess.Popen(
                self.command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True
            )
            
            # 收集完整输出
            full_output = []
            
            # 读取输出并发送进度更新信号
            for line in iter(self.process.stdout.readline, ''):
                if self.terminated:
                    break
                
                full_output.append(line)
                self.progressUpdate.emit(line)
            
            # 等待进程完成
            self.process.wait()
            
            # 发送完整结果
            self.resultReady.emit(''.join(full_output))
            
        except Exception as e:
            self.progressUpdate.emit(f"执行出错: {str(e)}")
            self.resultReady.emit(f"执行出错: {str(e)}")
    
    def terminate(self):
        self.terminated = True
        if self.process:
            self.process.terminate()
        super().terminate()

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.compressedZipPath = ''  # 用于存储被加密的压缩包路径
        self.plainFilePath = ''  # 用于存储明文路径
        self.bind()
        # 初始化线程变量
        self.worker_thread = None

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
        # 禁用按钮，防止重复点击
        self.CompressedZipInfo.setEnabled(False)
        self.OutPutArea.setPlainText("正在获取压缩包信息，请稍候...")
        
        # "bkcrack.exe -L " + self.ViewCompressedZip.toPlainText()
        command = ["bkcrack.exe", "-L", self.ViewCompressedZip.toPlainText()]
        print(command)
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleZipInfoResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()

    def updateProgress(self, line):
        # 追加新的进度信息到输出区域
        current_text = self.OutPutArea.toPlainText()
        self.OutPutArea.setPlainText(current_text + line)
        # 滚动到底部
        self.OutPutArea.verticalScrollBar().setValue(self.OutPutArea.verticalScrollBar().maximum())

    def handleZipInfoResult(self, output):
        # 重新启用按钮
        self.CompressedZipInfo.setEnabled(True)
        
        # 从输出中提取文件名
        if output:
            # 清空下拉框
            self.PlainName.clear()
            
            # 按行分割输出
            lines = output.split('\n')
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
            
        # 禁用开始攻击按钮，防止重复点击
        self.StartAttack.setEnabled(False)
        self.OutPutArea.setPlainText("正在进行攻击，请稍候...\n这可能需要一些时间，请耐心等待。\n\n")
        
        # "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -p " + self.ViewPlainFile.toPlainText()
        command = ["bkcrack.exe", "-C", self.ViewCompressedZip.toPlainText(), "-c", plainname, "-p", self.ViewPlainFile.toPlainText()]
        print(command)
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleAttackResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()

    def handleAttackResult(self, output):
        # 重新启用按钮
        self.StartAttack.setEnabled(True)
        
        # 如果输出中包含密钥信息，自动提取并填入密钥输入框
        if "keys: " in output.lower() or "Keys: " in output:
            # 查找密钥行
            lines = output.split('\n')
            for line in lines:
                # 不区分大小写搜索"keys:"
                if "keys:" in line.lower():
                    # 提取密钥，支持不同格式的输出
                    keys_part = line.split(":", 1)[1].strip()
                    self.InputKey.setPlainText(keys_part)
                    # 添加提示信息
                    self.OutPutArea.setPlainText(self.OutPutArea.toPlainText() + "\n已自动提取密钥并填入密钥输入框！")
                    break

    def DoExportZip(self):
        key = self.InputKey.toPlainText()
        if not key:
            self.OutPutArea.setPlainText("请先输入密钥")
            return
        plainname = self.PlainName.currentText()
        if not plainname:
            self.OutPutArea.setPlainText("请先选择明文文件名称")
            return
            
        # 禁用导出按钮，防止重复点击
        self.ExportZip.setEnabled(False)
        self.OutPutArea.setPlainText("正在导出无密码压缩包，请稍候...\n\n")
        
        # 处理密钥字符串，将其拆分为三个单独的参数
        key_parts = key.strip().split()
        if len(key_parts) != 3:
            self.OutPutArea.setPlainText(f"密钥格式错误！应为三个32位整数，例如：be056038 0a143c0c 1ea08ca5\n当前输入：{key}")
            self.ExportZip.setEnabled(True)
            return
        
        # "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -k " + key_parts[0] + " " + key_parts[1] + " " + key_parts[2] + " -D " + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip"
        command = ["bkcrack.exe", "-C", self.ViewCompressedZip.toPlainText(), "-c", plainname, "-k", 
                  key_parts[0], key_parts[1], key_parts[2], 
                  "-D", self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip"]
        print(command)
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleExportResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()

    def handleExportResult(self, output):
        # 重新启用按钮
        self.ExportZip.setEnabled(True)
        # 使用setPlainText而不是appendPlainText
        self.OutPutArea.setPlainText(output + '\n' + "导出成功！无密码压缩包路径：" + self.ViewCompressedZip.toPlainText() + "_NO_PASS.zip")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
