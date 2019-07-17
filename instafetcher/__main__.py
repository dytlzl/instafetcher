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
        if "https://www.instagram.com/p/" in url:
            shortcode = re.search(r'https://www\.instagram.com/p/(.*?)/', url).groups()[0]
            instafetcher.Post(shortcode).fetch()
        elif "https://www.instagram.com/explore/tags/" in url:
            tag = re.search(r'https://www\.instagram.com/explore/tags/(.*?)/', url).groups()[0]
            instafetcher.Tag(tag).fetch()
        elif "https://www.instagram.com/" in url:
            username = re.search(r'https://www\.instagram.com/(.*?)/', url).groups()[0]
            instafetcher.Profile(username).fetch()
        else:
            print('Invalid URL')
    except IndexError:
        print('Invalid URL')


if __name__ == "__main__":
    main()
