import requests
import os
import sys
import re
from colorama import *
from urllib.parse import urlparse


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


init(autoreset=True) # reset color after each print

def banner():
    print(f"""{Fore.CYAN}
                                                                     
,--.   ,--.        ,--.    ,------.,--.           ,--.              
|  |   `--',--,--, |  |,-. |  .---'`--',--,--,  ,-|  | ,---. ,--.--.
|  |   ,--.|      \\|     / |  `--, ,--.|      \\' .-. || .-. :|  .--'
|  '--.|  ||  ||  ||  \\  \\ |  |`   |  ||  ||  |\\ `-' |\\   --.|  |    
`-----'`--'`--''--'`--'`--'`--'    `--'`--''--' `---'  `----'`--'    
                                                                     
                    Short link Resolver
                    By: github.com/ZH4CK3DE


""")

def menu():
    print(f"\n{Fore.CYAN}[+] Enter URLs (one per line, press Enter twice when done) :")

def getKnownShorteners(): # known urls that provide url shortening services
    return [
        'bit.ly', 'bitly.com', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly',
        'is.gd', 'buff.ly', 'adf.ly', 'short.link', 'tiny.cc', 'lnkd.in',
        'youtu.be', 'fb.me', 'amzn.to', 'rebrand.ly', 'cutt.ly', 'v.gd',
        'git.io', 'go2l.link', 'hyperurl.co', 'chilp.it', 'x.co', 'budurl.com',
        'clickmeter.com', 'clkim.com', 'short.cm', 'branch.io', 'app.link',
        'sl.link', 'shortened.link', 'smarturl.it', 'linktr.ee', 'bio.link'
    ]

def isValidUrl(url):
    try:
        # add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # parsing the url 
        parsed = urlparse(url)
    
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # check if netloc contains a dot
        if '.' not in parsed.netloc:
            return False
            
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, parsed.netloc):
            return False
            
        return True
    except:
        return False

def isShortener(url):
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain in getKnownShorteners()
    except:
        return False

def resolveUrl(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

        print(f"{Fore.CYAN}[i] Resolving URL...")
        
        try:
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=15)
            final_url = response.url
        except:
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
            final_url = response.url

        if response.status_code in [200, 301, 302, 303, 307, 308]:
            if final_url != url:
                print(f"\n{Fore.GREEN}[i] Original : {url}")
                print(f"{Fore.GREEN}[i] Resolved : {final_url}")
                
                original_domain = urlparse(url).netloc
                resolved_domain = urlparse(final_url).netloc
                if original_domain != resolved_domain:
                    print(f"{Fore.GREEN}[i] Domain   : {original_domain} → {resolved_domain}")
            else: 
                print(f"{Fore.RED}[!] URL doesn't redirect or is already expanded") # no redirection
                print(f"{Fore.RED}{url}")
        else:
            print(f"{Fore.RED}[!] Error : HTTP {response.status_code}")
            if response.status_code == 403:
                print(f"{Fore.RED}[!] This website may be blocking automated requests")
            elif response.status_code == 429:
                print(f"{Fore.RED}[!] Rate limited - try again later")

    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[!] Error : Request timeout")
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}[!] Error : Connection failed")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error : {e}")
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error : {e}")

def collectUrls():
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        
        if isValidUrl(url):
            urls.append(url)
        else:
            print(f"{Fore.RED}[!] Invalid URL: {url}")
            print(f"{Fore.RED}[!] Please enter a valid URL")
    
    return urls

def main():
    while True:  # main loop to restart if no valid urls
        clear()
        banner()
        menu()
        
        urls = collectUrls()
        
        if not urls:
            print(f"{Fore.RED}[!] No valid URLs provided")
            restart = input(f"\n{Fore.YELLOW}[?] Do you want to try again? (y/n): ").strip().lower()
            if restart not in ['y', 'yes']:
                print(f"{Fore.CYAN}[i] Goodbye!")
                sys.exit(0)
            continue  # restart from the beginning
        
        print(f"\n{Fore.CYAN}[i] Resolving {len(urls)} URLs...")
        print("=" * 60)
        
        for i, url in enumerate(urls, 1):
            print(f"\n{Fore.CYAN}[{i}/{len(urls)}]")
            resolveUrl(url)
            if i < len(urls):
                print(f"{Fore.CYAN}{'-' * 40}")
        
        print(f"\n{Fore.GREEN}[i] Done ! Resolved {len(urls)} URLs")
        
        another = input(f"\n{Fore.YELLOW}[?] Do you want to process more URLs? (y/n) : ").strip().lower()
        if another not in ['y', 'yes']:
            print(f"{Fore.CYAN}[i] Goodbye!")
            break

if __name__ == "__main__":
    main()