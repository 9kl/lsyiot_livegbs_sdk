"""
测试直播流相关API
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from lsyiot_livegbs_sdk import LiveGBSAPI, StreamStartResponse, StreamStopResponse
from lsyiot_livegbs_sdk.exceptions import LiveGBSAPIError, LiveGBSNetworkError


class TestStartStream:
    """测试开始直播API"""

    @pytest.fixture
    def client(self):
        """创建API客户端实例"""
        return LiveGBSAPI("http://test-server:10000")

    @pytest.fixture
    def mock_stream_response(self):
        """模拟开始直播的成功响应"""
        return {
            "StreamID": "test-stream-id-12345",
            "DeviceID": "34020000001320000001",
            "ChannelID": "34020000001320000001",
            "ChannelName": "测试通道",
            "ChannelCustomName": "自定义通道名",
            "WEBRTC": "webrtc://test-server:10000/sms/xxx/rtc/xxx",
            "FLV": "http://test-server:10000/sms/xxx/flv/xxx.flv",
            "WS_FLV": "ws://test-server:10000/sms/xxx/flv/xxx.flv",
            "RTMP": "rtmp://test-server:11935/hls/xxx",
            "HLS": "http://test-server:10000/sms/xxx/hls/xxx/live.m3u8",
            "RTSP": "rtsp://test-server:10554/sms/xxx",
            "CDN": "",
            "SnapURL": "http://test-server:10000/snap/xxx.jpg",
            "Transport": "UDP",
            "StartAt": "2025-09-22T10:00:00+08:00",
            "RecordStartAt": "",
            "Duration": 0,
            "SourceVideoCodecName": "H264",
            "SourceVideoWidth": 1920,
            "SourceVideoHeight": 1080,
            "SourceVideoFrameRate": 25.0,
            "SourceAudioCodecName": "AAC",
            "SourceAudioSampleRate": 48000,
            "RTPCount": 100,
            "RTPLostCount": 0,
            "RTPLostRate": 0.0,
            "VideoFrameCount": 250,
            "AudioFrameCount": 500,
            "InBytes": 1024000,
            "OutBytes": 2048000,
            "NumOutputs": 1,
            "CascadeSize": 0,
            "CloudRecordSize": 0,
        }

    def test_start_stream_basic(self, client, mock_stream_response):
        """测试基本的开始直播功能"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response):
            result = client.start_stream(serial="34020000001320000001", channel=1)

            assert isinstance(result, StreamStartResponse)
            assert result.stream_id == "test-stream-id-12345"
            assert result.device_id == "34020000001320000001"
            assert result.transport == "UDP"
            assert "webrtc://" in result.webrtc
            assert "http://" in result.flv
            assert "rtmp://" in result.rtmp

    def test_start_stream_with_code(self, client, mock_stream_response):
        """测试使用通道编号开始直播"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.start_stream(
                serial="34020000001320000001",
                code="34020000001320000002",
            )

            # 验证请求参数
            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["serial"] == "34020000001320000001"
            assert request_data["code"] == "34020000001320000002"
            assert isinstance(result, StreamStartResponse)

    def test_start_stream_with_audio_transport(self, client, mock_stream_response):
        """测试设置音频和传输模式"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                audio="true",
                transport="TCP",
                transport_mode="active",
            )

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["audio"] == "true"
            assert request_data["transport"] == "TCP"
            assert request_data["transport_mode"] == "active"
            assert isinstance(result, StreamStartResponse)

    def test_start_stream_with_streamnumber(self, client, mock_stream_response):
        """测试指定码流编号"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            # 主码流
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                streamnumber=0,
            )
            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["streamnumber"] == 0

            # 子码流
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                streamnumber=1,
            )
            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["streamnumber"] == 1

    def test_start_stream_with_cdn(self, client, mock_stream_response):
        """测试CDN转推"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                cdn="rtmp://cdn.example.com/live/stream",
            )

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["cdn"] == "rtmp://cdn.example.com/live/stream"

    def test_start_stream_with_check_channel_status(self, client, mock_stream_response):
        """测试检查通道状态"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                check_channel_status=True,
            )

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["check_channel_status"] is True

    def test_start_stream_with_timeout(self, client, mock_stream_response):
        """测试自定义超时时间"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.start_stream(
                serial="34020000001320000001",
                channel=1,
                timeout=30,
            )

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["timeout"] == 30

    def test_start_stream_api_error(self, client):
        """测试API错误处理"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch.object(client.session, "request", return_value=mock_response):
            with pytest.raises(LiveGBSAPIError) as exc_info:
                client.start_stream(serial="34020000001320000001", channel=1)

            assert "500" in str(exc_info.value)

    def test_start_stream_network_error(self, client):
        """测试网络错误处理"""
        import requests

        with patch.object(
            client.session,
            "request",
            side_effect=requests.exceptions.ConnectionError("Connection refused"),
        ):
            with pytest.raises(LiveGBSNetworkError) as exc_info:
                client.start_stream(serial="34020000001320000001", channel=1)

            assert "网络请求失败" in str(exc_info.value)

    def test_start_stream_default_channel(self, client, mock_stream_response):
        """测试默认通道值"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_stream_response

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            # 不传channel参数
            result = client.start_stream(serial="34020000001320000001")

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            # 应该使用默认值1
            assert request_data["channel"] == 1


