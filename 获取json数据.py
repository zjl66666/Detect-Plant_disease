import base64
import json


name = ''
# 病的基本特征及防治方法
info = """

"""
img_path_list = ['1.jpg', '2.jpg', '3.jpg']  # 相关的病害的图片路径,不要超过三张


def get_json_data(info, img_path_list):
    data = {'name': name, 'info': info, 'img': []}
    # 保存每一张图片信息
    for img_path in img_path_list:
        with open(img_path, 'rb') as f:
            img = base64.b64encode(f.read()).decode()
            data['img'].append(img)
    # 将图片数据添加到data中,展示第一张图片
    with open(f'{name}.json', 'w') as f:
        json.dump(data, f)
    print(f'保存{name}.json文件成功')


if __name__ == '__main__':
    get_json_data(info, img_path_list)
