"""
LiveGBS GB28181国标流媒体服务响应数据类
包含所有API接口的响应数据类定义
"""

from typing import Optional, Dict, Any, List


class LoginResponse:
    """登录接口响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化登录响应
        :param data: 接口返回的数据
        """
        self.cookie_token: str = data.get("CookieToken", "")
        self.url_token: str = data.get("URLToken", "")
        self.stream_token: Optional[str] = data.get("StreamToken")
        self.token_timeout: int = data.get("TokenTimeout", 604800)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {"CookieToken": self.cookie_token, "URLToken": self.url_token, "TokenTimeout": self.token_timeout}
        if self.stream_token:
            result["StreamToken"] = self.stream_token
        return result


class ModifyPasswordResponse:
    """修改密码接口响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化修改密码响应
        :param data: 接口返回的数据
        """
        self.cookie_token: str = data.get("CookieToken", "")
        self.url_token: str = data.get("URLToken", "")
        self.stream_token: Optional[str] = data.get("StreamToken")
        self.token_timeout: int = data.get("TokenTimeout", 604800)
        # 兼容字段
        self.auth_token: str = data.get("AuthToken", "")  # 等同于 URLToken
        self.token: str = data.get("Token", "")  # 等同于 CookieToken

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "CookieToken": self.cookie_token,
            "URLToken": self.url_token,
            "TokenTimeout": self.token_timeout,
            "AuthToken": self.auth_token,
            "Token": self.token,
        }
        if self.stream_token:
            result["StreamToken"] = self.stream_token
        return result


class Device:
    """设备信息数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化设备信息
        :param data: 设备数据
        """
        self.id: str = data.get("ID", "")
        self.name: str = data.get("Name", "")
        self.custom_name: Optional[str] = data.get("CustomName")
        self.type: str = data.get("Type", "")
        self.channel_count: int = data.get("ChannelCount", 0)
        self.recv_stream_ip: Optional[str] = data.get("RecvStreamIP")
        self.contact_ip: Optional[str] = data.get("ContactIP")
        self.drop_channel_type: Optional[str] = data.get("DropChannelType")
        self.sms_id: Optional[str] = data.get("SMSID")
        self.sms_group_id: Optional[str] = data.get("SMSGroupID")
        self.catalog_interval: Optional[int] = data.get("CatalogInterval", 3600)
        self.subscribe_interval: Optional[int] = data.get("SubscribeInterval", 0)
        self.catalog_subscribe: bool = data.get("CatalogSubscribe", False)
        self.alarm_subscribe: bool = data.get("AlarmSubscribe", False)
        self.position_subscribe: bool = data.get("PositionSubscribe", False)
        self.ptz_subscribe: bool = data.get("PTZSubscribe", False)
        self.online: bool = data.get("Online", False)
        self.password: str = data.get("Password", "")
        self.record_center: bool = data.get("RecordCenter", False)
        self.record_indistinct: bool = data.get("RecordIndistinct", False)
        self.civil_code_first: bool = data.get("CivilCodeFirst", False)
        self.keep_original_tree: bool = data.get("KeepOriginalTree", False)
        self.command_transport: str = data.get("CommandTransport", "")
        self.media_transport: str = data.get("MediaTransport", "")
        self.media_transport_mode: str = data.get("MediaTransportMode", "")
        self.remote_ip: str = data.get("RemoteIP", "")
        self.remote_port: int = data.get("RemotePort", 0)
        self.longitude: Optional[float] = data.get("Longitude", 0)
        self.latitude: Optional[float] = data.get("Latitude", 0)
        self.last_register_at: str = data.get("LastRegisterAt", "")
        self.last_keepalive_at: str = data.get("LastKeepaliveAt", "")
        self.updated_at: str = data.get("UpdatedAt", "")
        self.created_at: str = data.get("CreatedAt", "")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "ID": self.id,
            "Name": self.name,
            "CustomName": self.custom_name,
            "Type": self.type,
            "ChannelCount": self.channel_count,
            "RecvStreamIP": self.recv_stream_ip,
            "ContactIP": self.contact_ip,
            "DropChannelType": self.drop_channel_type,
            "SMSID": self.sms_id,
            "SMSGroupID": self.sms_group_id,
            "CatalogInterval": self.catalog_interval,
            "SubscribeInterval": self.subscribe_interval,
            "CatalogSubscribe": self.catalog_subscribe,
            "AlarmSubscribe": self.alarm_subscribe,
            "PositionSubscribe": self.position_subscribe,
            "PTZSubscribe": self.ptz_subscribe,
            "Online": self.online,
            "Password": self.password,
            "RecordCenter": self.record_center,
            "RecordIndistinct": self.record_indistinct,
            "CivilCodeFirst": self.civil_code_first,
            "KeepOriginalTree": self.keep_original_tree,
            "CommandTransport": self.command_transport,
            "MediaTransport": self.media_transport,
            "MediaTransportMode": self.media_transport_mode,
            "RemoteIP": self.remote_ip,
            "RemotePort": self.remote_port,
            "Longitude": self.longitude,
            "Latitude": self.latitude,
            "LastRegisterAt": self.last_register_at,
            "LastKeepaliveAt": self.last_keepalive_at,
            "UpdatedAt": self.updated_at,
            "CreatedAt": self.created_at,
        }


