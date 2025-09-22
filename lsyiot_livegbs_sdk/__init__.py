"""
LiveGBS GB28181国标流媒体服务Python SDK

这是一个用于与LiveGBS流媒体服务交互的Python SDK，
提供了完整的API接口封装，包括用户认证、设备管理、流媒体控制等功能。

基本使用方法:
    from lsyiot_livegbs_sdk import LiveGBSAPI

    # 创建API客户端
    client = LiveGBSAPI('http://your-livegbs-server:10086')

    # 登录
    login_result = client.login('username', 'password')
    print(f"登录成功，URLToken: {login_result.url_token}")

作者: lsyiot
版本: 1.0.0
"""

from .api import LiveGBSAPI
from .responses import (
    LoginResponse,
    ModifyPasswordResponse,
    Device,
    DeviceListResponse,
    DeviceChannel,
    DeviceChannelListResponse,
    OnlineStatsResponse,
    StreamStartResponse,
    StreamStopResponse,
    StreamOSDResponse,
    PTZControlResponse,
    FIControlResponse,
    PresetControlResponse,
    HomePositionControlResponse,
)
from .exceptions import LiveGBSError, LiveGBSNetworkError, LiveGBSAPIError, LiveGBSParseError

__version__ = "1.0.0"
__author__ = "lsyiot"
__all__ = [
    "LiveGBSAPI",
    "LoginResponse",
    "ModifyPasswordResponse",
    "Device",
    "DeviceListResponse",
    "DeviceChannel",
    "DeviceChannelListResponse",
    "OnlineStatsResponse",
    "StreamStartResponse",
    "StreamStopResponse",
    "StreamOSDResponse",
    "PTZControlResponse",
    "FIControlResponse",
    "PresetControlResponse",
    "HomePositionControlResponse",
    "LiveGBSError",
    "LiveGBSNetworkError",
    "LiveGBSAPIError",
    "LiveGBSParseError",
]
