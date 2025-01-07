from faplus.utils import settings

apis = {}

if settings.DEBUG:

    from .views.tests import test_upload_view, test_download_view

    apis["/debug"] = [
        ("01", "/upload", test_upload_view, "测试文件上传"),
        ("02", "/donwload/{sn}", test_download_view, "测试文下载"),
    ]