class DeviceListResponse:
    """设备列表响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化设备列表响应
        :param data: 接口返回的数据
        """
        self.device_count: int = data.get("DeviceCount", 0)
        self.device_list: List[Device] = [Device(device_data) for device_data in data.get("DeviceList", [])]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {"DeviceCount": self.device_count, "DeviceList": [device.to_dict() for device in self.device_list]}


class DeviceChannel:
    """设备通道信息数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化设备通道信息
        :param data: 通道数据
        """
        self.id: str = data.get("ID", "")
        self.device_id: str = data.get("DeviceID", "")
        self.device_name: str = data.get("DeviceName", "")
        self.device_custom_name: Optional[str] = data.get("DeviceCustomName")
        self.device_type: str = data.get("DeviceType", "")
        self.device_online: bool = data.get("DeviceOnline", False)
        self.channel: int = data.get("Channel", 0)
        self.name: str = data.get("Name", "")
        self.custom_name: Optional[str] = data.get("CustomName")
        self.block: str = data.get("Block", "")
        self.custom_block: Optional[str] = data.get("CustomBlock")
        self.custom: bool = data.get("Custom", False)
        self.custom_id: Optional[str] = data.get("CustomID")
        self.sub_count: int = data.get("SubCount", 0)
        self.snap_url: Optional[str] = data.get("SnapURL")
        self.manufacturer: str = data.get("Manufacturer", "")
        self.custom_manufacturer: Optional[str] = data.get("CustomManufacturer")
        self.model: str = data.get("Model", "")
        self.custom_model: Optional[str] = data.get("CustomModel")
        self.owner: str = data.get("Owner", "")
        self.civil_code: str = data.get("CivilCode", "")
        self.custom_civil_code: Optional[str] = data.get("CustomCivilCode")
        self.address: str = data.get("Address", "")
        self.custom_address: Optional[str] = data.get("CustomAddress")
        self.firmware: Optional[str] = data.get("Firmware")
        self.custom_firmware: Optional[str] = data.get("CustomFirmware")
        self.serial_number: Optional[str] = data.get("SerialNumber")
        self.custom_serial_number: Optional[str] = data.get("CustomSerialNumber")
        self.ip_address: Optional[str] = data.get("IPAddress")
        self.custom_ip_address: Optional[str] = data.get("CustomIPAddress")
        self.port: Optional[int] = data.get("Port")
        self.custom_port: Optional[int] = data.get("CustomPort")
        self.parental: int = data.get("Parental", 0)
        self.parent_id: str = data.get("ParentID", "")
        self.custom_parent_id: Optional[str] = data.get("CustomParentID")
        self.secrecy: int = data.get("Secrecy", 0)
        self.register_way: int = data.get("RegisterWay", 1)
        self.status: str = data.get("Status", "")
        self.custom_status: Optional[str] = data.get("CustomStatus")
        self.longitude: Optional[float] = data.get("Longitude", 0)
        self.latitude: Optional[float] = data.get("Latitude", 0)
        self.custom_longitude: Optional[float] = data.get("CustomLongitude", 0)
        self.custom_latitude: Optional[float] = data.get("CustomLatitude", 0)
        self.altitude: Optional[float] = data.get("Altitude", 0)
        self.speed: Optional[float] = data.get("Speed", 0)
        self.direction: Optional[float] = data.get("Direction", 0)
        self.ptz_type: Optional[int] = data.get("PTZType", 0)
        self.custom_ptz_type: Optional[int] = data.get("CustomPTZType", 0)
        self.battery_level: Optional[int] = data.get("BatteryLevel", 0)
        self.signal_level: Optional[int] = data.get("SignalLevel", 0)
        self.download_speed: Optional[str] = data.get("DownloadSpeed")
        self.ondemand: bool = data.get("Ondemand", True)
        self.audio_enable: bool = data.get("AudioEnable", False)
        self.cloud_record: bool = data.get("CloudRecord", False)
        self.stream_id: Optional[str] = data.get("StreamID")
        self.num_outputs: Optional[int] = data.get("NumOutputs")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "ID": self.id,
            "DeviceID": self.device_id,
            "DeviceName": self.device_name,
            "DeviceCustomName": self.device_custom_name,
            "DeviceType": self.device_type,
            "DeviceOnline": self.device_online,
            "Channel": self.channel,
            "Name": self.name,
            "CustomName": self.custom_name,
            "Block": self.block,
            "CustomBlock": self.custom_block,
            "Custom": self.custom,
            "CustomID": self.custom_id,
            "SubCount": self.sub_count,
            "SnapURL": self.snap_url,
            "Manufacturer": self.manufacturer,
            "CustomManufacturer": self.custom_manufacturer,
            "Model": self.model,
            "CustomModel": self.custom_model,
            "Owner": self.owner,
            "CivilCode": self.civil_code,
            "CustomCivilCode": self.custom_civil_code,
            "Address": self.address,
            "CustomAddress": self.custom_address,
            "Firmware": self.firmware,
            "CustomFirmware": self.custom_firmware,
            "SerialNumber": self.serial_number,
            "CustomSerialNumber": self.custom_serial_number,
            "IPAddress": self.ip_address,
            "CustomIPAddress": self.custom_ip_address,
            "Port": self.port,
            "CustomPort": self.custom_port,
            "Parental": self.parental,
            "ParentID": self.parent_id,
            "CustomParentID": self.custom_parent_id,
            "Secrecy": self.secrecy,
            "RegisterWay": self.register_way,
            "Status": self.status,
            "CustomStatus": self.custom_status,
            "Longitude": self.longitude,
            "Latitude": self.latitude,
            "CustomLongitude": self.custom_longitude,
            "CustomLatitude": self.custom_latitude,
            "Altitude": self.altitude,
            "Speed": self.speed,
            "Direction": self.direction,
            "PTZType": self.ptz_type,
            "CustomPTZType": self.custom_ptz_type,
            "BatteryLevel": self.battery_level,
            "SignalLevel": self.signal_level,
            "DownloadSpeed": self.download_speed,
            "Ondemand": self.ondemand,
            "AudioEnable": self.audio_enable,
            "CloudRecord": self.cloud_record,
            "StreamID": self.stream_id,
            "NumOutputs": self.num_outputs,
        }


