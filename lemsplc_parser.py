import collections
import pyquery


Article = collections.namedtuple('Article', ['comments', 'link', 'text'])


def _strip_fragment(url):
    return url[:url.index('#')]


def front_page():
    pq = pyquery.PyQuery('http://www.marca.com')
    comment_links = pq('a[href*="js-comentar"]')

    def comment_link_to(_, e):
        pqe = pyquery.PyQuery(e)
        link = _strip_fragment(pqe.attr('href'))
        return Article(
            comments=int(pqe.find('.number-comments').text()),
            link=link,
            text=pq('a[href="{0}"]'.format(link)).text().strip()
        )

    return comment_links.map(comment_link_to)
