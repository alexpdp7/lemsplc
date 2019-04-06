import collections
import json
from urllib import request

import pyquery


BASE_URL = 'https://www.marca.com/'


Article = collections.namedtuple('Article', ['comments', 'link', 'text'])


def _strip_fragment(url):
    return url[:url.index('#')]


def front_page():
    pq = pyquery.PyQuery(BASE_URL)
    comment_links = pq('a[href*="js-comentar"]')

    def comment_link_to(_, e):
        pqe = pyquery.PyQuery(e)
        link = _strip_fragment(pqe.attr('href'))
        return Article(
            comments=int(pqe.find('.number-comments').text()),
            link=link[len(BASE_URL):],
            text=pq('a[href="{0}"]'.format(link)).text().strip()
        )

    return comment_links.map(comment_link_to)


DetailedArticle = collections.namedtuple('DetailedArticle', ['p_texts', 'comments'])
DetailedArticleComment = collections.namedtuple('DetailedArticleComment', ['user', 'body'])


def json_to_comment(json_):
    return DetailedArticleComment(user=json_['user'], body=json_['body'])


def get_detailed_article(url):
    pq = pyquery.PyQuery(BASE_URL + url)
    p_texts = pq('.row.content.cols-30-70').find('p').map(lambda _, e: pyquery.PyQuery(e).text())
    comment_id = pq('[data-commentId]').attr('data-commentid')
    comments_url = 'http://www.marca.com/servicios/noticias/comentarios/comunidad/listarMejorValorados.html?noticia={0}&version=v2'.format(comment_id)
    with request.urlopen(comments_url) as r:
        comments = json.loads(r.read().decode('utf-8'))
    return DetailedArticle(p_texts=p_texts, comments=map(json_to_comment, comments['items']))
