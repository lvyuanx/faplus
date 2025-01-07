from setuptools import setup, find_packages

setup(
    name="faplus",
    version="0.1.0",
    author="lvyuanxiang",
    author_email="testlv@foxmail.com",
    description="这是一个基于fastapi的增强包，用于实现类django的快速开发",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lvyuanx/faplus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi~=0.115.2",
        "Markdown~=3.7",
        "uvicorn[standard]~=0.32.0",
        "tortoise-orm~=0.21.7",
        "aerich~=0.7.2",
        "aiomysql~=0.2.0",
        "cryptography~=43.0.3",
        "PyJWT~=2.9.0",
        "redis~=5.2.0",
        "pytz~=2024.2",
        "python-multipart~=0.0.20",
        "aiofiles~=24.1.0",
    ],
)
