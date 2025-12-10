"""
LiveGBS GB28181国标流媒体服务API客户端
"""

import hashlib
import json
from typing import Optional, Dict, Any
from urllib.parse import urljoin

import requests

from .exceptions import (
    LiveGBSError,
    LiveGBSNetworkError,
    LiveGBSAPIError,
    LiveGBSOfflineError,
    LiveGBSNotFoundError,
    LiveGBSParseError,
)
from .responses import (
    LoginResponse,
    ModifyPasswordResponse,
    Device,
    DeviceListResponse,
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


class LiveGBSAPI:
    """LiveGBS API客户端类"""

    def __init__(self, base_url: str, timeout: int = 30, verify: bool = True):
        """
        初始化LiveGBS API客户端
        :param base_url: LiveGBS服务的基础URL
        :param timeout: 请求超时时间（秒）
        :param verify: 是否验证SSL证书
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify = verify
        self.session = requests.Session()

        # 设置默认headers
        self.session.headers.update({"Content-Type": "application/json", "User-Agent": "LiveGBS-Python-SDK/1.0.0"})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        :param method: HTTP方法
        :param endpoint: API端点
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(method=method, url=url, timeout=self.timeout, verify=self.verify, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            raise LiveGBSNetworkError(f"网络请求失败: {str(e)}")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理响应数据
        :param response: 响应对象
        :return: 解析后的数据
        """
        try:
            # 检查HTTP状态码
            if response.status_code != 200:
                # 先判断是否是设备不在线
                if "offline" in response.text.lower():
                    raise LiveGBSOfflineError(
                        "设备不在线",
                        error_code=str(response.status_code),
                        response_text=response.text,
                    )
                # 判断是否是设备未找到
                if "not found" in response.text.lower():
                    raise LiveGBSNotFoundError(
                        "设备未找到",
                        error_code=str(response.status_code),
                        response_text=response.text,
                    )
                raise LiveGBSAPIError(
                    f"API请求失败，状态码: {response.status_code}",
                    error_code=str(response.status_code),
                    response_text=response.text,
                )

            # 解析JSON响应
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise LiveGBSParseError("响应数据不是有效的JSON格式", response_text=response.text)

            return data

        except LiveGBSError:
            raise
        except Exception as e:
            raise LiveGBSError(f"处理响应时发生未知错误: {str(e)}", response_text=response.text)

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        对密码进行MD5加密
        :param password: 原始密码
        :return: MD5加密后的密码（32位长度，不带中划线，小写）
        """
        return hashlib.md5(password.encode("utf-8")).hexdigest().lower()

    def _handle_flexible_response(self, response: requests.Response, operation_name: str) -> Any:
        """
        处理可能返回JSON或纯文本的响应
        :param response: HTTP响应对象
        :param operation_name: 操作名称，用于错误信息
        :return: 响应数据（JSON对象或文本字符串）
        """
        try:
            if response.status_code != 200:
                if "offline" in response.text.lower():
                    raise LiveGBSOfflineError(
                        f"{operation_name}失败，设备不在线",
                        error_code=str(response.status_code),
                        response_text=response.text,
                    )
                if "not found" in response.text.lower():
                    raise LiveGBSNotFoundError(
                        f"{operation_name}失败，设备未找到",
                        error_code=str(response.status_code),
                        response_text=response.text,
                    )
                raise LiveGBSAPIError(
                    f"{operation_name}失败，状态码: {response.status_code}",
                    error_code=str(response.status_code),
                    response_text=response.text,
                )

            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text

        except LiveGBSError:
            raise
        except Exception as e:
            raise LiveGBSError(f"{operation_name}时发生未知错误: {str(e)}", response_text=response.text)

    @staticmethod
    def _add_channel_param(data: Dict[str, Any], channel: Optional[int], code: Optional[str]) -> None:
        """
        添加通道相关参数
        :param data: 请求数据字典
        :param channel: 通道序号
        :param code: 通道编号
        """
        data["channel"] = channel if channel is not None else 1
        if code is not None:
            data["code"] = code

    def login(
        self, username: str, password: str, url_token_only: bool = False, token_timeout: int = 604800
    ) -> LoginResponse:
        """
        用户登录
        :param username: 用户名
        :param password: 密码（原始密码，会自动进行MD5加密）
        :param url_token_only: 是否只获取URLToken，默认False
        :param token_timeout: Token超时时间（秒），默认604800
        :return: 登录响应对象
        """
        # 准备请求数据
        data = {
            "username": username,
            "password": self._hash_password(password),
            "url_token_only": url_token_only,
            "token_timeout": token_timeout,
        }

        # 发送登录请求
        response = self._make_request("POST", "/api/v1/login", json=data)
        response_data = self._handle_response(response)

        # 返回登录响应对象
        return LoginResponse(response_data)

    def logout(self) -> bool:
        """
        用户退出登录
        :return: 是否成功退出
        """
        # 发送退出登录请求
        response = self._make_request("GET", "/api/v1/logout")

        # 检查响应状态码，200表示成功
        if response.status_code == 200:
            return True
        else:
            self._handle_response(response)  # 这会抛出相应的异常
            return False

    def modify_password(self, old_password: str, new_password: str) -> ModifyPasswordResponse:
        """
        修改密码
        :param old_password: 旧密码（原始密码，会自动进行MD5加密）
        :param new_password: 新密码（原始密码，会自动进行MD5加密）
        :return: 修改密码响应对象
        """
        # 准备请求数据
        data = {
            "oldpassword": self._hash_password(old_password),
            "newpassword": self._hash_password(new_password),
        }

        # 发送修改密码请求
        response = self._make_request("POST", "/api/v1/modifypassword", json=data)
        response_data = self._handle_response(response)

        # 返回修改密码响应对象
        return ModifyPasswordResponse(response_data)

    def get_device_list(
        self,
        device_type: str = "all",
        start: Optional[int] = None,
        limit: int = 1000,
        q: Optional[str] = None,
        online: Optional[bool] = None,
    ) -> DeviceListResponse:
        """
        查询设备列表
        :param device_type: 设备类型，device-国标设备, decode-解码器, all-所有，默认all
        :param start: 分页游标开始(不是页码),从零开始
        :param limit: 分页大小，默认1000
        :param q: 搜索关键字
        :param online: 在线状态
        :return: 设备列表响应对象
        """
        # 准备查询参数
        params = {"device_type": device_type, "limit": limit}

        if start is not None:
            params["start"] = start
        if q is not None:
            params["q"] = q
        if online is not None:
            params["online"] = online

        # 发送请求
        response = self._make_request("GET", "/api/v1/device/list", params=params)
        response_data = self._handle_response(response)

        # 返回设备列表响应对象
        return DeviceListResponse(response_data)

    def get_device_info(self, serial: str) -> Device:
        """
        查询单条设备信息
        :param serial: 设备编号
        :return: 设备信息对象
        """
        # 准备查询参数
        params = {"serial": serial}

        # 发送请求
        response = self._make_request("GET", "/api/v1/device/info", params=params)
        response_data = self._handle_response(response)

        # 返回设备信息对象
        return Device(response_data)

    def get_device_channel_list(
        self,
        serial: Optional[str] = None,
        code: Optional[str] = None,
        civilcode: Optional[str] = None,
        block: Optional[str] = None,
        channel_type: str = "all",
        dir_serial: Optional[str] = None,
        start: Optional[int] = None,
        limit: int = 1000,
        q: Optional[str] = None,
        online: Optional[bool] = None,
    ) -> DeviceChannelListResponse:
        """
        查询设备通道列表
        :param serial: 设备国标编号，多条用逗号分隔
        :param code: 通道国标编号，多条用逗号分隔
        :param civilcode: 行政区号
        :param block: 警区
        :param channel_type: 通道类型，device-子设备, decode-解码器, dir-子目录, all-所有，默认all
        :param dir_serial: 子目录编号
        :param start: 分页游标开始(不是页码),从零开始
        :param limit: 分页大小，默认1000
        :param q: 搜索关键字
        :param online: 在线状态
        :return: 设备通道列表响应对象
        """
        # 准备查询参数
        params = {"channel_type": channel_type, "limit": limit}

        if serial is not None:
            params["serial"] = serial
        if code is not None:
            params["code"] = code
        if civilcode is not None:
            params["civilcode"] = civilcode
        if block is not None:
            params["block"] = block
        if dir_serial is not None:
            params["dir_serial"] = dir_serial
        if start is not None:
            params["start"] = start
        if q is not None:
            params["q"] = q
        if online is not None:
            params["online"] = online

        # 发送请求
        response = self._make_request("GET", "/api/v1/device/channellist", params=params)
        response_data = self._handle_response(response)

        # 返回设备通道列表响应对象
        return DeviceChannelListResponse(response_data)

    def get_device_online_stats(self) -> OnlineStatsResponse:
        """
        查询设备在线统计
        :return: 设备在线统计响应对象
        """
        # 发送请求
        response = self._make_request("GET", "/api/v1/device/onlinestats")
        response_data = self._handle_response(response)

        # 返回设备在线统计响应对象
        return OnlineStatsResponse(response_data)

    def start_stream(
        self,
        serial: str,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        sms_id: Optional[str] = None,
        sms_group_id: Optional[str] = None,
        cdn: Optional[str] = None,
        audio: str = "config",
        transport: str = "config",
        transport_mode: str = "passive",
        streamnumber: Optional[int] = None,
        check_channel_status: bool = False,
        timeout: Optional[int] = None,
    ) -> StreamStartResponse:
        """
        开始直播
        :param serial: 设备编号
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param sms_id: 指定SMS，默认取设备配置
        :param sms_group_id: 指定SMS分组，默认取设备配置
        :param cdn: 转推 CDN 地址，形如: [rtmp|rtsp]://xxx，需要encodeURIComponent
        :param audio: 是否开启音频，默认 config 表示读取通道音频开关配置，允许值: true, false, config
        :param transport: 流传输模式，默认 config 表示读取设备流传输模式配置，允许值: TCP, UDP, config
        :param transport_mode: 当 transport=TCP 时有效，指示流传输主被动模式，默认被动，允许值: active, passive
        :param streamnumber: 码流编号，0 - 主码流，1 - 子码流；以此类推
        :param check_channel_status: 是否检查通道状态，默认 false，表示拉流前不检查通道状态是否在线
        :param timeout: 拉流超时(秒)，默认使用 livecms.ini > sip > ack_timeout
        :return: 开始直播响应对象
        """
        # 准备请求数据
        data = {
            "serial": serial,
            "audio": audio,
            "transport": transport,
            "transport_mode": transport_mode,
            "check_channel_status": check_channel_status,
        }

        # 添加可选参数
        if channel is not None:
            data["channel"] = channel
        else:
            data["channel"] = 1  # 默认值

        if code is not None:
            data["code"] = code
        if sms_id is not None:
            data["sms_id"] = sms_id
        if sms_group_id is not None:
            data["sms_group_id"] = sms_group_id
        if cdn is not None:
            data["cdn"] = cdn
        if streamnumber is not None:
            data["streamnumber"] = str(streamnumber)
        if timeout is not None:
            data["timeout"] = timeout

        # 发送请求
        response = self._make_request("POST", "/api/v1/stream/start", json=data)
        response_data = self._handle_response(response)

        # 返回开始直播响应对象
        return StreamStartResponse(response_data)

    def stop_stream(
        self,
        serial: str,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        check_outputs: bool = False,
    ) -> StreamStopResponse:
        """
        停止直播
        谨慎调用，直播流单路拉取多路播放，停止直播流可能影响其它正在同一通道上的客户端播放
        直播流在一定时间内(默认1分钟)，没有客户端观看会自动停止

        :param serial: 设备编号
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param check_outputs: 是否检查通道在线人数，默认 false，表示停止前不检查通道是否有客户端正在播放
        :return: 停止直播响应对象
        """
        data: Dict[str, Any] = {"serial": serial, "check_outputs": check_outputs}
        self._add_channel_param(data, channel, code)

        response = self._make_request("POST", "/api/v1/stream/stop", json=data)
        response_data = self._handle_flexible_response(response, "停止直播")
        return StreamStopResponse(response_data)

    def stream_osd(
        self,
        serial: str,
        code: str,
        streamid: Optional[str] = None,
        text: Optional[str] = None,
        color: str = "white",
        border_color: str = "black",
        x: Optional[str] = None,
        y: Optional[str] = None,
        size: Optional[int] = None,
    ) -> StreamOSDResponse:
        """
        设置视频水印
        :param serial: 设备国标编号
        :param code: 通道国标编号
        :param streamid: 流标识，来自开始直播或开始回放接口返回的StreamID
        :param text: 文字内容
        :param color: 文字颜色，默认white
        :param border_color: 文字边框颜色，默认black
        :param x: 文字水平位置X
        :param y: 文字垂直位置Y
        :param size: 字体大小
        :return: 视频水印响应对象
        """
        data: Dict[str, Any] = {
            "serial": serial,
            "code": code,
            "color": color,
            "border_color": border_color,
        }

        # 添加可选参数
        if streamid is not None:
            data["streamid"] = streamid
        if text is not None:
            data["text"] = text
        if x is not None:
            data["x"] = x
        if y is not None:
            data["y"] = y
        if size is not None:
            data["size"] = size

        response = self._make_request("POST", "/api/v1/stream/osd", json=data)
        response_data = self._handle_flexible_response(response, "设置视频水印")
        return StreamOSDResponse(response_data)

    def ptz_control(
        self,
        serial: str,
        command: str,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        speed: int = 129,
    ) -> PTZControlResponse:
        """
        云台控制
        :param serial: 设备编号
        :param command: 控制指令，允许值: left, right, up, down, upleft, upright, downleft, downright, zoomin, zoomout, stop
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param speed: 速度(0~255)，默认129
        :return: 云台控制响应对象
        """
        valid_commands = [
            "left",
            "right",
            "up",
            "down",
            "upleft",
            "upright",
            "downleft",
            "downright",
            "zoomin",
            "zoomout",
            "stop",
        ]
        if command not in valid_commands:
            raise ValueError(f"无效的控制指令: {command}，允许的值: {', '.join(valid_commands)}")

        data: Dict[str, Any] = {"serial": serial, "command": command, "speed": speed}
        self._add_channel_param(data, channel, code)

        response = self._make_request("POST", "/api/v1/control/ptz", json=data)
        response_data = self._handle_flexible_response(response, "云台控制")
        return PTZControlResponse(response_data)

    def fi_control(
        self,
        serial: str,
        command: str,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        speed: int = 129,
    ) -> FIControlResponse:
        """
        焦点光圈控制
        :param serial: 设备编号
        :param command: 控制指令，允许值: focusnear, focusfar, irisin, irisout, stop
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param speed: 速度(0~255)，默认129
        :return: 焦点光圈控制响应对象
        """
        valid_commands = ["focusnear", "focusfar", "irisin", "irisout", "stop"]
        if command not in valid_commands:
            raise ValueError(f"无效的控制指令: {command}，允许的值: {', '.join(valid_commands)}")

        data: Dict[str, Any] = {"serial": serial, "command": command, "speed": speed}
        self._add_channel_param(data, channel, code)

        response = self._make_request("POST", "/api/v1/control/fi", json=data)
        response_data = self._handle_flexible_response(response, "焦点光圈控制")
        return FIControlResponse(response_data)

    def preset_control(
        self,
        serial: str,
        command: str,
        preset: int,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        name: Optional[str] = None,
    ) -> PresetControlResponse:
        """
        预置位控制
        :param serial: 设备编号
        :param command: 控制指令，允许值: set, goto, remove
        :param preset: 预置位编号(1~255)
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param name: 预置位名称，command=set 时有效
        :return: 预置位控制响应对象
        """
        valid_commands = ["set", "goto", "remove"]
        if command not in valid_commands:
            raise ValueError(f"无效的控制指令: {command}，允许的值: {', '.join(valid_commands)}")

        if not (1 <= preset <= 255):
            raise ValueError(f"预置位编号必须在1-255之间，当前值: {preset}")

        data: Dict[str, Any] = {"serial": serial, "command": command, "preset": preset}
        self._add_channel_param(data, channel, code)
        if name is not None:
            data["name"] = name

        response = self._make_request("POST", "/api/v1/control/preset", json=data)
        response_data = self._handle_flexible_response(response, "预置位控制")
        return PresetControlResponse(response_data)

    def home_position_control(
        self,
        serial: str,
        resettime: int,
        presetindex: int,
        channel: Optional[int] = None,
        code: Optional[str] = None,
        enabled: bool = False,
        timeout: int = 15,
    ) -> HomePositionControlResponse:
        """
        看守位控制
        :param serial: 设备编号
        :param resettime: 自动归位时间间隔(秒)
        :param presetindex: 调用预置位编号
        :param channel: 通道序号，默认1
        :param code: 通道编号，通过 /api/v1/device/channellist 获取的 ChannelList.ID，该参数和 channel 二选一传递即可
        :param enabled: 使能开关，默认false
        :param timeout: 超时时间(秒)，默认15
        :return: 看守位控制响应对象
        """
        data: Dict[str, Any] = {
            "serial": serial,
            "resettime": resettime,
            "presetindex": presetindex,
            "enabled": enabled,
            "timeout": timeout,
        }
        self._add_channel_param(data, channel, code)

        response = self._make_request("POST", "/api/v1/control/homeposition", json=data)
        response_data = self._handle_flexible_response(response, "看守位控制")
        return HomePositionControlResponse(response_data)
