"""用户数据的读取与写入（提示词、生成选项与设置）。"""

import json
import os

from backend.config import ROOT_DIR
from backend.formatting import AVAILABLE_FIELDS, DEFAULT_FIELDS

STATE_FILE = os.path.join(ROOT_DIR, 'user_state.json')

# 各字段默认值：用于首次运行、以及读取时补齐缺失键 / 过滤未知键
_DEFAULTS = {
    # 提示词
    "quality_tags": "masterpiece",
    "banned_tags": "",
    "artist_tags": "",
    "character_tags": "",
    "meta_tags": "hires",
    "tags": "",
    # 生成选项
    "seed": -1,
    "img_length": 512,
    "img_width": 512,
    "mode_tags": "None",
    "length_tags": "short",
    "rating_tags": "safe",
    "max_tokens": 1024,
    "temperature": 0.8,
    "top_p": 0.95,
    "min_p": 0.05,
    "top_k": 60,
    "format_field_order": list(DEFAULT_FIELDS),
    # 设置
    "model_path": None,
    "n_ctx": 2048,
    "n_gpu_layers": -1,
}


class AppState:
    """用户状态。内部字典私有，只能通过属性读写；赋值即自动保存。"""

    def __init__(self, path=STATE_FILE):
        self.__path = path
        self.__data = self.__load()

    # ==================== 内部实现 ====================

    def __load(self):
        data = dict(_DEFAULTS)
        if os.path.exists(self.__path):
            try:
                with open(self.__path, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                if isinstance(saved, dict):
                    data.update({k: v for k, v in saved.items() if k in _DEFAULTS})
            except (json.JSONDecodeError, OSError):
                pass  # 文件损坏 / 无法读取时静默回退默认值
        # 清洗字段顺序，剔除已不存在的字段
        order = data.get("format_field_order")
        data["format_field_order"] = (
            [f for f in order if f in AVAILABLE_FIELDS]
            if isinstance(order, list) else list(DEFAULT_FIELDS)
        )
        return data

    def __save(self):
        try:
            with open(self.__path, 'w', encoding='utf-8') as f:
                json.dump(self.__data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"[AppState] 保存失败：{e}")

    def __write(self, key, value):
        # 值未变化则不写盘，避免无谓 IO
        if self.__data.get(key) != value:
            self.__data[key] = value
            self.__save()

    # ==================== 提示词 ====================

    @property
    def quality_tags(self):
        return self.__data["quality_tags"]

    @quality_tags.setter
    def quality_tags(self, value):
        self.__write("quality_tags", value)

    @property
    def banned_tags(self):
        return self.__data["banned_tags"]

    @banned_tags.setter
    def banned_tags(self, value):
        self.__write("banned_tags", value)

    @property
    def artist_tags(self):
        return self.__data["artist_tags"]

    @artist_tags.setter
    def artist_tags(self, value):
        self.__write("artist_tags", value)

    @property
    def character_tags(self):
        return self.__data["character_tags"]

    @character_tags.setter
    def character_tags(self, value):
        self.__write("character_tags", value)

    @property
    def meta_tags(self):
        return self.__data["meta_tags"]

    @meta_tags.setter
    def meta_tags(self, value):
        self.__write("meta_tags", value)

    @property
    def tags(self):
        return self.__data["tags"]

    @tags.setter
    def tags(self, value):
        self.__write("tags", value)

    # ==================== 生成选项 ====================

    @property
    def seed(self):
        return self.__data["seed"]

    @seed.setter
    def seed(self, value):
        self.__write("seed", value)

    @property
    def img_length(self):
        return self.__data["img_length"]

    @img_length.setter
    def img_length(self, value):
        self.__write("img_length", value)

    @property
    def img_width(self):
        return self.__data["img_width"]

    @img_width.setter
    def img_width(self, value):
        self.__write("img_width", value)

    @property
    def mode_tags(self):
        return self.__data["mode_tags"]

    @mode_tags.setter
    def mode_tags(self, value):
        self.__write("mode_tags", value)

    @property
    def length_tags(self):
        return self.__data["length_tags"]

    @length_tags.setter
    def length_tags(self, value):
        self.__write("length_tags", value)

    @property
    def rating_tags(self):
        return self.__data["rating_tags"]

    @rating_tags.setter
    def rating_tags(self, value):
        self.__write("rating_tags", value)

    @property
    def max_tokens(self):
        return self.__data["max_tokens"]

    @max_tokens.setter
    def max_tokens(self, value):
        self.__write("max_tokens", value)

    @property
    def temperature(self):
        return self.__data["temperature"]

    @temperature.setter
    def temperature(self, value):
        self.__write("temperature", value)

    @property
    def top_p(self):
        return self.__data["top_p"]

    @top_p.setter
    def top_p(self, value):
        self.__write("top_p", value)

    @property
    def min_p(self):
        return self.__data["min_p"]

    @min_p.setter
    def min_p(self, value):
        self.__write("min_p", value)

    @property
    def top_k(self):
        return self.__data["top_k"]

    @top_k.setter
    def top_k(self, value):
        self.__write("top_k", value)

    @property
    def format_field_order(self):
        return self.__data["format_field_order"]

    @format_field_order.setter
    def format_field_order(self, value):
        self.__write("format_field_order", value)

    # ==================== 设置 ====================

    @property
    def model_path(self):
        return self.__data["model_path"]

    @model_path.setter
    def model_path(self, value):
        self.__write("model_path", value)

    @property
    def n_ctx(self):
        return self.__data["n_ctx"]

    @n_ctx.setter
    def n_ctx(self, value):
        self.__write("n_ctx", value)

    @property
    def n_gpu_layers(self):
        return self.__data["n_gpu_layers"]

    @n_gpu_layers.setter
    def n_gpu_layers(self, value):
        self.__write("n_gpu_layers", value)
