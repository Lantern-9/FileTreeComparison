from get_file_tree import get_file_tree
from get_file_tree_baidu import get_file_tree_baidu
import sys
import ui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # 关联信号与槽
        self.ui.pushButton.clicked.connect(self.onClick_csvButton)
        self.ui.comboBox.currentIndexChanged.connect(self.onChange_srcComboBox)

    def onClick_csvButton(self):
        """
        导出csv被点击
        """
        ...

    def onChange_srcComboBox(self):
        """
        文件源选择发生变化
        """
        ...



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r'img/tree.png'))
    main_window = MainWindow()  # 实例化自己的主窗口类
    main_window.show()
    sys.exit(app.exec_())

    folder_1 = '本地'
    folder_2 = '百度网盘'

    source_1 = ''
    target_1 = input('请输入目标文件夹地址: ')

    source_2 = input("请输入百度网盘导出的txt文本路径: ")
    target_2 = input("请输入百度网盘里指定的文件夹路径: ")

    data_1 = set(get_file_tree(target_1))
    data_2 = set(get_file_tree_baidu(source_2, target_2))

    len_1 = len(data_1)
    len_2 = len(data_2)

    if len_1 == len_2:
        if data_1 == data_2:
            print(f'完全相同，均有{len_1}条数据')
        else:
            print('数量相同，文件不同如下：')
            contain = comparison(data_1, data_2)
            if contain[0]:
                print(f"仅在{folder_1}存在的文件: {contain[0]}")
            if contain[1]:
                print(f"仅在{folder_2}存在的文件: {contain[1]}")
    else:
        print(f'文件数量不等，分别是: {folder_1}-{len_1}条, {folder_2}-{len_2}条')
        contain = comparison(data_1, data_2)
        if contain[0]:
            print(f"仅在{folder_1}存在的文件: {contain[0]}")
        if contain[1]:
            print(f"仅在{folder_2}存在的文件: {contain[1]}")

