import requests
from bs4 import BeautifulSoup as BS

# 文本列表页
index_page = requests.get('http://www.chinadmd.com/down/?q=6oxoore3sopvczapwousawvo')
soup = BS(index_page.text, 'lxml')
link_list = soup.find_all('a', target='_blank')
for image_num, link in enumerate(link_list):
    # 单个图片页
    image_page = requests.get(link['href']).text
    # 图片连接获取
    image_link = BS(image_page, 'lxml').find_all(
        'img', onload='AutotofuImage(600,400,this)')[0]['src']
    image = requests.get(image_link)
    with open('c:/answer/'+str(image_num)+'.png', 'ab') as img:
        img.write(image.content)
        img.close()
