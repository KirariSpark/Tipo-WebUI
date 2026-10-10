"""提示词文本的解析、过滤与格式化。"""

import re


##########################

# 可用于格式化的字段全集（顺序仅作为下拉框的默认展示顺序）
AVAILABLE_FIELDS = ['quality', 'artist', 'characters', 'meta', 'rating', 'tag', 'short', 'long']

# 默认保留的字段及顺序
DEFAULT_FIELDS = list(AVAILABLE_FIELDS)


# 格式化输出
def extract_and_format(model_out, fields_to_extract=None):
    # 未传入字段列表时使用默认顺序；传入空列表表示不保留任何字段
    if fields_to_extract is None:
        fields_to_extract = DEFAULT_FIELDS

    def extract_fields(model_output):
        extracted_data = {}

        for line in model_output.split('\n'):
            for field in fields_to_extract:
                if line.startswith(field + ':'):
                    extracted_data[field] = line[len(field) + 1:].strip()

        return extracted_data

    extracted_data = extract_fields(model_out)
    formatted_output = ""

    for field in fields_to_extract:
        value = extracted_data.get(field, '')
        if value:  # Only add the field if it has a value
            formatted_output += f"{value}\n\n"

    # Remove the last two newline characters to ensure no extra space at the end
    formatted_output = formatted_output.rstrip('\n')

    return formatted_output


##########################

# 排除标签
def remove_words_by_regex(sentence, pattern):
    # 移除末尾的逗号和空格（如果有的话）
    patterns = pattern.rstrip(', ')
    # 将传入的正则表达式字符串分割成列表
    pattern_list = re.split(r',\s*', patterns)
    # 使用正则表达式分割句子
    words = re.split(r',\s*', sentence)
    # 初始化一个空列表来存放过滤后的词
    filtered_words = []
    # 遍历原始单词列表
    for word in words:
        # 检查当前单词是否与任一正则表达式匹配
        should_remove = False
        for pattern in pattern_list:
            if re.match(pattern, word):
                should_remove = True
                break
        # 如果当前单词不匹配任何正则表达式，则添加到过滤后的列表中
        if not should_remove:
            filtered_words.append(word)
    # 重新组合成字符串
    result = ', '.join(filtered_words)
    return result
