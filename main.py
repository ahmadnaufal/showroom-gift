import requests
import time
import argparse

base_url = "https://www.showroom-live.com/api/live"
gift_free_url = "/gifting_free"
gift_point_url = "/gifting_point_use"

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

def main():
    parser = argparse.ArgumentParser(description='Gifting showroom for some period of time')
    parser.add_argument('gift_type', help='Gift type (free/point)')
    parser.add_argument('live_id', type=int, help='Showroom Live ID')
    parser.add_argument('--gift-id', dest='gift_id', type=int, default=1, help='Gift ID')
    parser.add_argument('--referer', type=str, default="https://www.showroom-live.com", help='Referer to put to header')
    parser.add_argument('--size', type=int, default=1, help='Number of gift item(s) will be sent per iteration (default: 1)')
    parser.add_argument('-n', type=int, default=1, help='How many iterations will be executed (default: 1)')
    parser.add_argument('--delay', type=int, default=1, help='Delay per iteration (in seconds)')
    parser.add_argument('--token', type=str, help='CSRF Token provided')

    args = parser.parse_args()
    #build request
    headers = header_template
    headers['Referer'] = args.referer
    req_body = {
        'gift_id': args.gift_id,
        'num': args.size,
        'live_id': args.live_id,
        'csrf_token': args.token,
        'isRemovable': True
    }
    req_url = base_url + (gift_point_url if args.gift_type == 'point' else gift_free_url)

    i = 0
    while i < args.n:
        r = requests.post(req_url, data=req_body, headers=headers)
        print(r.text)
        # do request
        time.sleep(args.delay)
        i += 1

if __name__ == '__main__':
    main()