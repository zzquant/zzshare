# -*- coding: utf-8 -*-
import requests
from typing import Any, Optional, Dict, Callable, List, Tuple, Union


class BaseDataApi:
    def __init__(self, token: str = '', timeout: int = 10, http_url: str = 'https://api.zizizaizai.com'):
        self.token = token
        self.timeout = timeout
        self.http_url = http_url.rstrip('/')

        self.headers = {}
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

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
        for name, (path_template, param_names, post_process) in self.SHORTCUTS.items():
            def make_method(
                    template: str = path_template,
                    params_list: List[str] = param_names,
                    processor: Optional[Callable[[Optional[Dict]], Any]] = post_process
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
                    f"快捷调用：{template}\n"
                    f"参数：{', '.join(params_list)}（路径参数会自动替换）\n"
                    f"后处理：{processor.__name__ if processor else '无'}"
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
                    print(f"API Error: {data.get('msg')}")
                    return None
            else:
                print(f"HTTP Error: {res.status_code} - {res.text}")
                return None
        except Exception as e:
            print(f"Request Error: {e}")
            return None

    def query(self, api_name: str, params: Optional[Dict] = None) -> Optional[Dict]:
        return self._query(api_name, params)
