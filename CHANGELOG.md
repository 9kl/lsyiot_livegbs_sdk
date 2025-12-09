# Changelog

本文件记录 lsyiot-livegbs-sdk 的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.0.3] - 2025-12-09

### Improved
- 优化 `LiveGBSError` 异常类的 `__str__` 方法，现在会包含 `response_text` 响应信息
  - 便于调试时查看完整的错误上下文
  - 输出格式：`[错误码] 错误消息 (响应: 响应内容)`

## [1.0.2] - 2025-12-09

### Fixed
- 修复 `start_stream` 方法的 `streamnumber` 参数类型问题，强制转换为字符串类型
  - 官方文档标注为 number 类型，但实际传数字时接口返回 HTTP 400 错误
  - 现在自动将 `streamnumber` 转换为字符串，确保接口调用正常

## [1.0.1] - 2025-09-22

### Added
- 完整的设备控制API
  - 云台控制 (`ptz_control`)：支持上下左右、变焦等操作
  - 焦点光圈控制 (`fi_control`)：支持聚焦、光圈调节
  - 预置位控制 (`preset_control`)：支持设置、跳转、删除预置位
  - 看守位控制 (`home_position_control`)：支持自动归位设置
- 视频水印功能 (`stream_osd`)：支持动态添加文字水印
- 直播流控制
  - 开始直播 (`start_stream`)：支持多种播放格式输出
  - 停止直播 (`stop_stream`)：支持检查在线人数
- 设备在线统计 (`get_device_online_stats`)

### Changed
- 优化项目结构，统一使用 `pyproject.toml` 配置
- 移除 `setup.py`、`requirements.txt`、`MANIFEST.in` 等冗余文件
- 更新许可证为 Apache License 2.0

### Security
- 移除文档中的敏感信息（服务器地址、设备序列号等）

## [1.0.0] - 2025-09-22

### Added
- 初始版本发布
- 用户认证功能
  - 登录 (`login`)：支持 MD5 密码加密
  - 退出 (`logout`)
  - 修改密码 (`modify_password`)
- 设备管理功能
  - 查询设备列表 (`get_device_list`)
  - 查询设备信息 (`get_device_info`)
  - 查询通道列表 (`get_device_channel_list`)
- 完善的异常处理机制
  - `LiveGBSError`：基础异常类
  - `LiveGBSNetworkError`：网络错误
  - `LiveGBSAPIError`：API错误
  - `LiveGBSParseError`：数据解析错误
- 类型提示支持
- 响应对象封装

[Unreleased]: https://github.com/9kl/lsyiot_livegbs_sdk/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/9kl/lsyiot_livegbs_sdk/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/9kl/lsyiot_livegbs_sdk/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/9kl/lsyiot_livegbs_sdk/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/9kl/lsyiot_livegbs_sdk/releases/tag/v1.0.0
