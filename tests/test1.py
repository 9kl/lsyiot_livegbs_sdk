from lsyiot_livegbs_sdk import LiveGBSAPI
from lsyiot_livegbs_sdk.exceptions import LiveGBSAPIError, LiveGBSNotFoundError, LiveGBSOfflineError

# 测试用设备信息
TEST_SERIAL = "34020000001320000008"
TEST_CHANNEL = 1


def get_client() -> LiveGBSAPI:
    """获取LiveGBSAPI客户端实例"""
    try:
        server_url = "http://127.0.0.1:10000"
        username = "admin"
        password = "hsd123456"

        client = LiveGBSAPI(server_url)
        login_result = client.login(username, password, url_token_only=True)
        client.session.headers.update({"Authorization": f"Bearer {login_result.url_token}"})
        return client
    except Exception as ex:
        print(f"获取客户端失败: {ex}")
        return None


def test_stream_start():
    """测试开始直播"""
    try:
        client = get_client()
        stream = client.start_stream(serial=TEST_SERIAL, channel=TEST_CHANNEL, streamnumber="1")
        print(stream.to_dict())
    except LiveGBSOfflineError as offline_err:
        print(f"设备不在线: {offline_err}")
    except LiveGBSNotFoundError as notfound_err:
        print(f"设备未找到: {notfound_err}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


def test_get_record_list():
    """测试查询录像列表"""
    try:
        client = get_client()
        if client is None:
            return

        # 查询最近一天的录像
        result = client.get_record_list(
            serial=TEST_SERIAL,
            channel=TEST_CHANNEL,
            starttime="2025-12-09T00:00:00",
            endtime="2025-12-10T00:00:00",
            type="all",
            timeout=30,
        )
        print(f"录像总数: {result.sum_num}")
        for record in result.record_list[:5]:  # 只打印前5条
            print(f"  - {record.start_time} ~ {record.end_time}, 文件大小: {record.file_size}")
    except LiveGBSOfflineError as offline_err:
        print(f"设备不在线: {offline_err}")
    except LiveGBSNotFoundError as notfound_err:
        print(f"设备未找到: {notfound_err}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


def test_start_playback():
    """测试开始回放"""
    try:
        client = get_client()
        if client is None:
            return

        result = client.start_playback(
            serial=TEST_SERIAL,
            channel=TEST_CHANNEL,
            starttime="2025-12-09T10:00:00",
            endtime="2025-12-09T10:30:00",
            download=False,
            transport="UDP",  # 使用 UDP 传输模式
            audio="false",  # 关闭音频
        )
        print(f"回放流ID: {result.stream_id}")
        print(f"FLV地址: {result.flv}")
        print(f"HLS地址: {result.hls}")
        return result.stream_id
    except LiveGBSOfflineError as offline_err:
        print(f"设备不在线: {offline_err}")
    except LiveGBSNotFoundError as notfound_err:
        print(f"设备未找到: {notfound_err}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")
    return None


def test_stop_playback(stream_id: str):
    """测试停止回放"""
    try:
        client = get_client()
        if client is None:
            return

        result = client.stop_playback(streamid=stream_id)
        print(f"停止回放成功: {result.success}")
        print(f"下载文件URL: {result.playback_file_url}")
    except LiveGBSAPIError as api_err:
        # 502 错误可能是回放流已自动结束
        if "502" in str(api_err):
            print(f"回放流可能已自动结束: {api_err}")
        else:
            print(f"API错误: {api_err}")


def test_control_playback(stream_id: str):
    """测试回放控制"""
    try:
        client = get_client()
        if client is None:
            return

        # 测试暂停
        result = client.control_playback(streamid=stream_id, command="pause")
        print(f"暂停回放: {result.success}")

        # 测试继续播放
        result = client.control_playback(streamid=stream_id, command="play", range="now")
        print(f"继续播放: {result.success}")

        # 测试倍速播放
        result = client.control_playback(streamid=stream_id, command="scale", scale=2.0)
        print(f"2倍速播放: {result.success}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


def test_get_playback_stream_list():
    """测试查询回放流列表"""
    try:
        client = get_client()
        if client is None:
            return

        result = client.get_playback_stream_list(start=0, limit=10)
        print(f"回放流总数: {result.playback_count}")
        for stream in result.playbacks:
            print(f"  - 流ID: {stream.stream_id}")
            print(f"    通道: {stream.channel_name}")
            print(f"    回放进度: {stream.playback_progress * 100:.1f}%")
            print(f"    下载进度: {stream.download_progress * 100:.1f}%")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


def test_get_playback_stream_info(stream_id: str):
    """测试获取单条回放流信息"""
    try:
        client = get_client()
        if client is None:
            return

        result = client.get_playback_stream_info(stream_id=stream_id)
        stream = result.stream
        print(f"流ID: {stream.stream_id}")
        print(f"通道名称: {stream.channel_name}")
        print(f"回放开始时间: {stream.playback_start_time}")
        print(f"回放结束时间: {stream.playback_end_time}")
        print(f"回放总时长: {stream.playback_duration}秒")
        print(f"当前回放时长: {stream.timestamp_sec}秒")
        print(f"回放进度: {stream.playback_progress * 100:.1f}%")
        print(f"下载进度: {stream.download_progress * 100:.1f}%")
        print(f"视频分辨率: {stream.video_resolution}")
        print(f"视频编码: {stream.source_video_codec_name}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


def test_playback_workflow():
    """测试完整的回放工作流程"""
    print("=" * 50)
    print("1. 查询录像列表")
    print("=" * 50)
    test_get_record_list()

    print("\n" + "=" * 50)
    print("2. 开始回放")
    print("=" * 50)
    stream_id = test_start_playback()

    if stream_id:
        print("\n" + "=" * 50)
        print("3. 查询回放流列表")
        print("=" * 50)
        test_get_playback_stream_list()

        print("\n" + "=" * 50)
        print("4. 获取单条回放流信息")
        print("=" * 50)
        test_get_playback_stream_info(stream_id)

        print("\n" + "=" * 50)
        print("5. 回放控制（暂停/继续/倍速）")
        print("=" * 50)
        test_control_playback(stream_id)

        print("\n" + "=" * 50)
        print("6. 停止回放")
        print("=" * 50)
        test_stop_playback(stream_id)


if __name__ == "__main__":
    # 单独测试直播
    # test_stream_start()

    # 测试完整的回放工作流程
    test_playback_workflow()
