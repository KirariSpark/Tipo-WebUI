"""提示词文本的解析、过滤与格式化。"""

import re


##########################

# 把 artist 放到末尾
def send_artist_to_end(text):
    pattern1 = r"\nartist:.*"
    # 移动到末尾
    text = re.sub(pattern1, "", text) + re.search(pattern1, text).group(0)
    # 去除末尾的换行
    text = text.rstrip("\n")
    return text


##########################

# 格式化输出
def extract_and_format(model_out, mode_tags):
    if mode_tags == "None":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'tag']
    elif mode_tags == "tag_to_long":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'tag', 'long']
    elif mode_tags == "tag_to_short_to_long":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'tag', 'short', 'long']
    elif mode_tags == "long_to_tag":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'long', 'tag']
    elif mode_tags == "short_to_long":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'short', 'long']
    elif mode_tags == "short_to_tag_to_long":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'short', 'tag', 'long']
    elif mode_tags == "short_to_long_to_tag":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'short', 'long', 'tag']
    elif mode_tags == "short_to_tag":
        fields_to_extract = ['quality', 'artist', 'characters', 'meta', 'rating', 'short', 'tag']
    else:
        print("Error: Invalid mode_tags value")
        return "Error: Invalid mode_tags value"

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