class DeviceChannelListResponse:
    """设备通道列表响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化设备通道列表响应
        :param data: 接口返回的数据
        """
        self.channel_count: int = data.get("ChannelCount", 0)
        self.channel_list: List[DeviceChannel] = [
            DeviceChannel(channel_data) for channel_data in data.get("ChannelList", [])
        ]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {"ChannelCount": self.channel_count, "ChannelList": [channel.to_dict() for channel in self.channel_list]}


class OnlineStatsResponse:
    """设备在线统计响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化设备在线统计响应
        :param data: 接口返回的数据
        """
        self.channel_online: int = data.get("ChannelOnline", 0)
        self.channel_total: int = data.get("ChannelTotal", 0)
        self.device_online: int = data.get("DeviceOnline", 0)
        self.device_total: int = data.get("DeviceTotal", 0)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "ChannelOnline": self.channel_online,
            "ChannelTotal": self.channel_total,
            "DeviceOnline": self.device_online,
            "DeviceTotal": self.device_total,
        }

    @property
    def device_online_rate(self) -> float:
        """设备在线率"""
        if self.device_total == 0:
            return 0.0
        return self.device_online / self.device_total

    @property
    def channel_online_rate(self) -> float:
        """通道在线率"""
        if self.channel_total == 0:
            return 0.0
        return self.channel_online / self.channel_total


