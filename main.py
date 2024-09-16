"""
获取Raycast扩展统计数据并发送到Bark

这个脚本从Raycast API获取扩展数据，格式化这些数据，
然后通过Bark服务发送加密的通知。
"""

import os
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests

# 常量定义
DEVICE_KEY = os.environ.get('DEVICE_KEY')  # Bark服务的设备密钥
BARK_BASE_URL = os.environ.get('BARK_BASE_URL')  # Bark服务的基础URL
BARK_API_URL = BARK_BASE_URL + DEVICE_KEY  # 完整的Bark API URL

RAYCAST_API_URL = os.environ.get('RAYCAST_API_URL')  # Raycast API的URL，用于获取扩展信息
ICON = os.environ.get('ICON')  # 通知使用的图标URL

BARK_ENCRYPT_KEY = os.environ.get('BARK_ENCRYPT_KEY')  # 16字节AES加密密钥
BARK_ENCRYPT_IV = os.environ.get('BARK_ENCRYPT_IV')  # 16字节AES加密初始化向量

# 新增常量
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extension_data.json')

# 创建全局AES密码对象
KEY = bytes.fromhex(BARK_ENCRYPT_KEY.encode('utf-8').hex())
IV_BYTES = bytes.fromhex(BARK_ENCRYPT_IV.encode('utf-8').hex())
CIPHER = AES.new(KEY, AES.MODE_CBC, IV_BYTES)

def encrypt_message(message):
    """
    使用AES-CBC模式加密消息
    
    Args:
        message (str): 要加密的消息
    
    Returns:
        str: Base64编码的加密消息
    """
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_message = CIPHER.encrypt(padded_message)
    return base64.b64encode(encrypted_message).decode('utf-8')

def get_extension_data():
    """
    从Raycast API获取扩展数据
    
    Returns:
        list: 包含扩展名称和下载次数的字典列表，按下载次数降序排序
    """
    response = requests.get(RAYCAST_API_URL, timeout=10)
    data = response.json()

    # 使用列表推导式创建扩展数据列表
    extensions = [
        {'name': ext['name'], 'download_count': int(ext['download_count'])}
        for ext in data['data']
    ]


    # 按下载次数降序排序
    return sorted(
        extensions,
        key=lambda x: x['download_count'],
        reverse=True
    )

def load_previous_data():
    """
    从文件加载之前保存的扩展数据
    
    Returns:
        dict: 包含扩展名称和下载次数的字典
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_current_data(data):
    """
    将当前扩展数据保存到文件
    
    Args:
        data (list): 扩展数据列表
    """
    data_dict = {ext['name']: ext['download_count'] for ext in data}
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f)

def format_message(data, prev_data):
    """
    格式化扩展数据为可读的消息字符串，并显示下载量的增加
    
    Args:
        data (list): 当前扩展数据列表
        prev_data (dict): 之前保存的扩展数据
    
    Returns:
        str: 格式化后的消息字符串
    """
    text = []
    for index, extension in enumerate(data, start=1):
        name = extension['name']
        current_count = extension['download_count']
        previous_count = prev_data.get(name, current_count)
        increase = current_count - previous_count
        
        if increase > 0:
            text.append(f"{index}. {name}: {current_count} | +{increase}")
        else:
            text.append(f"{index}. {name}: {current_count}")
    
    formatted_text = "\n".join(text)
    return formatted_text

def send_to_bark(current_data, prev_data):
    """
    将Raycast扩展统计数据发送到Bark
    
    Args:
        current_data (list): 当扩展数据列表
        prev_data (dict): 之前保存的扩展数据
    """
    payload = {
        "body": format_message(current_data, prev_data),
        "title": "Raycast Extension Stats",
        "icon": ICON,
        "group": "Raycast统计",
        "isArchive": "1"
    }
    params = {
        "ciphertext": encrypt_message(json.dumps(payload)),
        "iv": BARK_ENCRYPT_IV
    }
    response = requests.post(BARK_API_URL, params=params, timeout=10)
    print(f"发送{'成功' if response.status_code == 200 else '失败'}: {response.status_code}")
    if response.status_code != 200:
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    previous_data = load_previous_data()
    extension_data = get_extension_data()
    send_to_bark(extension_data, previous_data)
    save_current_data(extension_data)
