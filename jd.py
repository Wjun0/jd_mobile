# coding:utf8
import random
import json
import requests
from lxml.html import etree

#要爬取的商品信息
class Item(object):
    id = "123"
    image = "默认图片"
    price = "价格"
    description = "描述"
    store = "店铺"
    color = "[颜色列表]"
    version = "[版本型号列表]"
    weight = "重量"
    url = "商品url"



class Jd_mobile(object):
    def __init__(self):
        self.url = "https://list.jd.com/list.html?cat=9987,653,655"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
        }


    def parse(self,url):
        data = requests.get(url,headers=self.headers)
        html = etree.HTML(data.content.decode())
        item_lis = html.xpath('//*[@id="plist"]/ul/li')
        dic = {}
        for item in item_lis:
            image = item.xpath('./div/div[1]/a/img/@src')
            desc = item.xpath("./div/div[4]/a/em/text()")[0].strip()
            data_sku = item.xpath('./div/@data-sku')[0]
            venderid = item.xpath('./div/@venderid')[0]

            get_sku_url = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(data_sku)
            get_store_url = "https://rms.shop.jd.com/json/pop/shopInfo.action?ids={}".format(venderid)
            price_dic = requests.get(get_sku_url, headers=self.headers)
            stort_dic = requests.get(get_store_url, headers=self.headers)

            price = json.loads(price_dic.content.decode())[0]['p']
            store = json.loads(stort_dic.content.decode(encoding='GBK'))[0]['name']

            detail_url = item.xpath('./div/div[1]/a/@href')[0]
            detail_url = "https:{}".format(detail_url)

            detail_data = requests.get(detail_url,headers=self.headers)
            html = etree.HTML(detail_data.text)

            color = html.xpath('//*[@id="choose-attr-1"]/div/div/@data-value')
            version = html.xpath('//*[@id="choose-attr-2"]/div/div/@data-value')

            w_url = "https://c0.3.cn/stock?skuId={}&area=15_1243_3419_0&venderId={}&choseSuitSkuIds=&cat=9987,653,655".format(data_sku,venderid)
            print(data_sku)
            print(venderid)
            print(w_url)
            d = requests.get(w_url, headers = self.headers)
            weight = json.loads(d.content.decode("GBK"))['stock'].get("weightValue")



            dic['id'] = data_sku
            dic['image'] = image
            dic['price'] = price
            dic['description'] = desc
            dic['store'] = store
            dic['url'] = detail_url
            dic['color'] = color
            dic['version'] = version
            dic['weight'] = weight

            # print(dic)


    def get_url_list(self):  #拿到不同品牌的url_list
        param_url = "https://list.jd.com/list.html?cat=9987,653,655&md=1"
        data = requests.get(param_url)
        item_list = json.loads(data.content.decode())['brands']
        url_detail_list = []
        for i in item_list:
            base_url = "https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_"
            url = base_url + str(i['id'])
            url_detail_list.append(url)

        return url_detail_list


    def run(self):
        detail_url_list = self.get_url_list()
        # 调用多线程
        self.parse(detail_url_list[0])


if __name__ == '__main__':
    jd = Jd_mobile()
    jd.run()
    #爬取步骤
        # 确认爬取的字段
        #1，请求手机页面，拿到所有品牌的手机url
        #2, 分别请求所有的品牌url,拿到手机页面
        #3，实现单页的数据爬取
        #4，拿取翻页url,翻页爬取
        #5， 保存数据