class StreamStartResponse:
    """开始直播响应数据类"""

    def __init__(self, data: Dict[str, Any]):
        """
        初始化开始直播响应
        :param data: 接口返回的数据
        """
        self.stream_id: str = data.get("StreamID", "")
        self.sms_id: str = data.get("SMSID", "")
        self.device_id: str = data.get("DeviceID", "")
        self.channel_id: str = data.get("ChannelID", "")
        self.channel_name: str = data.get("ChannelName", "")
        self.webrtc: str = data.get("WEBRTC", "")
        self.flv: str = data.get("FLV", "")
        self.ws_flv: str = data.get("WS_FLV", "")
        self.rtmp: str = data.get("RTMP", "")
        self.hls: str = data.get("HLS", "")
        self.rtsp: Optional[str] = data.get("RTSP")
        self.cdn: Optional[str] = data.get("CDN")
        self.snap_url: Optional[str] = data.get("SnapURL")
        self.transport: str = data.get("Transport", "")
        self.start_at: str = data.get("StartAt", "")
        self.record_start_at: Optional[str] = data.get("RecordStartAt")
        self.duration: int = data.get("Duration", 0)
        self.source_video_codec_name: str = data.get("SourceVideoCodecName", "")
        self.source_video_width: int = data.get("SourceVideoWidth", 0)
        self.source_video_height: int = data.get("SourceVideoHeight", 0)
        self.source_video_frame_rate: float = data.get("SourceVideoFrameRate", 0.0)
        self.source_audio_codec_name: str = data.get("SourceAudioCodecName", "")
        self.source_audio_sample_rate: int = data.get("SourceAudioSampleRate", 0)
        self.rtp_count: int = data.get("RTPCount", 0)
        self.rtp_lost_count: int = data.get("RTPLostCount", 0)
        self.rtp_lost_rate: float = data.get("RTPLostRate", 0.0)
        self.video_frame_count: int = data.get("VideoFrameCount", 0)
        self.audio_enable: bool = data.get("AudioEnable", False)
        self.ondemand: bool = data.get("Ondemand", False)
        self.cloud_record: bool = data.get("CloudRecord", False)
        self.in_bytes: int = data.get("InBytes", 0)
        self.in_bit_rate: int = data.get("InBitRate", 0)
        self.out_bytes: int = data.get("OutBytes", 0)
        self.num_outputs: int = data.get("NumOutputs", 0)
        self.cascade_size: int = data.get("CascadeSize", 0)
        self.decode_size: int = data.get("DecodeSize", 0)
        self.relay_size: int = data.get("RelaySize", 0)
        self.channel_ptz_type: int = data.get("ChannelPTZType", 0)
        self.channel_osd: Optional[str] = data.get("ChannelOSD")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "StreamID": self.stream_id,
            "SMSID": self.sms_id,
            "DeviceID": self.device_id,
            "ChannelID": self.channel_id,
            "ChannelName": self.channel_name,
            "WEBRTC": self.webrtc,
            "FLV": self.flv,
            "WS_FLV": self.ws_flv,
            "RTMP": self.rtmp,
            "HLS": self.hls,
            "Transport": self.transport,
            "StartAt": self.start_at,
            "Duration": self.duration,
            "SourceVideoCodecName": self.source_video_codec_name,
            "SourceVideoWidth": self.source_video_width,
            "SourceVideoHeight": self.source_video_height,
            "SourceVideoFrameRate": self.source_video_frame_rate,
            "SourceAudioCodecName": self.source_audio_codec_name,
            "SourceAudioSampleRate": self.source_audio_sample_rate,
            "RTPCount": self.rtp_count,
            "RTPLostCount": self.rtp_lost_count,
            "RTPLostRate": self.rtp_lost_rate,
            "VideoFrameCount": self.video_frame_count,
            "AudioEnable": self.audio_enable,
            "Ondemand": self.ondemand,
            "CloudRecord": self.cloud_record,
            "InBytes": self.in_bytes,
            "InBitRate": self.in_bit_rate,
            "OutBytes": self.out_bytes,
            "NumOutputs": self.num_outputs,
            "CascadeSize": self.cascade_size,
            "DecodeSize": self.decode_size,
            "RelaySize": self.relay_size,
            "ChannelPTZType": self.channel_ptz_type,
        }

        # 添加可选字段
        if self.rtsp:
            result["RTSP"] = self.rtsp
        if self.cdn:
            result["CDN"] = self.cdn
        if self.snap_url:
            result["SnapURL"] = self.snap_url
        if self.record_start_at:
            result["RecordStartAt"] = self.record_start_at
        if self.channel_osd:
            result["ChannelOSD"] = self.channel_osd

        return result

    @property
    def video_resolution(self) -> str:
        """获取视频分辨率字符串"""
        return f"{self.source_video_width}x{self.source_video_height}"

    @property
    def is_streaming(self) -> bool:
        """是否正在直播"""
        return self.num_outputs > 0


