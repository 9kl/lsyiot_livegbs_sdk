# LiveGBS Python SDK

一个功能完整的 LiveGBS GB28181 国标流媒体服务 Python SDK，提供了完整的 API 接口封装，包括用户认证、设备管理、直播流控制、视频水印、设备控制等功能。

## 🌟 特性

- 🔐 **完整的认证管理** - 用户登录、退出、密码修改
- 📱 **设备管理** - 设备列表、设备信息、通道列表、在线统计
- 🎬 **直播流控制** - 开始/停止直播、获取多种播放格式
- 🏷️ **视频水印** - 动态添加文字水印，支持位置、颜色、大小定制
- 🎮 **设备控制** - 云台控制、焦点光圈、预置位管理、看守位设置
- 🛡️ **完善的错误处理** - 自定义异常类和详细错误信息
- 📊 **类型提示支持** - 完整的类型注解，IDE 友好
- 🧪 **经过实际验证** - 在真实 GB28181 设备上测试验证

## 📦 安装

### 使用 pip 安装（推荐）

```bash
pip install lsyiot-livegbs-sdk
```

### 从源码安装

```bash
git clone https://github.com/your-repo/lsyiot_livegbs_sdk.git
cd lsyiot_livegbs_sdk
pip install -e .
```

## 🚀 快速开始

### 基本使用

```python
from lsyiot_livegbs_sdk import LiveGBSAPI

# 创建 API 客户端
client = LiveGBSAPI('http://your-livegbs-server:port')

# 登录
login_result = client.login('username', 'password')
print(f"登录成功，URLToken: {login_result.url_token}")

# 设置认证令牌（推荐）
client.session.headers.update({"Authorization": f"Bearer {login_result.url_token}"})

# 获取设备列表
device_list = client.get_device_list()
print(f"设备数量: {device_list.device_count}")
```

### 完整示例

```python
from lsyiot_livegbs_sdk import LiveGBSAPI, StreamStartResponse
from lsyiot_livegbs_sdk.exceptions import LiveGBSError

def main():
    # 服务器配置
    server_url = "http://your-server:port"
    username = "your-username"
    password = "your-password"
    
    # 设备配置
    device_serial = "your-device-serial"
    channel = 1

    client = LiveGBSAPI(server_url)

    try:
        # 1. 用户认证
        login_result = client.login(username, password)
        client.session.headers.update({"Authorization": f"Bearer {login_result.url_token}"})
        
        # 2. 设备管理
        devices = client.get_device_list()
        if devices.device_count > 0:
            device = devices.device_list[0]
            print(f"设备: {device.name}, 在线: {device.online}")
        
        # 3. 开始直播
        stream = client.start_stream(
            serial=device_serial,
            channel=channel,
            audio="config",
            transport="UDP"
        )
        print(f"直播开始: {stream.stream_id}")
        print(f"WEBRTC播放地址: {stream.webrtc}")
        
        # 4. 设置视频水印
        client.stream_osd(
            serial=device_serial,
            code=device_serial,
            text="Live Stream",
            color="white",
            x="10", y="10", size=24
        )
        
        # 5. 云台控制
        client.ptz_control(
            serial=device_serial,
            channel=channel,
            command="left",
            speed=100
        )
        
        # 6. 停止直播
        client.stop_stream(serial=device_serial, channel=channel)
        
    except LiveGBSError as e:
        print(f"操作失败: {e}")

if __name__ == "__main__":
    main()
```

## 📖 API 文档

### 认证管理

#### 用户登录
```python
login_result = client.login(username, password, url_token_only=False, token_timeout=604800)
# 返回: LoginResponse 对象，包含 cookie_token, url_token, token_timeout 等
```

#### 退出登录
```python
logout_result = client.logout()
# 返回: ModifyPasswordResponse 对象
```

#### 修改密码
```python
modify_result = client.modify_password(old_password, new_password)
# 返回: ModifyPasswordResponse 对象
```

### 设备管理

