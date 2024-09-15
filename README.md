# Raycast 扩展统计数据收集器

这个项目是一个 Python 脚本，用于从 Raycast API 获取扩展统计数据，并通过 Bark 服务发送加密通知。

## 功能特点

- 从 Raycast API 获取扩展数据
- 对扩展数据按下载次数进行降序排序
- 使用 AES-CBC 模式加密消息
- 通过 Bark 服务发送加密通知

## 依赖

- Python 3.x
- requests
- pycryptodome

## 安装

1. 克隆仓库：

   ```
   git clone https://github.com/elonwoo/raycast-stats-to-bark.git
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 配置

在运行脚本之前，需要设置以下环境变量：

- `DEVICE_KEY`：Bark 服务的设备密钥
- `BARK_BASE_URL`：Bark 服务的基础 URL
- `RAYCAST_API_URL`：Raycast API 的 URL
- `ICON`：通知使用的图标 URL
- `BARK_ENCRYPT_KEY`：16 字节 AES 加密密钥
- `BARK_ENCRYPT_IV`：16 字节 AES 加密初始化向量

## 使用方法

运行主脚本：

```
bash
python main.py
```

脚本将从 Raycast API 获取扩展数据，对数据进行处理，然后通过 Bark 服务发送加密通知。

## 注意事项

- 确保已正确设置所有必要的环境变量。
- 请遵守 Raycast API 的使用条款和限制。
- 定期检查 Bark 服务的文档，以了解任何可能的更改或更新。

## 贡献

欢迎提交问题和拉取请求。对于重大更改，请先开启一个问题进行讨论。

## 许可证

本项目采用 [MIT 许可证](https://choosealicense.com/licenses/mit/)。
