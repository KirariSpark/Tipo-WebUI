"""模型文件的扫描以及 llama.cpp 模型的生命周期管理。"""

import os

from llama_cpp import Llama

from backend.config import ROOT_DIR, locale

MODELS_DIR = os.path.join(ROOT_DIR, 'models')

# 当前已加载的模型，None 表示尚未加载
llm = None


##########################

# 获取模型文件列表
def list_model_files():
    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.gguf')]
    # 返回相对于项目根目录的路径，方便展示也方便加载
    return [os.path.relpath(os.path.join(MODELS_DIR, f), ROOT_DIR) for f in model_files]


##########################

# 加载模型
def load_model(model_path, gpu, n_ctx):
    global llm
    try:
        if not model_path:
            return locale["no_model"]
        llm = None
        llm = Llama(model_path=model_path, n_gpu_layers=gpu, n_ctx=n_ctx)
        return locale["load_model_success"].format(model_path=model_path)
    except Exception as e:
        return str(e)


##########################

# 卸载模型
def unload_model():
    global llm
    llm = None
    return locale["unload_model_success"]