class TestStreamStartResponse:
    """测试StreamStartResponse响应类"""

    @pytest.fixture
    def response_data(self):
        """模拟响应数据"""
        return {
            "StreamID": "stream-12345",
            "DeviceID": "device-001",
            "ChannelID": "channel-001",
            "ChannelName": "测试通道",
            "WEBRTC": "webrtc://server/stream",
            "FLV": "http://server/stream.flv",
            "RTMP": "rtmp://server/stream",
            "HLS": "http://server/stream.m3u8",
            "RTSP": "rtsp://server/stream",
            "SourceVideoWidth": 1920,
            "SourceVideoHeight": 1080,
            "SourceVideoCodecName": "H264",
            "SourceAudioCodecName": "AAC",
            "Transport": "UDP",
            "NumOutputs": 2,
        }

    def test_response_properties(self, response_data):
        """测试响应属性"""
        response = StreamStartResponse(response_data)

        assert response.stream_id == "stream-12345"
        assert response.device_id == "device-001"
        assert response.channel_id == "channel-001"
        assert response.channel_name == "测试通道"
        assert response.webrtc == "webrtc://server/stream"
        assert response.flv == "http://server/stream.flv"
        assert response.rtmp == "rtmp://server/stream"
        assert response.hls == "http://server/stream.m3u8"
        assert response.rtsp == "rtsp://server/stream"

    def test_video_resolution_property(self, response_data):
        """测试视频分辨率属性"""
        response = StreamStartResponse(response_data)

        resolution = response.video_resolution
        assert resolution == "1920x1080"

    def test_is_streaming_property(self, response_data):
        """测试是否正在直播属性"""
        response = StreamStartResponse(response_data)

        assert response.is_streaming is True

        # 测试没有StreamID的情况
        response_data_no_stream = {"StreamID": ""}
        response_no_stream = StreamStartResponse(response_data_no_stream)
        assert response_no_stream.is_streaming is False

    def test_data_access(self, response_data):
        """测试数据访问"""
        response = StreamStartResponse(response_data)

        # 通过属性访问数据
        assert response.source_video_codec_name == "H264"
        assert response.source_audio_codec_name == "AAC"


class TestStopStream:
    """测试停止直播API"""

    @pytest.fixture
    def client(self):
        """创建API客户端实例"""
        return LiveGBSAPI("http://test-server:10000")

    def test_stop_stream_basic(self, client):
        """测试基本的停止直播功能"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "OK"

        with patch.object(client.session, "request", return_value=mock_response):
            result = client.stop_stream(serial="34020000001320000001", channel=1)

            assert isinstance(result, StreamStopResponse)
            assert result.success is True

    def test_stop_stream_text_response(self, client):
        """测试文本响应"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
        mock_response.text = "OK"

        with patch.object(client.session, "request", return_value=mock_response):
            result = client.stop_stream(serial="34020000001320000001", channel=1)

            assert isinstance(result, StreamStopResponse)

    def test_stop_stream_with_check_outputs(self, client):
        """测试检查在线人数"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "OK"

        with patch.object(client.session, "request", return_value=mock_response) as mock_request:
            result = client.stop_stream(
                serial="34020000001320000001",
                channel=1,
                check_outputs=True,
            )

            call_args = mock_request.call_args
            request_data = call_args.kwargs.get("json", {})
            assert request_data["check_outputs"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