#### 查询设备列表
```python
device_list = client.get_device_list(start=0, limit=100, q="search_keyword")
# 返回: DeviceListResponse 对象，包含设备数量和设备列表
```

#### 查询单个设备信息
```python
device_info = client.get_device_info(serial="device_serial")
# 返回: Device 对象，包含设备详细信息
```

#### 查询设备通道列表
```python
channel_list = client.get_device_channel_list(
    serial="device_serial",
    channel_type="all",
    limit=1000
)
# 返回: DeviceChannelListResponse 对象
```

#### 查询设备在线统计
```python
stats = client.get_device_online_stats()
# 返回: OnlineStatsResponse 对象
print(f"设备在线率: {stats.device_online_rate:.2%}")
```

### 直播流控制

#### 开始直播
```python
stream = client.start_stream(
    serial="device_serial",
    channel=1,                    # 通道序号
    audio="config",               # 音频设置: true/false/config
    transport="UDP",              # 传输模式: TCP/UDP/config
    streamnumber=0,               # 码流编号: 0-主码流, 1-子码流
    check_channel_status=False    # 是否检查通道状态
)
# 返回: StreamStartResponse 对象
print(f"WEBRTC: {stream.webrtc}")
print(f"FLV: {stream.flv}")
print(f"RTMP: {stream.rtmp}")
print(f"HLS: {stream.hls}")
```

#### 停止直播
```python
stop_result = client.stop_stream(
    serial="device_serial",
    channel=1,
    check_outputs=False    # 是否检查在线人数
)
# 返回: StreamStopResponse 对象
```

### 视频水印

#### 设置视频水印
```python
osd_result = client.stream_osd(
    serial="device_serial",
    code="channel_code",
    streamid="stream_id",         # 可选
    text="水印文字",
    color="white",                # 文字颜色
    border_color="black",         # 边框颜色
    x="10",                       # 水平位置
    y="10",                       # 垂直位置
    size=24                       # 字体大小
)
# 返回: StreamOSDResponse 对象
```

### 设备控制

#### 云台控制
```python
ptz_result = client.ptz_control(
    serial="device_serial",
    command="left",               # 控制指令
    channel=1,
    speed=129                     # 速度 0-255
)
# 支持的指令: left, right, up, down, upleft, upright, downleft, downright, zoomin, zoomout, stop
```

#### 焦点光圈控制
```python
fi_result = client.fi_control(
    serial="device_serial",
    command="focusnear",          # 控制指令
    channel=1,
    speed=129
)
# 支持的指令: focusnear, focusfar, irisin, irisout, stop
```

#### 预置位控制
```python
# 设置预置位
preset_result = client.preset_control(
    serial="device_serial",
    command="set",
    preset=1,                     # 预置位编号 1-255
    channel=1,
    name="重要位置"               # 预置位名称
)

# 跳转到预置位
preset_result = client.preset_control(
    serial="device_serial",
    command="goto",
    preset=1,
    channel=1
)

# 删除预置位
preset_result = client.preset_control(
    serial="device_serial",
    command="remove",
    preset=1,
    channel=1
)
```

#### 看守位控制
```python
home_result = client.home_position_control(
    serial="device_serial",
    resettime=60,                 # 自动归位时间间隔(秒)
    presetindex=1,                # 调用预置位编号
    channel=1,
    enabled=True,                 # 使能开关
    timeout=15                    # 超时时间(秒)
)
```

## 🛡️ 错误处理

SDK 提供了完善的异常处理机制：

```python
from lsyiot_livegbs_sdk.exceptions import (
    LiveGBSError,           # 基础异常类
    LiveGBSNetworkError,    # 网络错误
    LiveGBSAPIError,        # API错误
    LiveGBSParseError       # 数据解析错误
)

try:
    result = client.login(username, password)
except LiveGBSNetworkError as e:
    print(f"网络错误: {e}")
except LiveGBSAPIError as e:
    print(f"API错误: {e}, 状态码: {e.error_code}")
except LiveGBSParseError as e:
    print(f"数据解析错误: {e}")
except LiveGBSError as e:
    print(f"SDK错误: {e}")
```

