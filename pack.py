import zipfile
import os

# 指定文件夹路径
folder_path = r'E:\之江\pick-point'

# 获取父目录
parent_dir = os.path.dirname(folder_path)

# 创建或覆盖.zip文件
with zipfile.ZipFile(os.path.join(parent_dir, 'pick-tool.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 将文件添加到.zip文件中
        for file in files:
            file_path = os.path.join(root, file)
            # 替换文件路径的前缀
            zipf.write(file_path, os.path.join('pick-tool', os.path.relpath(file_path, folder_path)))
