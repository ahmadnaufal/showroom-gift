import requests
import time
import argparse

base_url = "https://www.showroom-live.com/api/live"
gift_free_url = "/gifting_free"
gift_point_url = "/gifting_point_use"

# seeds: seedA, seedB, seedC, seedB, seedE
seed_ids = [1501, 1502, 1503, 1504, 1505]
# stars: starA, starB, starC, starD, starE
star_ids = [1, 1001, 1002, 1003, 2]

header_template = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.showroom-live.com",
    "Connection": "keep-alive",
    "Cookie": "<insert-cookie-here>"
}

def build_request_props(args) -> (str, dict, dict):
    # build headers
    headers = header_template
    headers['Referer'] = args.referer

    # build request body
    body = {
        'gift_id': args.gift_id,
        'num': args.size,
        'live_id': args.live_id,
        'csrf_token': args.token,
        'isRemovable': True
    }

    # build url
    url = base_url + (gift_free_url if is_free_gift(args.gift_id) else gift_point_url)

    return url, headers, body

def is_free_gift(gift_id: int) -> bool:
    return gift_id in (seed_ids + star_ids)

def parse_response(response: requests.Response):
    parsed_resp = response.json()
    if parsed_resp['errors']:
        print("Error: [%d] %s" % (parsed_resp['errors'][0]['code'], parsed_resp['errors'][0]['message']))
    else:
        print(parsed_resp)

def main():
    parser = argparse.ArgumentParser(description='Gifting showroom for some period of time')
    parser.add_argument('live_id', type=int, help='Showroom Live ID')
    parser.add_argument('--gift-id', dest='gift_id', type=int, default=1, help='Gift ID')
    parser.add_argument('--referer', type=str, default="https://www.showroom-live.com", help='Referer to put to header')
    parser.add_argument('--size', type=int, default=1, help='Number of gift item(s) will be sent per iteration (default: 1)')
    parser.add_argument('-n', type=int, default=1, help='How many iterations will be executed (default: 1)')
    parser.add_argument('--delay', type=int, default=1, help='Delay per iteration (in seconds)')
    parser.add_argument('--token', type=str, help='CSRF Token provided')

    args = parser.parse_args()

    url, headers, body = build_request_props(args)

    i = 0
    while i < args.n:
        # do request
        r = requests.post(url, data=body, headers=headers)
        parse_response(r)
        time.sleep(args.delay)
        i += 1


if __name__ == '__main__':
    main()