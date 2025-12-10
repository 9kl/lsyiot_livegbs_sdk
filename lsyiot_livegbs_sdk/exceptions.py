"""
LiveGBS GB28181国标流媒体服务异常模块
包含所有LiveGBS相关的异常类定义
"""


class LiveGBSError(Exception):
    """LiveGBS异常基类"""

    def __init__(self, message: str, error_code: str = None, response_text: str = None):
        """
        初始化LiveGBS异常
        :param message: 错误消息
        :param error_code: 错误代码
        :param response_text: 响应文本（用于调试）
        """
        super().__init__(message)
        self.error_code = error_code
        self.response_text = response_text
        self.message = message

    def __str__(self):
        parts = []
        if self.error_code:
            parts.append(f"[{self.error_code}]")
        parts.append(self.message)
        if self.response_text:
            parts.append(f"(响应: {self.response_text})")
        return " ".join(parts)


class LiveGBSNetworkError(LiveGBSError):
    """网络相关异常"""

    pass


class LiveGBSAPIError(LiveGBSError):
    """API业务逻辑异常"""

    pass


class LiveGBSOfflineError(LiveGBSError):
    """设备不在线异常"""

    pass


class LiveGBSNotFoundError(LiveGBSError):
    """设备未找到异常"""

    pass


class LiveGBSParseError(LiveGBSError):
    """数据解析异常"""

    pass
