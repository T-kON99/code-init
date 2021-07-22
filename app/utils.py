def insert_src(lang: str, text: str) -> str:
    import config.config as config

    src_code = str(config.init_code.get(lang))
    src_comment = config.comments.get(lang)
    src_code = src_code.replace("$comment_open", src_comment[0])
    src_code = src_code.replace("$summary", text)
    src_code = src_code.replace("$comment_close", src_comment[1])
    return src_code
