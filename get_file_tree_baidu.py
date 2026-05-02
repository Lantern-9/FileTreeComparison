# 获取百度网盘文件树

import csv
from pathlib import Path


def baidu_directory(baidu_output, target_file, output_csv='folder_report_baidu.csv'):
    data = []
    with open(baidu_output, 'r', encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
        for line in lines:
            data.append(line)

    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # 修改表头：增加了文件名相关的列
        fieldnames = ['所在文件夹', '文件名']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in data:
            line = line.replace(target_file, '')
            if line:
                path = Path(line)
                if str(path.parent) != '\\':
                    # 直接获取文件名和父目录写入csv
                    writer.writerow({
                        '所在文件夹': path.parent,
                        '文件名': path.name,
                    })
    print(f"百度网盘文件树已成功导出至：{output_csv}")


if __name__ == '__main__':
    # 获取百度网盘导出的文件路径
    txt = input("请输入百度网盘导出的txt文本路径: ")
    target = input("请输入百度网盘里指定的文件夹路径: ")

    baidu_directory(txt, target)


