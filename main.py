import requests
import os
import tqdm
import re
import json
# import xml.dom.minidom
# from urllib.request import urlopen
from lxml import etree  # 解析数据
import csv
# import parsel
from time import sleep




def main():
    while True:
        Menu()
        choice = int(input("请选择：\n"))
        if choice in [0,1,2,3,4,5]:
            if choice == 0:
                answer = input("您确定要退出系统吗？y/n\n")
                if answer == 'Y' or answer == 'y':
                    print('小爬欢迎您的下次使用！')
                    print("   ﾍ⌒ヽﾌ ")
                    print(" （　・ω・）　")
                    print("   / ~つと）")

                    break  # 退出系统
                else:
                    continue
            elif choice == 1:
                Get_Picture()       #获取图片
            elif choice == 2:
                Get_Fiction()       #获取小说
            elif choice == 3:
                Get_CloudMusic()         #获取网易云音乐
            elif choice == 4:
                Get_coronavirus_Data()      #获取有疫情数据
            elif choice == 5:
                Get_SportNews()
        else:
            print("请输入正确选项！！")


def Menu():
    print("================================小爬欢迎您============================")
    print("------------------------------查点什么呀？^_^-------------------------")
    print("---------------------------------------------------------------------")
    # print("   ﾍ⌒ヽﾌ \t\t\t1.图片")
    # print(" （　・ω・）　\t\t\t2.小说")
    # print("   / ~つと）\t\t\t3.网易云音乐")
    # print("\t\t\t\t4.疫情数据")
    # print("\t\t\t\t5.体育新闻")
    # print("\t\t\t\t0.退出")
    print("   ﾍ⌒ヽﾌ \t\t\t\t\t\t1.图片")
    print(" （　・ω・）　\t\t\t\t\t2.小说")
    print("   / ~つと）\t\t\t\t\t\t3.网易云音乐")
    print("\t\t\t\t\t\t\t\t4.疫情数据")
    print("\t\t\t\t\t\t\t\t5.体育新闻")
    print("\t\t\t\t\t\t\t\t0.退出")
    print("---------------------------------------------------------------------")


def Get_Picture():
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=11447910797017413454&ipn=rj&ct=201326592&is=&fp=result&fr=&word=%E5%88%98%E4%BA%A6%E8%8F%B2&cg=star&queryWord=%E5%88%98%E4%BA%A6%E8%8F%B2&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn=90&rn=60&gsm=5a&1649945363653="
    search = input("请输入要搜索的信息：\n")
    page = 0
    number = int(input("请输入要下载的图片数量；\n"))
    bar = tqdm.tqdm(total=number)
    #
    # url = f"https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111110&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word={name}"+"&oq=%E5%88%98%E4%BA%A6%E8%8F%B2&rsp=-1"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
        "Upgrade_Insecure_Requests": '1'
    }
    param = {
        'tn': 'resultjson_com',
        'logid': 8695852041715982282,
        'ipn': 'rj',
        'ct': 201326592,
        'is': '',
        'fp': 'result',
        'fr': '',
        'word': search,
        'cg': 'star',
        'queryWord': search,
        'cl': 2,
        'lm': -1,
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': -1,
        'z': '',
        'ic': 0,
        'hd': '',
        'latest': '',
        'copyright': '',
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': 0,
        'istype': 2,
        'qc': '',
        'nc': 1,
        'expermode': '',
        'nojc': '',
        'isAsync': '',
        'pn': str(60 * page),  # 显示页数
        'rn': number,  # 每页显示数目
        'gsm': '3c',
        "1650081377382": ""
    }

    resp = requests.get(url, headers=header, params=param)
    # res = resp.text
    resp_json = resp.json()
    # 解析json数据，格式转化，将resp转化为json格式
    data_list = resp_json['data']
    # print(data_list)

    # 提取有用的url
    lst = []  # 存文件的url
    for item in data_list:
        if len(item) != 0:
            lst.append(item['thumbURL'])
    for i in range(len(lst)):
        count = 60 * page + i
        number -= 1
        bar.update(1)
        if number == 0:
            break
    # print(lst)

    # 数据存储：重新发送请求获取数据&存储
    count = 0
    for item in lst:
        resp = requests.get(item, headers=header, params=param)
        count += 1
        page += 1
        # path = 'E:\Leaning\Python-code\SpiderSys\picturedownload\picture' + str(count) + '.jpg'
        # path = os.path.expanduser(path)
        with open('./picturedownload/' + str(count) + '.jpg', mode="wb") as file:
            file.write(resp.content)
    print("图片下载完成！")
    print("^_^")


