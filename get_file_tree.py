# 获取文件树

import os
import csv
from collections import defaultdict


def analyze_directory(target_path, output_csv='folder_report.csv'):
    # 1. 用于存储每个文件夹的统计数据（总大小和文件总数）
    folder_stats = defaultdict(lambda: {'size_kb': 0.0, 'file_count': 0})
    # 2. 新增：用于存储每个具体文件的详细信息
    file_details = []

    print(f"正在扫描目录：{target_path}，请稍候...")

    # 遍历目录树
    for root, dirs, files in os.walk(target_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 获取文件大小（字节），并转换为 KB
                file_size_bytes = os.path.getsize(file_path)
                file_size_kb = file_size_bytes / 1024

                # 累加到当前文件夹的统计中
                folder_stats[root]['size_kb'] += file_size_kb
                folder_stats[root]['file_count'] += 1

                # 新增：将当前文件的详细信息添加到列表中
                file_details.append({
                    '所在文件夹': root,
                    '文件名': file,
                    '文件大小(KB)': round(file_size_kb, 2)
                })
            except Exception as e:
                print(f"无法读取文件: {file_path}, 错误: {e}")

        # 确保空的子文件夹也会出现在统计中
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if dir_path not in folder_stats:
                folder_stats[dir_path] = {'size_kb': 0.0, 'file_count': 0}

    # 导出为 CSV 文件
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 修改表头：增加了文件名相关的列
            fieldnames = ['所在文件夹', '文件名', '文件大小(KB)', '文件夹总大小(KB)', '文件夹文件总数']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            # 遍历我们收集到的每一个文件详情
            for detail in file_details:
                folder_path = detail['所在文件夹']
                stats = folder_stats[folder_path]
                # 写入每一行的数据：既包含当前文件的信息，也包含它所属文件夹的汇总信息
                writer.writerow({
                    '所在文件夹': folder_path,
                    '文件名': detail['文件名'],
                    '文件大小(KB)': detail['文件大小(KB)'],
                    '文件夹总大小(KB)': round(stats['size_kb'], 2),
                    '文件夹文件总数': stats['file_count']
                })
        print(f"✅ 统计完成！文件树报告已成功导出至：{output_csv}")
    except Exception as e:
        print(f"❌ 导出 CSV 失败: {e}")


if __name__ == "__main__":
    # 在这里替换为你想要扫描的本地文件夹路径
    TARGET_FOLDER = r"H:\核心存储"

    analyze_directory(TARGET_FOLDER)