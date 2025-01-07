import hashlib
import random
import string

def md5_encrypt(plaintext: str) -> str:
    """
    对输入的字符串进行 MD5 哈希加密。
    :param plaintext: 要加密的字符串
    :return: MD5 哈希值（32 字符长的十六进制字符串）
    """
    md5_hash = hashlib.md5()
    md5_hash.update(plaintext.encode('utf-8'))
    return md5_hash.hexdigest()

def generate_replacement_rule(seed: str) -> dict:
    """
    生成一个固定的字符替换规则。使用哈希值作为种子来生成伪随机替换规则。
    :param seed: 用于生成替换规则的种子（例如 MD5 哈希）
    :return: 字符替换的映射字典
    """
    random.seed(seed)  # 固定随机种子，确保相同输入得到相同的替换规则
    
    # 字符集，可以选择替换的字符范围
    all_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    replace_rule = {}
    
    # 随机生成替换规则
    for char in all_chars:
        # 为每个字符生成一个随机替代字符
        replace_rule[char] = random.choice(all_chars)
    
    return replace_rule

def encrypt(plaintext: str, length: int = 32, replace: bool = False) -> str:
    """
    对输入的字符串进行 MD5 哈希加密，并进行进一步的复杂操作（如替换、截取等）。
    :param plaintext: 要加密的字符串
    :param length: 结果字符串的长度（默认为 32）
    :param replace: 是否进行替换操作（默认为 False）
    :return: 加密并处理后的字符串
    """
    # 进行 MD5 哈希加密
    result = md5_encrypt(plaintext)

    # 生成固定的替换规则
    replace_rule = generate_replacement_rule(result)

    # 执行替换操作
    if replace:
        result = ''.join([replace_rule.get(c, c) for c in result])

    # 截取指定长度
    if length != 32:
        result = result[:length]

    return result