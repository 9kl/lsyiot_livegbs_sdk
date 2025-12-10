from lsyiot_livegbs_sdk import LiveGBSAPI
from lsyiot_livegbs_sdk.exceptions import LiveGBSAPIError, LiveGBSNotFoundError, LiveGBSOfflineError


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
        return None


def test_stream_start():
    try:
        client = get_client()
        stream = client.start_stream(serial="34020000001320000012", channel=20, streamnumber="1")
        print(stream.to_dict())
    except LiveGBSOfflineError as offline_err:
        print(f"设备不在线: {offline_err}")
    except LiveGBSNotFoundError as notfound_err:
        print(f"设备未找到: {notfound_err}")
    except LiveGBSAPIError as api_err:
        print(f"API错误: {api_err}")


if __name__ == "__main__":
    test_stream_start()
