from bs4 import BeautifulSoup
import requests
import re
import time
import sys


visited = []

def check_in_tag(content_div, tag):
    global visited

    valid_link = None
    tags = content_div.select(tag)
    found_link = False

    for t in tags:
        if t.find("a"):
            t_str = str(t)
            t_str_formatted = re.sub("\((.+?)\)", "", t_str) #remove paranthesis
            t_str_formatted = re.sub("\[(.+?)\]", "", t_str_formatted) #remove square brackets
            s = BeautifulSoup(t_str_formatted, "html.parser")  #beautiful soup object
            a_list = s.find_all("a") #list of links

            for a_elem in a_list:

                if a_elem.get('href') and '#' in a_elem.get('href'):
                    continue
                elif a_elem.get('href'):
                    valid_link = a_elem.get('href')
                    if valid_link in visited:
                        print(f"loop detected of link {valid_link}")
                        return True, None
                    else:
                        visited.append(valid_link)
                        break
            if valid_link is not None:
                found_link = True
                break

    return found_link, valid_link

def first_valid_link(url):
    global visited
    src_code = requests.get(url)
    plain_text = src_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    print(f"Title = {soup.title.string}:  {url}")

    content_div = soup.find("div", {"class":"mw-parser-output"})

    p_links_found, valid_link = check_in_tag(content_div, "p")
    a_links_found = False

    if p_links_found == False:
        a_links_found, valid_link = check_in_tag(content_div, "li")



    if valid_link is None:
        print("No valid first link!")
        return
    elif (soup.title.string == "Philosophy - Wikipedia"):
        print("reached the end Philosophy")
        return
    else:
        time.sleep(0.5)
        first_valid_link("https://en.wikipedia.org" +valid_link)



if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print("Usage: python3 getting_to_philosophy.py <wikipedia link>")
        print("OR generate random link: python3 getting_to_philosophy.py -r")
    else:
        url = str(sys.argv[1])
        if url == "-r":
            url = "https://en.wikipedia.org/wiki/Special:Random"
        first_valid_link(url)
