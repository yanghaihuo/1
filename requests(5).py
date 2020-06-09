import requests
import time
from lxml import etree
import pandas as pd


# 获取详情页url
def get_detail_url(text):
    html = etree.HTML(text)
    trs = html.xpath('//table[@class="s_table"]//tr')
    for tr in trs[1:]:
        detail_url = 'http://dbpub.cnki.net/Grid2008/Dbpub/' + tr.xpath('./td/a/@href')[0]
        yield detail_url


# 解析详情页信息
def get_detail_text(url, count):
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.62 Safari/537.36 Edg/81.0.416.31'}
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    # 获取标题
    title = ''.join(html.xpath('//table[1]//td[2]/text()')).strip()
    print(f'正在保存 {title}')
    trs = html.xpath('//table[2]//tr')
    data = []
    for tr in trs[:-1]:
        data_1 = tr.xpath('./td/text()')
        data_2 = [item.strip() for item in data_1]
        if data_2:
            data.extend(data_2)
    headers = ['标题'] + [item[1:-1] for item in data[::2]]
    content = [title] + data[1::2] + [url]
    if count == 1:
        pd.DataFrame(columns=headers).to_csv('专利.csv', index=False, encoding='gbk')
    pd.DataFrame([content]).to_csv('专利.csv', index=False, header=False, mode='a+', encoding='gbk')


def main():
    headers = {
            'Uesr-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45',
            'Cookie': 'Ecp_ClientId=4200517191102693070; amid=9c5ff208-7ea6-4cc9-842c-50699c235aca; UM_distinctid=1722fbf8ee54bd-0c0b7c01417b27-70657c6e-100200-1722fbf8ee618d; Ecp_IpLoginFail=200608153.118.27.22; ASP.NET_SessionId=3gcx5bm4kubq1i45osaep345; AutoIpLogin=; LID=; SID=130102; CurTop10KeyWord=%2c%u4e0a%u6d77%u7535%u529b%u80a1%u4efd%u6709%u9650%u516c%u53f8; FileNameM=cnki%3A'
            }
    count = 1
    for i in range(1, 4):
        url = f'http://dbpub.cnki.net/Grid2008/Dbpub/brief.aspx?curpage={i}&RecordsPerPage=20&QueryID=63&ID=SCPD&turnpage=1&systemno=&NaviDatabaseName=SCPD_ZJCLS&NaviField=%e4%b8%93%e9%a2%98%e5%ad%90%e6%a0%8f%e7%9b%ae%e4%bb%a3%e7%a0%81&navigatorValue=&subBase=all'
        res = requests.get(url, headers=headers)
        for detail_url in get_detail_url(res.text):
            try:
                get_detail_text(detail_url, count)
            except:
                continue
            count += 1
            time.sleep(1)


if __name__ == '__main__':
    main()