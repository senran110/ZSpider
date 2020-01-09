import logging
import multiprocessing
import os
import time
import random


def copy_file(queue, file_name, source_folder_name, dest_folder_name):
    """copy文件到指定的路径"""
    print("the file is:", file_name)
    f_read = open(source_folder_name + "/" + file_name, 'rb')
    f_write = open(dest_folder_name + '/' + file_name, 'wb')
    while True:
        time.sleep(random.random())
        content = f_read.read(1024)
        if content:
            f_write.write(content)
        else:
            break

    f_read.close()
    f_write.close()

    # 发送已经拷贝完毕的文件名字
    queue.put(file_name)


def is_file(path):
    if os.path.isdir(path):
        print("it's a directory %s" % path)
        return 1
    elif os.path.isfile(path):
        print("it's a normal file %s" % path)
        return 2
    else:
        print("it's a special file(socket,FIFO,device file) %s" % path)


def main(q, old_folder_name, store_old_name):
    try:
        new_folder_name = old_folder_name + "[复件]"
        os.mkdir(new_folder_name)
    except:
        logging.warning("创建文件出错")

    file_names = os.listdir(store_old_name)

    for file_name in file_names:
        path = os.path.join(store_old_name, file_name)
        flag = is_file(path)
        if flag == 1:
            new_path = os.path.join(new_folder_name, file_name)
            store_path = os.path.join(store_old_name, file_name)
            main(q, new_path, store_path)
        elif flag == 2:
            po.apply_async(copy_file, args=(q, file_name, store_old_name, new_folder_name))
            # 不加延时会导致复制不完全
            # time.sleep(0.1)

    # for file_name in file_names:
    #     po.apply_async(copy_file, args=(q, file_name, old_folder_name, new_folder_name))


def process(q):
    # 测一下所有文件的个数
    # all_file_num = len(file_names)
    file_names = []
    srcPath = r"C:\Users\hp\Downloads\Chaojiying_Python"
    for root, dirs, file_name in os.walk(srcPath):
        file_names = file_names + file_name
    all_file_num = len(file_names)

    copy_ok_num = 0

    while True:
        file_name = q.get()
        if file_name in file_names:
            file_names.remove(file_name)
        # copy_rate = (all_file_num-len(file_names))*100/all_file_num
        # if copy_rate >100:
        #     break
        copy_ok_num += 1
        print("\r拷贝进度为:%.2f %%" % (copy_ok_num * 100 / all_file_num), end="")
        if copy_ok_num >= all_file_num:
            break


if __name__ == '__main__':
    # 获取要复制的文件夹C:\Users\hp\Downloads\Chaojiying_Python
    po = multiprocessing.Pool(5)
    q = multiprocessing.Manager().Queue()
    old_folder_name = input("请输入要copy的文件夹的名字:")
    main(q, old_folder_name, old_folder_name)
    po.close()
    process(q)

    # 直接拷贝目录
    # import shutil
    # shutil.copytree(r'C:\Users\hp\Downloads\Chaojiying_Python', r'C:\Users\hp\Downloads\Chaojiying_Python2')
