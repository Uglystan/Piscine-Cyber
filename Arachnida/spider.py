import sys
import os
import requests
from bs4 import BeautifulSoup

def use_case():
    print("Bad using. ./spider [-r] [-l length recursively] [-p path where store img] URL of WebSite\n")
    print("Option [-r] Active recursion use -l for specify depth\n")
    print("Option [-l] 1-99 (take only a digit parameter)\n")
    print("Option [-p] specified path where store image (must be a directory and correct right)\n")
    exit(1)   

def set_arg(arg):
    arguments = sys.argv
    
    if len(arguments) < 2 or len(arguments) > 7:
        use_case()
    if arg == "-r":
        if arg in arguments and arguments.count(arg) == 1:
            return (1)
        else:
            return (0)
    elif arg == "-l":
        if arg in arguments and arguments.count(arg) == 1:
            if arguments[arguments.index("-l") + 1].isdigit() == True:
                return (int(arguments[arguments.index("-l") + 1]))
            else:
                use_case()
        else:
            return (5)
    elif arg == "-p":
        if arg in arguments and arguments.count(arg) == 1:
            if os.path.exists(arguments[arguments.index("-p") + 1]) == True and os.path.isdir(arguments[arguments.index("-p") + 1]) == True and os.access(arguments[arguments.index("-p") + 1], os.W_OK) == True:
                return (arguments[arguments.index("-p") + 1])
            else:
                use_case()
        else:
            return ("./data/")
    elif arg == "url":
        try:
            req = requests.get(arguments[len(arguments) - 1])
            if req.status_code // 100 == 2:
                return (arguments[len(arguments) - 1])
            else:
                use_case()
        except Exception as e:
            print("URL not valid\n")
            use_case()

def download_img(image, storage_path, name):
    img_html = requests.get(image["src"])
    
    if img_html.status_code == 200:
        with open(name, 'wb') as f:
            f.write(img_html.content)
    else:
        print("No image in this site :", img_html)

def main():
    r_opt: int = set_arg("-r")
    l_opt: str = set_arg("-l")
    p_opt: int = set_arg("-p")
    url: str = set_arg("url")
    i: int = 0
    
    print(f"r_opt = {r_opt}, l_opt = {l_opt}, p_opt = {p_opt}, url = {url}\n")

    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    link_img = soup.find_all('img', src=True)
    for image in link_img:
        print(f"src = ", image["src"])
        download_img(image, p_opt, i)
        
    
    
    

if __name__ == "__main__":
    main()