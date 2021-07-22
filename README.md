# dcinside-scraper
- A dcinside-scraper is a DCinside scraping tool written in Python. 
- This script was used for collecting fandom collaboration data in our paper, *"Behind the scenes of K-pop fandom: unveiling K-pop fandom collaboration network"*.

## Requirements
- Python>=3.6
- scrapy>=2.5.0

## Installing
**Git:**
```bash
git clone https://github.com/ji1kang/dcinside-scraper
cd dcinside-scraper
pip3 install . -r requirements.txt
```

## How to collect data
Set-up the project folder, where you clone this repository, in `idoldc/settings.py`:
```python
PROJECT_URL = "/home/username/dcinside-scraper"
```

Download the latest **5 pages** from **MIYAWAKI SAKURA** **minor** gallery:
```bash
scrapy crawl idoldc -a BASEURL=https://gall.dcinside.com/mgallery/board/lists?id=sakura0319 -a N=5
```

The collected data will be saved as JSON in a `data` folder in your project folder. 
An example of JSON as follows: 
```JSON
[{"error": false,
 "gall_count": "34",
 "gall_recommend": "0",
 "gall_type": "mgallery",
 "gallery": "sakura0319",
 "post_id": "3660470",
 "post_type": "icon_pic",
 "referer": "http://gall.dcinside.com/mgallery/board/lists?id=sakura0319&page=2&list_num=100",
 "reply_num": "4",
 "title": "사쿠라 귀여워",
 "uploaded_date": "2021-07-22 23:12:32",
 "url": "/mgallery/board/view/?id=sakura0319&no=3660470",
 "userid": "fiesta",
 "userip": "",
 "usernick": "user-nick-name"}]
```

## Citatation
```latex
@article{kang2021behind,
  title={Behind the scenes of K-pop fandom: unveiling K-pop fandom collaboration network},
  author={Kang, Jiwon and Kim, Jina and Yang, Migyeong and Park, Eunil and Ko, Minsam and Lee, Munyoung and Han, Jinyoung},
  journal={Quality \& Quantity},
  pages={1--22},
  year={2021},
  publisher={Springer}
}
```