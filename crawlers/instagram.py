import asyncio
import json
import pprint
import sys

import aiohttp
from bs4 import BeautifulSoup


async def fetch(session, url, proxy=None):
    async with session.get(url, proxy=proxy) as response:
        return await response.text()


def _find_shared_data(soup):
    tags = soup.find_all('script')
    for t in map(lambda t: t.get_text(), tags):
        if t.startswith('window._sharedData'):
            return t


def _get_json_from_text(text):
    start = text.find('{')
    end = text.rfind('}')
    return text[start:end+1]


def _get_shortcode_media(data_dict):
    post_page = data_dict.get('entry_data', {}).get('PostPage', [])
    return post_page[0].get('graphql', {}).get('shortcode_media', {})


def _get_nodes_from_sidecar(shortcode_media):
    edges = shortcode_media.get('edge_sidecar_to_children', {}).get('edges', [])  # core meida list
    return map(lambda e: e.get('node', {}), edges)


def _get_nodes(shortcode_media):
    typename = shortcode_media.get('__typename')
    if not typename:
        return []
    if typename == 'GraphSidecar':
        return _get_nodes_from_sidecar(shortcode_media)
    else:
        return (s for s in (shortcode_media, ))


def _get_src_from_node(node):
    key = 'video_url' if node.get('is_video', False) else 'display_url'
    return node.get(key, '')


def parse(html):
    soup = BeautifulSoup(html, features='html.parser')
    # return soup.prettify()
    shared_data = _find_shared_data(soup)
    json_data = _get_json_from_text(shared_data)
    data_dict = json.loads(json_data)
    shortcode_media = _get_shortcode_media(data_dict)
    nodes = _get_nodes(shortcode_media)
    src_list = map(_get_src_from_node, nodes)
    result = list(src_list)
    return result


async def crawl(url, proxy=None):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url, proxy)
        return parse(html)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # url = 'https://www.instagram.com/p/BqarTuBHdcC/?utm_source=ig_share_sheet&igshid=15n3gxl891200'  # 单图片
        url = 'https://www.instagram.com/p/BqcrITsAlqT/?utm_source=ig_share_sheet&igshid=dsxz8l9zogcv'  # 二连视频
        # url = 'https://www.instagram.com/p/Bqe1lQ_jsKr/?utm_source=ig_share_sheet&igshid=cbs6or0xuzao'  # 四连图片
    proxy = 'http://127.0.0.1:1087'

    async def main():
        result = await crawl(url, proxy)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(result)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