def Get_coronavirus_Data():
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner"
    with open('data.csv', mode='a',newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['area', 'confirmedRelative', 'curConfirm', 'confirmed', 'died', 'crued'])
    header = {
        "upgrade-insecure-requests": '1',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    resp = requests.get(url, headers=header)
    html_data = resp.text
    component = re.findall('"component":\[(.*)\],', html_data)[0]  # 提取"caseList":[],返回列表，获取第一个内容
    # pprint.pprint(component)

    # 类型转化
    json_data = json.loads(component)  # 字符串转字典
    # pprint.pprint(json_data)

    caseList = json_data['caseList']
    for case in caseList:
        area = case['area']  # 城市
        confirmedRelative = case['confirmedRelative']  # 新增确诊人数
        curConfirm = case['curConfirm']  # 现有确诊人数
        confirmed = case['confirmed']  # 累计确诊
        died = case['died']  # 死亡人数
        crued = case['crued']  # 治愈人数
        print(area, confirmedRelative, curConfirm, confirmed, died, crued)

        # 保存
        with open('data.csv', mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([area, confirmedRelative, curConfirm, confirmed, died, crued])
    file.close()


def Get_Fiction():
    url = 'http://www.xbiquge.la/xiaoshuodaquan/'

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }

    all_book_r = requests.get(url, headers=headers)
    all_book_html = etree.HTML(all_book_r.content.decode('utf-8'))
    all_book_url = all_book_html.xpath('//div[@class="novellist"]/ul/li/a/@href')
    all_book_title = all_book_html.xpath('//div[@class="novellist"]/ul/li/a/text()')
    find_book = input('输入想下载的书名:')
    num = 0
    for book_title in all_book_title:
        if find_book == book_title:
            print('找到了，您要的', book_title + ' (*^▽^*)')
            book_url = all_book_url[num]
            book_r = requests.get(book_url, headers=headers)
            book_html = etree.HTML(book_r.content.decode('utf-8'))
            book_url = book_html.xpath('//div[@id="list"]/dl/dd/a/@href')
            chapter_title = book_html.xpath('//div[@id="list"]/dl/dd/a/text()')
            judge = os.path.exists('../小说/%s' % str(book_title))
            if not judge:
                os.makedirs('../小说/%s' % str(book_title))
            print('<------请输入数字(该小说共有%s章)------>' % len(chapter_title))
            download_book_start = int(input('输入从第几章开始下载：'))
            download_book_end = int(input('输入到第几章结束：'))
            chapter_num = 0
            for book_content_url in book_url[download_book_start - 1:download_book_end]:
                sleep(2)
                new_book_content_url = 'http://www.xbiquge.la' + book_content_url
                book_content_r = requests.get(new_book_content_url, headers=headers)
                book_content_html = etree.HTML(book_content_r.content.decode('utf-8'))
                book_content = book_content_html.xpath('//div[@class="box_con"]/div[@id="content"]/text()')
                with open('../小说/%s/%s.txt' % (str(book_title), chapter_title[download_book_start + chapter_num - 1]),
                          'w', encoding='utf-8') as write_content:
                    all_content = ''
                    for content in book_content:
                        all_content += content
                    write_content.write(all_content)
                    print(chapter_title[download_book_start + chapter_num - 1], '--下载成功')
                    chapter_num += 1
            print('全部下载完成')
            break
        elif num + 1 == len(all_book_title):
            print('抱歉查无此书,去其他站点看看呢(*￣︶￣)、')
        num += 1


def Get_CloudMusic():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }  # 请求头

    # 1、网易云音乐热歌榜页面地址
    url = "https://music.163.com/playlist?id=982566337"

    # 2、通过网址进入网站获取网页数据,获取响应
    response = requests.get(url, headers=headers)

    # 3、筛选想要的目标数据
    data = etree.HTML(response.text)  # 获取网页源代码，并将源代码转化为能被xpath匹配的格式，此处HTML必须大写
    music_list = data.xpath('//a[contains(@href,"/song?")]')  # 全文扫描查找符合指定条件的内容，并以列表的形式返回
    # print(music_list) #查看返回的列表
    # print(music_list)
    # 4、列表进行拆分并显示
    for music in music_list:
        href = music.xpath('./@href')[0]  # 上面返回的列表依然不是最终想要的，所以还需在当前节点下查找指定条件的内容
        # print('href:' + href)
        music_id = href.split('=')[1]  # 使用关键字split 从查找到的内容中截取自己想要的
        # print(music_id)
        if '$' in music_id:
            continue
        music_name = music.xpath('./text()')[0]  # 获取当前节点下的文本内容（此处是获取歌曲的名字）
        # print(music_name)
        if '$' in music_name:
            continue
        url_base = "http://music.163.com/song/media/outer/url?id="  # 定义下载接口

        music = requests.get(url_base + music_id, headers=headers)  # 获取音乐

        with open('./music/' + music_name + '.mp3', 'wb') as file:  # 保存音乐文件
            file.write(music.content)

        print(music_name + ' ok')  # 提示
    print("下载完毕！")
    file.close()


