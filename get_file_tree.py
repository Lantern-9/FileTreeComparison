# 获取本地指定文件夹下的文件树
# 空文件夹不会过掉

import os
import csv
from collections import defaultdict


def analyze_directory(target_path, output_csv='folder_report.csv'):
    """
    将本地指定文件夹的文件树写入csv
    """
    # 用于存储每个文件夹的统计数据（总大小和文件总数）
    folder_stats = defaultdict(lambda: {'size_kb': 0.0, 'file_count': 0})
    # 用于存储每个具体文件的详细信息
    file_details = []

    # 遍历目录树
    try:
        if not os.path.exists(target_path):
            raise Exception("路径不存在")

        for root, dirs, files in os.walk(target_path):
            if root != target_path:
                temp_path = os.path.split(root)
                file_details.append({
                    '所在文件夹': temp_path[0],
                    '文件名': temp_path[1],
                    '文件大小(KB)': 0
                })
            for file in files:
                file_path = os.path.join(root, file)
                # 获取文件大小（字节），并转换为 KB
                file_size_bytes = os.path.getsize(file_path)
                file_size_kb = file_size_bytes / 1024

                # 累加到当前文件夹的统计中
                folder_stats[root]['size_kb'] += file_size_kb
                folder_stats[root]['file_count'] += 1

                # 将当前文件的详细信息添加到列表中
                file_details.append({
                    '所在文件夹': root,
                    '文件名': file,
                    '文件大小(KB)': round(file_size_kb, 2)
                })

            # 确保空的子文件夹也会出现在统计中
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_path not in folder_stats:
                    folder_stats[dir_path] = {'size_kb': 0.0, 'file_count': 0}

    except Exception as e:
        raise Exception(e) from e

    # 导出为 CSV 文件
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 修改表头：增加了文件名相关的列
            fieldnames = ['所在文件夹', '文件名', '文件大小(KB)', '文件夹总大小(KB)', '文件夹文件总数']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # 遍历收集到的每一个文件详情
            for detail in file_details:
                folder_path = detail['所在文件夹']
                stats = folder_stats[folder_path]
                # 写入每一行的数据：既包含当前文件的信息，也包含它所属文件夹的汇总信息
                # 且去掉指定目录
                folder_path = folder_path.replace(f'{target_path}', '')
                if folder_path:
                    writer.writerow({
                        '所在文件夹': folder_path.replace(f'{target_path}', ''),
                        '文件名': detail['文件名'],
                        '文件大小(KB)': detail['文件大小(KB)'],
                        '文件夹总大小(KB)': round(stats['size_kb'], 2),
                        '文件夹文件总数': stats['file_count']
                    })
        return f"文件树已成功导出至：{output_csv}"
    except Exception as e:
        raise Exception(e) from e


def get_file_tree(target_path):
    """
    获取本地指定文件夹的文件数，并放入列表
    """
    data = []
    try:
        for root, dirs, files in os.walk(target_path):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name).replace('\\', '/').replace(rf'{target_path}', '')
                data.append(dir_path)
                # print(dir_path)
            for file in files:
                # 排除临时文件
                if file.startswith("~$"):
                    continue
                file_path = os.path.join(root, file).replace('\\', '/').replace(rf'{target_path}', '')
                data.append(file_path)
                # print(file_path)
        return data
    except Exception as e:
        print(f"列表生成失败: {e.__traceback__.tb_lineno, e}")


if __name__ == "__main__":
    TARGET_FOLDER = input('请输入目标文件夹地址: ')

    base = get_file_tree(TARGET_FOLDER)

    # analyze_directory(TARGET_FOLDER)
