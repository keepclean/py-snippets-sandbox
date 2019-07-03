#!/usr/bin/env python3

import cachelib
import os
import requests
import urllib
import sys

API_HOST = os.environ.get("API_HOST", "https://jsonplaceholder.typicode.com/")
CACHE_TIMEOUT = os.environ.get("CACHE_TIMEOUT", 10)

cache = cachelib.MemcachedCache(["127.0.0.1:11211"])


def main():
    actions = {"users": get_json("/users")}
    users = get_with_cache("users", actions["users"])
    print(users)


def get_json(uri):
    headers = {"user-agent": "exporter", "accept-encoding": "gzip, deflate"}
    try:
        url = urllib.parse.urljoin(API_HOST, uri)
        r = requests.get(url, timeout=120, headers=headers)

        return r.json(), ""

    except Exception as e:
        return [], e


def get_with_cache(key, func):
    """
    Logic here is simple, but the code is not obvious and needs some
    refactoring

    1. If there's no key (and for long cache as well) in cache
        1.1 function queries API
        1.2 if a response isn't valid => exporter exits
        1.3 otherwise it stores the response in short and long term caches

    2. If one of the keys in caches, function queries the short term cache
        2.1 if there's data in it for that key => function returns data
        2.2 otherwise function queries API
            2.2.1 if a response valid => function stores response in both
            caches and returns a result of the response
            2.2.2 if not, then the function tries get data for the key from
            the long term cache and export may exit if there's no data for
            key in it

    TODO: refactor that function
    """
    value = list()

    if not has_key(key) and not has_key(key + "60s"):
        value, err = func

        if not value:
            sys.exit(
                (
                    "ERROR: No data for {} in short and long caches;\n"
                    "ERROR: Unable to get data from API: {}"
                ).format(key, err)
            )

        set_cache(key, value)
        set_cache(key + "60s", value, timeout=60)

        print("return data from API")
        return value

    value = get_cache(key)
    if value:
        print("return data from short cache")
        return value

    value, err = func
    if value:
        set_cache(key, value)
        set_cache(key + "60s", value, timeout=60)

        print("return data from API 2")
        return value

    value = get_cache(key + "60s")
    if value is None:
        sys.exit(
            "ERROR: No data for {} in short and long caches;\n"
            "ERROR: Unable to get data from API: {}"
        ).format(key, err)

    print("return data from long cache")
    return value


def has_key(key):
    return cache.has(key)


def get_cache(key):
    return cache.get(key)


def set_cache(key, value, timeout=CACHE_TIMEOUT):
    cache.set(key, value, timeout=timeout)


if __name__ == "__main__":
    main()
