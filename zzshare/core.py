# -*- coding: utf-8 -*-
import requests
from typing import Any, Optional, Dict, Callable, List, Tuple, Union

from zzshare.logger import logger


import os

class ApiAuthError(Exception):
    pass

class ApiRateLimitError(Exception):
    pass

class BaseDataApi:
    def __init__(self, token: str = '', timeout: int = 10, http_url: str = 'https://api.zizizaizai.com'):
        self.token = token or os.environ.get('ZZSHARE_TOKEN', '')
        self.timeout = timeout
        self.http_url = http_url.rstrip('/')

        self.headers = {}
        if self.token:
            # SDK 鉴权使用自定义请求头 sdk-key（非 Bearer Token）
            self.headers['sdk-key'] = self.token

        # 注册快捷方法（在 __init__ 中自动注册）
        self._register_shortcuts()

    # ====================== 快捷映射表 ======================
    # 格式：(路径模板, [路径/必填参数名列表], 可选的后处理函数)
    # - 路径模板支持 {xxx} 占位符，会从 kwargs 中 pop 对应参数并替换
    # - param_names 中的参数会被优先用于路径替换，剩下的作为 query 参数
    # - post_process: 可选 callable，接收原始 data（dict 或 None），返回处理后的结果
    #   - 如果 post_process 返回 None，方法也会返回 None
    #   - 示例：过滤、排序、转换格式、添加默认值、异常处理等
    SHORTCUTS = {}

    def _register_shortcuts(self):
        """根据 SHORTCUTS 表动态生成方法"""
        for name, entry in self.SHORTCUTS.items():
            # 支持旧的三元组或新的四元组
            if len(entry) == 3:
                path_template, param_names, post_process = entry
                description = f"快捷调用：{path_template}"
            else:
                path_template, param_names, post_process, description = entry

            def make_method(
                    template: str = path_template,
                    params_list: List[str] = param_names,
                    processor: Optional[Callable[[Optional[Dict]], Any]] = post_process,
                    desc: str = description
            ):
                def shortcut_method(**kwargs) -> Any:
                    path = template
                    # 先处理路径参数：从 kwargs 中 pop 并替换 {xxx}
                    for param in params_list:
                        placeholder = f"{{{param}}}"
                        if placeholder in path:
                            if param not in kwargs:
                                raise ValueError(f"缺少路径参数 '{param}' for {name}")
                            value = kwargs.pop(param)
                            path = path.replace(placeholder, str(value))

                    # 剩下的 kwargs 作为 query 参数
                    data = self._query(path.lstrip('/'), params=kwargs)

                    # 后处理（如果定义了）
                    if processor:
                        return processor(data)
                    return data

                # 绑定方法名和文档
                shortcut_method.__name__ = name
                shortcut_method.__doc__ = (
                    f"{desc}\n\n"
                    f"API路径：{template}\n"
                    f"参数：{', '.join(params_list)}（路径参数会自动替换）\n"
                )
                setattr(self, name, shortcut_method)

            make_method()

    def _query(self, path: str, params: Optional[Dict] = None) -> Optional[Dict]:
        if params is None:
            params = {}

        url = f"{self.http_url}/{path}"
        try:
            res = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            if res.status_code == 200:
                data = res.json()
                if data.get('code') == 20000:
                    return data.get('data')
                else:
                    logger.error(f"API Error: {data.get('msg')}")
                    return None
            elif res.status_code == 401:
                msg = "工具执行错误：触发 401 鉴权失败。请亲切地告知用户：请检查本地是否正确配置了 ZZSHARE_TOKEN 环境变量，或个人中心 Token 是否变化。"
                logger.error(msg)
                raise ApiAuthError(msg)
            elif res.status_code == 429:
                msg = f"工具执行错误：触发频率限制 (429)。请亲切地告知用户：当前的 API 请求频次已达上限，建议稍作休息，或前往 zzshare 官网升级高级别会员以提升额度。附加信息: {res.text}"
                logger.warning(msg)
                raise ApiRateLimitError(msg)
            else:
                logger.error(f"HTTP Error: {res.status_code} - {res.text}")
                return None
        except Exception as e:
            logger.exception(f"Request Error: {e}")
            return None

    def query(self, api_name: str, params: Optional[Dict] = None) -> Optional[Dict]:
        return self._query(api_name, params)
