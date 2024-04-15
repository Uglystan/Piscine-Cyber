import sys
import os
from bs4 import BeautifulSoup
import requests

request_headers = {
"Referer": "https://www.google.com/", 
"Connection": "keep-alive",
"Cache-Control": "max-age=0",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Sec-Fetch-Site": "none",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-User": "?1",
"Sec-Fetch-Dest": "document",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.9"
    }

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
        if arg in arguments and "-r" in arguments and arguments.count(arg) == 1:
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
            req = requests.get(arguments[len(arguments) - 1], headers=request_headers)
            # print(req.status_code)
            if req.status_code // 100 == 2:
                return (arguments[len(arguments) - 1])
            else:
                use_case()
        except Exception as e:
            print("URL not valid\n")
            use_case()

def download_img(image_url, storage_path, url_racine):
    img_html = None
    
    print(image_url["src"])
    
    if image_url["src"].find("https://") != -1 or image_url["src"].find("http://") != -1:
        img_html = requests.get(image_url["src"], request_headers)
    else:
        if image_url["src"][0] == '/' and image_url["src"][1] == '/':
            if url_racine.find("https://") != -1:
                img_html = requests.get("https:" + image_url["src"], request_headers)
            elif url_racine.find("http://") != -1:
                img_html = requests.get("http:" + image_url["src"], request_headers)
        elif image_url["src"][0] == '/' and image_url["src"][1] != '/':
            img_html = requests.get(url_racine + image_url["src"], request_headers)
    
    if img_html:
        with open(storage_path, 'wb') as f:
            f.write(img_html.content)


def find_links_with_depth(url, depth, current_depth=0):
    if depth == 0:
        return [url]
    if current_depth == depth:
        return []

    links = []
    
    try:
        html_page = requests.get(url, request_headers)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            links.append(link['href']) #Ajout de chaque lien a une liste
        
        if current_depth < depth:
            links.extend(find_links_with_depth(link['href'], depth, current_depth + 1)) #Fusion de 2 listes depth + 1
    except:
        print("Err\n")
        
    links.append(url)
    return links

def site_name(image):
    return (image["src"][image["src"].find("//") + 2:image["src"].find("/", (image["src"].find("//") + 2))])

def img_name(image):
    end_ext = ""
    i: int = image["src"].rfind('.')
    end_ext += image["src"][i]
    i+=1
    while i < len(image["src"]) and (image["src"][i].isalpha() == True or image["src"][i] == '.'):
        end_ext += image["src"][i]
        i += 1
    name = image["src"][image["src"].rfind("/") + 1:image["src"].rfind(".")]
    # ext = image["src"][image["src"].rfind("."):end_ext]
    name = name + end_ext
    return (name)

def main():
    r_opt: int = set_arg("-r")
    l_opt: int= set_arg("-l")
    p_opt: str = set_arg("-p")
    url: str = set_arg("url")
    
    if r_opt == 1:
        all_url = find_links_with_depth(url, l_opt)
        all_url_without_double = list(set(all_url))
    else:
        all_url = find_links_with_depth(url, 0)
        all_url_without_double = list(set(all_url))

    for link in all_url_without_double:
        file_name: int = 0
        
        try:
            html_page = requests.get(link, request_headers)
        except:
            continue
        
        soup = BeautifulSoup(html_page.content, 'html.parser')
        link_img = soup.find_all('img', src=True)
        print(link_img)
        for image in link_img:
            print(f"src = ", image["src"])
            if image["src"] != "":
                download_img(image, p_opt + site_name(image) + '-' + img_name(image), link[0:link.find("/", (link.find("//") + 2))])
                file_name+=1


if __name__ == "__main__":
    main()

#For bmp : https://onlinebitmaptools.com/create-transparent-bitmap
#For GIF : https://giphy.com/