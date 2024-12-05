# coding:utf-8
import requests

import threading


class UrlFnc:
    @classmethod
    def send_request(cls, url, data, headers, results):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            results.append((response.status_code, response.json()))
        except requests.exceptions.RequestException as e:
            results.append(str(e))

    @classmethod
    def send_async_request(cls, url, data, headers):
        results = []

        thread = threading.Thread(target=cls.send_request, args=(url, data, headers, results))
        thread.start()
        thread.join()

        return results[0]

    @classmethod
    def send_async_requests(cls, url, data_list, headers):
        results = []
        threads = []

        for data in data_list:
            thread = threading.Thread(target=cls.send_request, args=(url, data, headers, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return results