## 📊 响应对象

所有 API 方法都返回相应的响应对象，包含完整的数据和便捷方法：

### LoginResponse
```python
login_result = client.login(username, password)
print(login_result.cookie_token)    # Cookie令牌
print(login_result.url_token)       # URL令牌
print(login_result.token_timeout)   # 令牌超时时间
```

### StreamStartResponse
```python
stream = client.start_stream(serial, channel)
print(stream.stream_id)             # 流ID
print(stream.webrtc)                # WEBRTC播放地址
print(stream.video_resolution)      # 视频分辨率 (属性方法)
print(stream.is_streaming)          # 是否正在直播 (属性方法)
```

### Device
```python
device = client.get_device_info(serial)
print(device.name)                  # 设备名称
print(device.online)                # 在线状态
print(device.channel_count)         # 通道数量
```

## 🔧 配置选项

### 创建客户端时的配置
```python
client = LiveGBSAPI(
    base_url='http://your-server:port',
    timeout=30,                     # 请求超时时间(秒)
    verify=True                     # 是否验证SSL证书
)
```

### 自定义请求头
```python
client.session.headers.update({
    'User-Agent': 'My-App/1.0',
    'Authorization': f'Bearer {token}'
})
```

## 📝 最佳实践

### 1. 认证管理
```python
# 推荐：使用 URLToken 进行API认证
login_result = client.login(username, password)
client.session.headers.update({"Authorization": f"Bearer {login_result.url_token}"})

# 检查令牌是否即将过期
if time.time() + 3600 > login_result.token_timeout:
    # 重新登录或刷新令牌
    login_result = client.login(username, password)
```

### 2. 设备控制
```python
# 云台控制后要及时停止
client.ptz_control(serial, "left", speed=100)
time.sleep(2)  # 转动2秒
client.ptz_control(serial, "stop")  # 停止转动

# 预置位管理
try:
    # 设置预置位
    client.preset_control(serial, "set", preset=1, name="监控点A")
    # 使用预置位
    client.preset_control(serial, "goto", preset=1)
except ValueError as e:
    print(f"预置位参数错误: {e}")
```

### 3. 直播流管理
```python
# 开始直播前检查设备状态
device = client.get_device_info(serial)
if device.online:
    stream = client.start_stream(serial, channel, check_channel_status=True)
    # 使用流...
    client.stop_stream(serial, channel)
else:
    print("设备离线，无法开始直播")
```

### 4. 错误处理和重试
```python
import time
from lsyiot_livegbs_sdk.exceptions import LiveGBSNetworkError

def robust_api_call(func, *args, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except LiveGBSNetworkError as e:
            if attempt == max_retries - 1:
                raise
            print(f"网络错误，{2**attempt}秒后重试...")
            time.sleep(2**attempt)

# 使用示例
device_list = robust_api_call(client.get_device_list)
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境设置
```bash
# 克隆项目
git clone https://github.com/9kl/lsyiot_livegbs_sdk.git
cd lsyiot_livegbs_sdk

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e .
```

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行测试
pytest tests/ -v --cov=lsyiot_livegbs_sdk
```

## 📄 许可证

本项目采用 Apache License 2.0 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 🔖 版本历史

### v1.0.0 (2025-09-22)
- ✨ 初始版本发布
- 🔐 完整的认证管理功能
- 📱 设备管理和查询功能
- 🎬 直播流控制功能
- 🏷️ 视频水印功能
- 🎮 设备控制功能（云台、焦点、预置位、看守位）
- 🛡️ 完善的错误处理和类型提示
- 📊 经过实际设备验证

## 📞 问题反馈

如果您在使用过程中遇到问题，请通过 [GitHub Issues](https://github.com/9kl/lsyiot_livegbs_sdk/issues) 提交反馈。
