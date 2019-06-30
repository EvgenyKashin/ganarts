# From: https://stackabuse.com/asynchronous-vs-synchronous-python-performance-analysis/

import threading
import argparse
import requests


def create_parser():
    parser = argparse.ArgumentParser(
        description="Specify the number of threads to use"
    )

    parser.add_argument("-nt", "--n_threads", default=4, type=int)
    parser.add_argument("-nr", "--n_requests", default=100, type=int)

    return parser


def make_requests(session, n, url, name=""):
    for i in range(n):
        print(f"{name}: making request {i} to {url}")
        resp = session.get(url)
        if resp.status_code == 200:
            pass


def main():
    parsed = create_parser().parse_args()

    n_requests = parsed.n_requests
    n_requests_per_thread = n_requests // parsed.n_threads

    url = "http://localhost:5000/"
    session = requests.Session()

    threads = [
        threading.Thread(
            target=make_requests,
            args=(session, n_requests_per_thread, url, f"thread_{i}")
        ) for i in range(parsed.n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


main()
