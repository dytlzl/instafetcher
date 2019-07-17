import instafetcher
import sys
import re


def main():
    try:
        url = sys.argv[1]
        fetch(url)
    except IndexError:
        while True:
            in_str = input('URL>>')
            if in_str == 'exit' or in_str == 'quit':
                return
            fetch(in_str)


def fetch(url):
    try:
        if "instagram.com/p/" in url:
            shortcode = re.search(r'instagram.com/p/(.*?)/', url).groups()[0]
            instafetcher.Post(shortcode).fetch()
        elif "instagram.com/explore/tags/" in url:
            tag = re.search(r'instagram.com/explore/tags/(.*?)/', url).groups()[0]
            instafetcher.Tag(tag).fetch()
        elif "instagram.com/" in url:
            username = re.search(r'instagram.com/(.*?)/', url).groups()[0]
            instafetcher.Profile(username).fetch()
        else:
            print('Invalid URL')
    except (IndexError, AttributeError):
        print('Invalid URL')


if __name__ == "__main__":
    main()
