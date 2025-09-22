from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lsyiot-livegbs-sdk",
    version="1.0.1",
    author="fhp",
    author_email="chinafengheping@outlook.com",
    description="LiveGBS GB28181国标流媒体服务Python接口（https://gbs.liveqing.com:10010/apidoc/）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/9kl/lsyiot_livegbs_sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["requests>=2.25.0"],
)
