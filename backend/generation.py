"""提示词生成逻辑。"""

from backend import model
from backend.config import locale


##########################

# 生成提示词
def gen_prompt(quality_tags, mode_tags, length_tags, tags, max_token, temp, Seed, top_p, min_p, top_k, rating,
               artist, characters, meta, length, width):
    aspect_ratio = round(length / width, 1)

    llm = model.llm
    if llm is None:
        return locale["model_not_loaded"]
    else:
        if mode_tags == "None" or mode_tags == "tag_to_long" or mode_tags == "tag_to_short_to_long":
            output = llm.create_completion(
                f"quality: {quality_tags}\naspect ratio: {aspect_ratio}\ntarget: <|{length_tags}|> <|{mode_tags}|>\nrating: {rating}\nartist: {artist}\ncharacters: {characters}\nmeta: {meta}\ntag: {tags}",
                max_tokens=max_token,
                echo=True,
                temperature=temp,
                seed=Seed,
                top_p=top_p,
                min_p=min_p,
                top_k=top_k
            )
        elif mode_tags == "long_to_tag":
            output = llm.create_completion(
                f"quality: {quality_tags}\naspect ratio: {aspect_ratio}\ntarget: <|{length_tags}|> <|{mode_tags}|>\nrating: {rating}\nartist: {artist}\ncharacters: {characters}\nmeta: {meta}\nlong: {tags}",
                max_tokens=max_token,
                echo=True,
                temperature=temp,
                seed=Seed,
                top_p=top_p,
                min_p=min_p,
                top_k=top_k
            )
        else:
            output = llm.create_completion(
                f"quality: {quality_tags}\naspect ratio: {aspect_ratio}\ntarget: <|{length_tags}|> <|{mode_tags}|>\nrating: {rating}\nartist: {artist}\ncharacters: {characters}\nmeta: {meta}\nshort: {tags}",
                max_tokens=max_token,
                echo=True,
                temperature=temp,
                seed=Seed,
                top_p=top_p,
                min_p=min_p,
                top_k=top_k
            )

        return output['choices'][0]['text']
