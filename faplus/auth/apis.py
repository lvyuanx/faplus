from faplus.core import settings
from .views.user import login_view, logout_view

DEBUG = getattr(settings, "DEBUG", True)
FAP_LOGIN_URL = getattr(settings, "FAP_LOGIN_URL", None)

apis = {
    "": [
        ("09", "/login", login_view, "登录"),
        ("10", "/logout", logout_view, "登出"),
    ]
}


if DEBUG:
    from .views.encrypt_decrypt import (
        rsa_encrypt_view,
        rsa_decrypt_view,
        aes_decrypt_view,
        aes_encrypt_view,
        md5_encrypt_view,
        aes2_decrypt_view,
        aes2_encrypt_view,
    )

    from .views.user import create_user_view, test_view

    apis["/user"] = [
        ("07", "/create", create_user_view, "创建用户", {"tags": ["DEBUG"]}),
        ("08", "/test", test_view, "测试", {"tags": ["DEBUG"]}),
    ]

    apis["/crypto/rsa"] = [
        ("00", "/encrypt", rsa_encrypt_view, "RSA加密", {"tags": ["DEBUG"]}),
        ("01", "/decrypt", rsa_decrypt_view, "RSA解密", {"tags": ["DEBUG"]}),
    ]

    apis["/crypto/aes"] = [
        ("02", "/encrypt", aes_encrypt_view, "AES加密", {"tags": ["DEBUG"]}),
        ("03", "/decrypt", aes_decrypt_view, "AES解密", {"tags": ["DEBUG"]}),
    ]

    apis["/crypto/md5"] = [
        ("04", "/encrypt", md5_encrypt_view, "MD5加密", {"tags": ["DEBUG"]}),
    ]

    apis["/crypto/aes2"] = [
        ("05", "/encrypt", aes2_encrypt_view, "AES2加密", {"tags": ["DEBUG"]}),
        ("06", "/decrypt", aes2_decrypt_view, "AES2解密", {"tags": ["DEBUG"]}),
    ]
