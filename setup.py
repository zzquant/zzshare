from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zzshare",
    version="0.1.2",
    author="zzquant",
    author_email="",
    description="A股量化数据接口 SDK - 免费、开箱即用的量化数据接口",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzquant/zzshare",
    project_urls={
        "Homepage": "https://github.com/zzquant/zzshare",
        "Repository": "https://github.com/zzquant/zzshare",
        "Issues": "https://github.com/zzquant/zzshare/issues",
    },
    packages=find_packages(exclude=["test*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="stock quant finance tushare china a-share kline market-data",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.3.0",
    ],
    license="MIT",
    include_package_data=True,
    package_data={"zzshare": ["*.pyi"]},
)