def Get_SportNews():
    import requests
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    import re
    import xml.dom.minidom

    doc = xml.dom.minidom.Document()
    root = doc.createElement('AllNews')
    doc.appendChild(root)
    # 用于爬取新浪体育的网页
    urls2 = ['http://sports.sina.com.cn/nba/25.shtml']

    def scrap():
        for url in urls2:
            count = 0  # 用于统计总共爬取新闻数量
            html = urlopen(url).read().decode('utf-8')
            # print(html)
            res = re.findall(r'<a href="(.*?)" target="_blank">(.+?)</a><br><span>', html)  # 用于爬取超链接和新闻标题

            for i in res:
                try:
                    urli = i[0]
                    htmli = urlopen(urli).read().decode('utf-8')
                    time = re.findall(r'<span class="date">(.*?)</span>', htmli)
                    time = ''.join(time)
                    resp = re.findall(r'<p>(.*?)</p>', htmli)
                    resp = ''.join(resp)
                    # subHtml=re.findall('',htmli)
                    nodeNews = doc.createElement('News')
                    nodeTopic = doc.createElement('Topic')
                    nodeTopic.appendChild(doc.createTextNode('sports'))
                    nodeLink = doc.createElement('Link')
                    nodeLink.appendChild(doc.createTextNode(str(i[0])))
                    nodeTitle = doc.createElement('Title')
                    nodeTitle.appendChild(doc.createTextNode(str(i[1])))
                    nodeTime = doc.createElement('Time')
                    nodeTime.appendChild(doc.createTextNode(str(time)))
                    nodeText = doc.createElement('Text')
                    nodeText.appendChild(doc.createTextNode(str(resp)))
                    nodeNews.appendChild(nodeTopic)
                    nodeNews.appendChild(nodeLink)
                    nodeNews.appendChild(nodeTitle)
                    nodeNews.appendChild(nodeTime)
                    nodeNews.appendChild(nodeText)
                    root.appendChild(nodeNews)
                    print(i)
                    print(time)
                    print(resp)
                    count += 1
                except:
                    print(count)
                    break

    scrap()
    fp = open('news1.xml', 'w', encoding="utf-8")
    doc.writexml(fp, indent='', addindent='\t', newl='\n', encoding="utf-8")
    fp.close()


if __name__ == '__main__':
    main()


