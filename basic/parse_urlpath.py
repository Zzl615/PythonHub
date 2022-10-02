# -*- coding: utf-8 -*-
# @Author: Noaghzil
# @Date:   2022-10-02 18:36:13
# @Last Modified by:   Noaghzil
# @Last Modified time: 2022-10-02 18:41:28

from urllib import parse


def supple_params_of_urlpath(channel_name: str, uid: str) -> str:
    url_path = "https://nxx.com/soi/video/consultation"
    url_obj = parse.urlparse(url_path)
    params = {"name": channel_name, "uid": uid}
    query_url = parse.urlencode(params, True)
    entrance_urlpath = url_obj._replace(query=query_url).geturl()
    return entrance_urlpath


def main():
    urlpath = supple_params_of_urlpath(channel_name="test_channel", uid="123")
    print(f"Hello, World!, {urlpath}")


if __name__ == "__main__":
    main()