class StreamStopResponse:
    """停止直播响应数据类"""

    def __init__(self, data):
        """
        初始化停止直播响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 停止直播接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "直播流停止成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "直播流停止成功")
        else:
            self.success = True
            self.message = "直播流停止成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }


class StreamOSDResponse:
    """视频水印响应数据类"""

    def __init__(self, data):
        """
        初始化视频水印响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 视频水印接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "视频水印设置成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "视频水印设置成功")
        else:
            self.success = True
            self.message = "视频水印设置成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }


class PTZControlResponse:
    """云台控制响应数据类"""

    def __init__(self, data):
        """
        初始化云台控制响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 云台控制接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "云台控制成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "云台控制成功")
        else:
            self.success = True
            self.message = "云台控制成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }


class FIControlResponse:
    """焦点光圈控制响应数据类"""

    def __init__(self, data):
        """
        初始化焦点光圈控制响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 焦点光圈控制接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "焦点光圈控制成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "焦点光圈控制成功")
        else:
            self.success = True
            self.message = "焦点光圈控制成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }


class PresetControlResponse:
    """预置位控制响应数据类"""

    def __init__(self, data):
        """
        初始化预置位控制响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 预置位控制接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "预置位控制成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "预置位控制成功")
        else:
            self.success = True
            self.message = "预置位控制成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }


class HomePositionControlResponse:
    """看守位控制响应数据类"""

    def __init__(self, data):
        """
        初始化看守位控制响应
        :param data: 接口返回的数据，可能是字符串或字典
        """
        # 看守位控制接口可能返回字符串或字典
        if isinstance(data, str):
            self.success = True
            self.message = data if data else "看守位控制成功"
        elif isinstance(data, dict):
            self.success = True
            self.message = data.get("message", "看守位控制成功")
        else:
            self.success = True
            self.message = "看守位控制成功"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "message": self.message,
        }
