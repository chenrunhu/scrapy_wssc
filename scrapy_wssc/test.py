# -*- coding: utf-8 -*-
import re

import bs4

if __name__ == '__main__':
    str = '4545212.html'
    patten = re.compile(r'^\d+.html')
    if patten.search(str):
        print patten.search(str).group()

    html = u"""<div id="list">
                <dl>
                    <dt>《汉末武圣》最新章节（提示：已启用缓存技术，最新章节可能会延时显示，登录书架即可实时查看。）</dt>
                    <dd> <a style="" href="4760651.html">第两百二十六章 巅峰决战 下</a></dd>
                    <dd> <a style="" href="4760650.html">第两百二十五章 巅峰决战 中</a></dd>
                    <dt>《汉末武圣》正文卷</dt>
                    <dd> <a style="" href="/book/84466/4350297.html">第一章 北地烽烟</a></dd>
                    <dd> <a style="" href="/book/84466/4350298.html">第二章 离家</a></dd>
                </dl>
            </div>
        """
    soup = bs4.BeautifulSoup(html, 'lxml')
    list = soup.find('div', id="list").dl.find_all('dt')[1].next_sibling.next_sibling.a.attrs['href']
    print list
    for child in list:
        print child

