# -*-coding:utf-8 -*-

"""
# File       : guest_user.py
# Time       : 2025-01-15 14:42:59
# Author     : lyx
# version    : python 3.11
# Description: 访客
"""
class GuestUser(object):

    id: str = None
    username: str = None
    password: str = None
    nickname: str = None
    avatar: str = None
    email: str = None
    mobile: str = None
    
    def __init__(self, id: str, username: str = None, password: str = None, nickname: str = None, avatar: str = None, email: str = None, mobile: str = None) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatar = avatar
        self.email = email
        self.mobile = mobile
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "email": self.email,
            "mobile": self.mobile
        }