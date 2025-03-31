from PySide6 import QtCore
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from ui.Ui_main import Ui_Form
from qfluentwidgets import ComboBox
import subprocess
import sys
import threading
import os
import logging

# 设置日志记录来捕获错误
logging.basicConfig(level=logging.ERROR)

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
        # 启用调试输出
        self.debug = True
        self.setupUi(self)
        self.compressedZipPath = ''  # 用于存储被加密的压缩包路径
        self.plainFilePath = ''  # 用于存储明文路径
        # 初始化线程变量
        self.worker_thread = None
        # 初始化明文文件下拉框
        self.initPlainFileComboBox()
        # 绑定事件处理函数
        self.bind()
        
    def log(self, message):
        """调试日志函数"""
        if self.debug:
            print(f"[DEBUG] {message}")

    def bind(self):
        # 选择被加密的压缩包
        self.SelectCompressedFile.clicked.connect(lambda: self.UpdateCompressedFilePath(str(QFileDialog.getOpenFileName(self, "请选择被加密的压缩包", "", "Zip Files (*.zip)")[0])))
        # 查看被加密的压缩包信息
        self.CompressedZipInfo.clicked.connect(self.GetCompressedZipInfo)
        # 选择明文路径
        self.SelectPlainFile.clicked.connect(self.selectCustomPlainFile)
        # 明文文件下拉框变化时更新明文路径
        self.PlainFileCombo.currentIndexChanged.connect(self.onPlainFileComboChanged)
        self.StartAttack.clicked.connect(self.Attack)
        self.ExportZip.clicked.connect(self.DoExportZip)
    
    def initPlainFileComboBox(self):
        # 创建明文文件下拉框
        self.PlainFileCombo = ComboBox(self)
        self.PlainFileCombo.setObjectName(u"PlainFileCombo")
        self.PlainFileCombo.setGeometry(self.ViewPlainFile.geometry())
        self.PlainFileCombo.setFont(self.ViewPlainFile.font())
        self.PlainFileCombo.setAutoFillBackground(False)
        self.PlainFileCombo.setStyleSheet(u"color: rgb(255, 255, 127);")
        
        # 隐藏原来的文本浏览框
        self.ViewPlainFile.hide()
        
        # 添加"选择其他文件..."选项
        self.PlainFileCombo.addItem("选择其他文件...")
        
        # 从plains文件夹加载文件
        self.loadPlainFiles()
    
    def loadPlainFiles(self):
        # 获取plains文件夹路径
        plains_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plains")
        
        # 检查文件夹是否存在
        if os.path.exists(plains_dir) and os.path.isdir(plains_dir):
            # 获取文件夹中的所有文件
            files = [f for f in os.listdir(plains_dir) if os.path.isfile(os.path.join(plains_dir, f))]
            
            # 将文件添加到下拉框，并记录文件路径
            self.plain_file_paths = {}  # 用字典存储文件名到路径的映射
            for file in files:
                file_path = os.path.join(plains_dir, file)
                self.PlainFileCombo.addItem(file)
                self.plain_file_paths[file] = file_path
                self.log(f"loadPlainFiles - 添加文件 {file} 路径 {file_path}")
    
    def onPlainFileComboChanged(self, index):
        if index == 0:  # "选择其他文件..."
            return
        
        # 获取选中文件的名称和路径
        file_name = self.PlainFileCombo.currentText()
        file_path = self.plain_file_paths.get(file_name)
        self.log(f"onPlainFileComboChanged - 选择的文件: {file_name}, 路径: {file_path}")
        if file_path:
            self.plainFilePath = file_path
            self.ViewPlainFile.setPlainText(file_path)
            self.ViewPlainFile.show()
    
    def selectCustomPlainFile(self):
        # 打开文件选择对话框
        file_path = str(QFileDialog.getOpenFileName(self, "请选择明文路径", "")[0])
        self.log(f"selectCustomPlainFile - 选择的文件路径: {file_path}")
        if file_path:
            # 更新明文路径
            self.plainFilePath = file_path
            self.ViewPlainFile.setPlainText(file_path)
            self.ViewPlainFile.show()
            # 将下拉框设置为"选择其他文件..."
            self.PlainFileCombo.setCurrentIndex(0)
    
    def UpdatePlainFilePath(self, path):
        if not path:
            return
        self.log(f"UpdatePlainFilePath - 更新路径: {path}")
        self.plainFilePath = path
        # 在下拉框下方显示选择的文件路径
        self.ViewPlainFile.setPlainText(path)
        self.ViewPlainFile.show()  # 显示路径
    
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
                # 自动匹配明文文件
                self.autoMatchPlainFile(filenames[0])

    def autoMatchPlainFile(self, filename):
        """根据压缩包中的文件名自动匹配明文文件"""
        if not filename:
            return
            
        # 获取文件扩展名
        file_ext = os.path.splitext(filename)[1].lower()
        if not file_ext:
            return
            
        # 去掉点号
        file_ext = file_ext[1:]
        
        self.log(f"autoMatchPlainFile - 文件扩展名: {file_ext}")
        
        # 在plains文件夹中查找匹配的明文文件
        for i in range(1, self.PlainFileCombo.count()):
            item_text = self.PlainFileCombo.itemText(i)
            self.log(f"autoMatchPlainFile - 检查项 {i}: {item_text}")
            if file_ext in item_text.lower():
                # 找到匹配的明文文件，选中它
                self.log(f"autoMatchPlainFile - 匹配到文件: {item_text}")
                self.PlainFileCombo.setCurrentIndex(i)
                # 获取文件路径并更新
                file_path = self.plain_file_paths.get(item_text)
                self.log(f"autoMatchPlainFile - 获取的文件路径: {file_path}")
                if file_path:
                    self.plainFilePath = file_path  # 直接设置明文路径
                    self.ViewPlainFile.setPlainText(file_path)
                    self.ViewPlainFile.show()
                    self.OutPutArea.setPlainText(self.OutPutArea.toPlainText() + f"\n已自动匹配明文文件：{item_text}")
                return
                    
        # 如果没有找到匹配的文件，提示用户
        self.OutPutArea.setPlainText(self.OutPutArea.toPlainText() + f"\n未找到匹配的明文文件，请手动选择与 {file_ext} 类型对应的明文文件。")

    def Attack(self):
        plainname = self.PlainName.currentText()
        if not plainname:
            self.OutPutArea.setPlainText("请先选择明文文件名称")
            return
        
        self.log(f"Attack - plainFilePath: {self.plainFilePath}")
        
        if not self.plainFilePath:
            self.OutPutArea.setPlainText("请先选择明文文件路径")
            return
            
        # 检查文件是否存在
        if not os.path.exists(self.plainFilePath):
            self.OutPutArea.setPlainText(f"明文文件不存在: {self.plainFilePath}")
            return
            
        # 禁用开始攻击按钮，防止重复点击
        self.StartAttack.setEnabled(False)
        self.OutPutArea.setPlainText("正在进行攻击，请稍候...\n这可能需要一些时间，请耐心等待。\n\n")
        
        # "bkcrack.exe -C " + self.ViewCompressedZip.toPlainText() + " -c " + plainname + " -p " + self.plainFilePath
        command = ["bkcrack.exe", "-C", self.ViewCompressedZip.toPlainText(), "-c", plainname, "-p", self.plainFilePath]
        print(f"执行命令: {command}")
        
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
    # 忽略libpng错误和其他图像相关警告
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    # 设置环境变量以禁用Qt的调试输出
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"
    
    app = QApplication(sys.argv)
    
    # 禁用QT的libpng错误输出
    QtCore.qInstallMessageHandler(lambda *args: None)
    
    window = MainWindow()
    window.show()
    app.exec()
