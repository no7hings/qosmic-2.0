# coding:utf-8
import os
import threading

# 创建一个全局列表来存储找到的文件
found_files = []
# 创建一个锁来确保线程安全
lock = threading.Lock()

def process_file(file_path):
    """处理单个文件的逻辑并将其添加到文件列表中"""
    # 使用锁来防止多个线程同时修改 found_files 列表
    with lock:
        found_files.append(file_path)
    # print("Processing file: {}".format(file_path))
    # 在这里添加你的处理逻辑


def process_directory(directory):
    """递归处理目录"""
    # 创建一个线程列表来存储所有文件和子目录处理的线程
    threads = []

    # 遍历当前目录中的文件和子目录
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            # 创建处理文件的线程
            thread = threading.Thread(target=process_file, args=(full_path,))
            thread.start()
            threads.append(thread)
        elif os.path.isdir(full_path):
            # 创建处理子目录的线程
            thread = threading.Thread(target=process_directory, args=(full_path,))
            thread.start()
            threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    root_directory = "X:/QSM_TST/Assets"
    process_directory(root_directory)

    # 打印所有找到的文件
    print("\nFound files:")
    print found_files
