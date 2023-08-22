import collections
import json
from urllib import request

import pyquery


BASE_URL = 'https://www.marca.com/'


Article = collections.namedtuple('Article', ['comments', 'link', 'text'])


def _strip_fragment(url):
    return url[:url.index('#')]


def front_page():
    pq = pyquery.PyQuery(url=BASE_URL)
    comment_links = pq('a[href*="ancla_comentarios"]')

    def comment_link_to(_, e):
        pqe = pyquery.PyQuery(e)
        link = _strip_fragment(pqe.attr('href'))
        return Article(
            comments=int(pqe.children()[1].text),
            link=link[len(BASE_URL):],
            text=pq('a[href="{0}"]'.format(link)).text().strip()
        )

    return comment_links.map(comment_link_to)


DetailedArticle = collections.namedtuple('DetailedArticle', ['p_texts', 'comments'])
DetailedArticleComment = collections.namedtuple('DetailedArticleComment', ['user', 'body'])


def json_to_comment(json_):
    return DetailedArticleComment(user=json_['user'], body=json_['body'])


def get_detailed_article(url):
    pq = pyquery.PyQuery(url=BASE_URL + url)
    p_texts = pq('.ue-c-article__body').find('p').map(lambda _, e: pyquery.PyQuery(e).text())
    comment_id = pq('[data-commentId]').attr('data-commentid')
    page = 1
    comments = []
    while True:
        comments_url = 'http://www.marca.com/servicios/noticias/comentarios/comunidad/listarMejorValorados.html?noticia={0}&version=v2&pagina={1}'.format(comment_id, page)
        with request.urlopen(comments_url) as r:
            page_comments = json.loads(r.read().decode('utf-8'))["items"]
        if not page_comments:
            break
        comments += map(json_to_comment, page_comments)

        page += 1
        if page > 10:
            break
    return DetailedArticle(p_texts=p_texts, comments=comments)
