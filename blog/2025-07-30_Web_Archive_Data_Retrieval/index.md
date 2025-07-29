I was hitted with a huge case of nostalgia recently, so I went digging quite deep on the internet only to find out the creator went quite far into deleting their work off the internet for some unknown reason.

So I went digging deep into the Internet Archive to find any trace of the works.

Found out the Internet Archive has an API to search with filter which was much better than crawling the website.

https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md

As the creator wanted to hide away their past, I will just give an example of what I did using my website instead.

First I used the cdx api on the internet archive to fetch all the pages on their domain:

```
wget -O cdx.json 'https://web.archive.org/cdx/search/cdx?url=asl97.github.io&matchType=prefix&output=json'
python gen_page_links.py > links
```

And extract the links from the cdx json

```python
#gen_page_links.py
import json
import zipfile

with open('cdx.json') as f:
    urls_list = json.load(f)

for urlkey, timestamp, original, mimetype, statuscode, digest, length in urls_list[1:]:
    if statuscode == "200":
        print(f'https://web.archive.org/web/{timestamp}id_/{original}')

```

Using my domain as an example isn't very good since it has a lot of binary files but the creator website in question only has webpages and their binary is in a sub-domain

We downloads all their webpages using wget

```
wget -i links -x
```

Now we just extract all the links

```
python extract_links.py > filelinks
```

```python
# extract_links.py
import os
import re

links = set()

for [path, dirs, files] in os.walk("web.archive.org/web"):
    for f in files:
        with open(os.path.join(path, f), 'rb') as fo:
            data = fo.read()
            for link in re.findall(b"'(https?://.*?)'", data):
                if link not in links:
                    print(link.decode('utf-8'))
                    links.add(link)
            for link in re.findall(b'"(https?://.*?)"', data):
                if link not in links:
                    print(link.decode('utf-8'))
                    links.add(link)
```

From here, it would be site specific and what you are trying to pull, in the creator case, I pull each sub-domain using the cdx again, but for my example, I would instead pull other github.io domain I uses in my website

```
python extract_subdomain_to_cdx_links.py filelinks >> cdx_links
```

```python
# extract_subdomain_to_cdx_links.py
import sys
import re

elinks = set()
with open(sys.argv[1]) as f:
    for link in f.readlines():
        for elink in re.findall('https?://(.*?).github.io/', link):
            elinks.add(elink)

selinks = sorted(elinks)
for sub in selinks:
    print(f'https://web.archive.org/cdx/search/cdx?url=http://{sub}.github.io/&matchType=prefix&output=json')
```

Download all the cdx files and combine them into a giant list of link

```
wget -i cdx_links -x
cat web.archive.org/cdx/search/* > datalinksraw_unfiltered 
```

Filter out the valid link and the redirect link that need more processing

```
cat datalinksraw_unfiltered | grep ',"200",' > datalinksraw200
cat datalinksraw_unfiltered | grep ',"301",' > datalinksraw301
```

Now use a python script to resolve the 301 links
The resulting 301_datalinks_a is usable immediately
but the 301_filelinks need to get processed like filelinks 
```
python 301_process_to_link.py 301_filelinks 301_datalinks_a
```

```python
import requests
import sys
import re

server_and_path = sys.argv[1]
datalink = sys.argv[2]
print(f"Dumping all links found to '{server_and_path}' and 200 links to '{datalink}'")

s = requests.session()

# new source server to fetch cdx search in next step
new_slinks = set()
# new images found
new_oklinks = set()
with open('datalinks301') as f:
    for line in f.readlines():
        link = line.strip()
        print(f"loading {link}")
        while link:
            r = s.head(link)
            if 300 <= r.status_code < 400:
                nlink = r.headers['location']
                new_slinks.add(nlink)
                link = nlink
            elif 200 <= r.status_code < 300:
                new_slinks.add(link)
                new_oklinks.add(link)
                break
            else:
                # 400+ status code and other unknown code
                # link should already been added but no issue adding it again
                # as set will remove duplicate
                new_slinks.add(link)
                print(f'status code: {r.status_code}, url: {r.url}')
                break

with open(server_and_path, 'w') as f:
    for link in sorted(new_slinks):
        f.write(link+'\n')

with open(datalink, 'w') as f:
    for link in sorted(new_oklinks):
        f.write(link+'\n')
```

We now process the resolved 301 links to get more links if stuff was moved to a new subdomain

```
python extract_server_and_basepath_to_cdx_links.py 301_filelinks > 301_cdx_links
```

Download the rest of the cdx files, wget will skip existing files
```
# download the other cdx files
wget -i 301_cdx_links -x
```

Join the newly added cdx file together with everything else in an even bigger cdx raw file and filter out the valid links

```
cat web.archive.org/cdx/search/* > 301_datalinksraw_unfiltered
cat 301_datalinksraw_unfiltered | grep ',"200",' > 301_datalinksraw200
```

Now we just treat the raw data file as a jsonline like file and read line by line and skip the , or ] at the end of each line.

```
python data_to_links.py 301_datalinksraw200 > 301_datalinks200
```

```python
# data_to_links.py
import json
import sys

links = set()
with open(sys.argv[1]) as f:
    for line in f.readlines():
        urlkey, timestamp, original, mimetype, statuscode, digest, length = json.loads(line.strip()[:-1])
        links.add(f'https://web.archive.org/web/{timestamp}id_/{original}')

for link in sorted(links):
    print(link)
```

The resulting 301_datalinks200 can then be passed into wget or a better download manager to download everything and archive it all


##### Is there an existing Web Archive downloader?

Maybe, who knows.

##### Why was this blog post created?

Turns out there was a group archiving the works by the specific creator.

Guess they never turned to an archiver to help on their project.

And I found the group by chance and started researching and putting together something to pull everything off the internet archive.

For the few extra pieces that I managed to pull that they haven't already found.

And for the ton of very early content that I had stored on my hard disk.

They would like to credit me on their private website and unlisted webpages for the days worth of work I putted in.

So I am creating this blog post so they have a place to link to.

For those who knows, "2013 chocobo" ~~~~ <img src="./star.gif"></img>
____
ASL97 https://github.com/asl97
