import os
import sys
from collections import deque
from colorama import Fore
import requests
from bs4 import BeautifulSoup

history = deque(maxlen=10)


def save_webpage(_filename, _folder_name, _content):
    with open(os.path.join(_folder_name, _filename), "w", encoding='utf-8') as f:
        f.write(_content)


def create_folder(_folder_name: str):
    if os.access(_folder_name, os.F_OK):
        pass
    else:
        os.mkdir(_folder_name)


# def validate_url(url: str):
#     if "." in url:
#         return True
#     return False


# def check_filename(_folder: str, _filename: str):
#     if _filename in os.listdir(_folder):
#         return True
#     return False


def get_page_content_from_file(_folder_name, _filename):
    with open(os.path.join(_folder_name, _filename), "r", encoding='utf-8') as f:
        output = f.read()
    return output


def get_page_content_from_url(url):
    r = requests.get(f"https://{url}")
    return r.text


def main():
    if len(sys.argv) < 2:
        exit(0)

    folder_name = sys.argv[1]
    create_folder(folder_name)

    while (url := input()) != "exit":
        i = url.rfind('.')
        url_basename = url[:i]
        if i < 0:
            print("Error: Incorrect URL")
        elif url == 'back':
            if len(history) > 1:
                history.pop()
                page_content = get_page_content_from_file(folder_name, history[-1])
                print(page_content)
        elif url_basename in os.listdir(folder_name):
            page_content = get_page_content_from_file(folder_name, url_basename)
            history.append(url_basename)
            print(page_content)
        else:
            page_content = get_page_content_from_url(url)
            soup = BeautifulSoup(page_content, 'html.parser')
            tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a']
            for tag in tags:
                for element in soup.find_all(tag):
                    if tag == 'a':
                        print(Fore.BLUE + element.text)
                    print(element.text)
            output = soup.get_text("\n", strip=True)
            print(output)
            save_webpage(url_basename, folder_name, output)
            history.append(url_basename)


if __name__ == '__main__':
    main()
