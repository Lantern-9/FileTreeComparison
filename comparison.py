import traceback
import logging
from get_file_tree import get_file_tree, analyze_directory
import sys
import ui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon

LOG = r'app.log'


# 封装日志查看窗口，是直接用 pyqt5 写和，没用 Designer
class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QTextBrowser()
        self.setCentralWidget(self.browser)
        self.showLog(LOG)
        self.setWindowTitle("日志查看器")
        self.setGeometry(100, 100, 800, 600)

    def showLog(self, log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            html_content = ""
            for line in lines:
                # 简单的颜色处理逻辑
                # if "ERROR" in line:
                if "DEBUG" in line:
                    html_content += f'<font color="red"><b>{line.strip()}</b></font><br>'
                elif "WARNING" in line:
                    html_content += f'<font color="orange">{line.strip()}</font><br>'
                elif "INFO" in line:
                    html_content += f'<font color="blue">{line.strip()}</font><br>'
                else:
                    html_content += f"{line.strip()}<br>"

            # 页面渲染
            self.browser.setHtml(html_content)

            # 让日志滑到最底，直接显示最新的
            # 1. 获取光标
            cursor = self.browser.textCursor()
            # 2. 移动光标到文档末尾
            cursor.movePosition(cursor.End)
            # 3. 设置光标并确保可见（这会自动触发滚动到底部）
            self.browser.setTextCursor(cursor)
            self.browser.ensureCursorVisible()
        except Exception as e:
            self.browser.setPlainText(f"读取日志失败: {e}")


# 主窗口，ui.py 是 Designer 完成设计后的 ui 文件生成的
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_viewer = None
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # 关联信号与槽
        self.ui.pushButton.clicked.connect(self.onClick_csvButton)
        self.ui.pushButton_2.clicked.connect(self.onClick_csvButton_2)
        self.ui.pushButton_4.clicked.connect(self.showLogWindow)
        self.ui.pushButton_3.clicked.connect(self.onClick_compareButton)

    def addEcho(self, text):
        self.ui.textBrowser.append(text)

    def setEcho(self, text):
        self.ui.textBrowser.setPlainText(text)

    def showLogWindow(self):
        # 调日志查看窗口
        self.log_viewer = LogViewer()
        self.log_viewer.show()

    def onClick_csvButton_2(self):
        """
        导出csv被点击_第二行
        """
        if content_2 := self.ui.lineEdit_2.text():
            try:
                file_path = self.save_file()
                if file_path:
                    result = analyze_directory(content_2, file_path)
                    self.addEcho(result)
            except Exception as e:
                error = traceback.format_exc()
                logging.debug(error)
                QMessageBox.warning(self, '警告', str(e), QMessageBox.Ok)
                self.setEcho(str(e))
        else:
            # 弹窗提示路径为空
            QMessageBox.warning(self, '警告', '路径为空', QMessageBox.Ok)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",  # 对话框标题
            "文件树导出.csv",  # 默认文件名
            "所有文件 (*);;文本文件 (*.csv)"  # 文件类型过滤器
        )
        if file_path:  # 用户点击了保存
            return file_path

    def onClick_csvButton(self):
        """
        导出csv被点击_第一行
        """
        if content_1 := self.ui.lineEdit.text():
            try:
                file_path = self.save_file()
                if file_path:
                    result = analyze_directory(content_1, file_path)
                    self.addEcho(result)
            except Exception as e:
                error = traceback.format_exc()
                logging.debug(error)
                QMessageBox.warning(self, '警告', str(e), QMessageBox.Ok)
                self.setEcho(str(e))
        else:
            # 弹窗提示路径为空
            QMessageBox.warning(self, '警告', '路径为空', QMessageBox.Ok)

    def compareSets(self, set_1, set_2):
        contain_1 = set_1 - set_2
        contain_2 = set_2 - set_1
        if contain_1:
            self.addEcho(f"仅在 文件树1 存在的文件:")
            for c1 in contain_1:
                self.addEcho(f"    {c1}")
        if contain_2:
            self.addEcho(f"仅在 文件树2 存在的文件:")
            for c2 in contain_2:
                self.addEcho(f"    {c2}")

    def comparison(self, set_1, set_2):
        len_1 = len(set_1)
        len_2 = len(set_2)

        if len_1 == len_2:
            if set_1 == set_2:
                self.addEcho(f'均有{len_1}条数据，且完全相同')
            else:
                self.addEcho('数量相同，文件不同如下：')
                self.compareSets(set_1, set_2)
        else:
            self.addEcho(f'文件数量不等，分别是:  文件树1 - {len_1}条,  文件树2 - {len_2}条')
            self.compareSets(set_1, set_2)

    def onClick_compareButton(self):
        self.setEcho('')
        target_1 = self.ui.lineEdit.text()
        target_2 = self.ui.lineEdit_2.text()
        if not (target_1 and target_2):
            QMessageBox.warning(self, "提示", "输入为空")
            return

        set_1 = set(get_file_tree(target_1))
        set_2 = set(get_file_tree(target_2))

        # 执行对比
        if set_1 is not None and set_2 is not None:
            self.comparison(set_1, set_2)
        else:
            QMessageBox.warning(self, "错误", "无法获取数据，请检查路径配置")


if __name__ == '__main__':
    # 配置logging
    logging.basicConfig(
        level=logging.DEBUG,  # 设置最低日志级别
        format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
        filename='app.log',  # 指定输出到文件，如果不指定则输出到控制台,
        encoding='utf-8'
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'img/tree.png'))
    main_window = MainWindow()  # 实例化自己的主窗口类
    main_window.show()
    sys.exit(app.exec_())

