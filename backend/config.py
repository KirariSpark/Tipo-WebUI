"""语言配置与本地化资源的加载。"""

import json
import os

# 项目根目录（backend 文件夹的上一级）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES_DIR = os.path.join(ROOT_DIR, 'Locales')


def _load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 加载语言
print("Loading configs...")
config = _load_json(os.path.join(LOCALES_DIR, 'config.json'))
lang = config['language']
locale = _load_json(os.path.join(LOCALES_DIR, f'{lang}.json'))
print(locale["locale_load_success"])


def load_tutorial(language=None):
    """读取对应语言的教程 Markdown 内容。"""
    language = language or lang
    tutorial_path = os.path.join(LOCALES_DIR, 'Tutorials', f'{language}.md')
    with open(tutorial_path, "r", encoding="utf-8") as tutorial:
        return tutorial.read()
