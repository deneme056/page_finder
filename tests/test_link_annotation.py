import os.path

import page_finder

from util import extract_all_links

try:
    FILE = __file__
except NameError:
    FILE = './tests'

TESTDIR = os.getenv('TESTPATH',
                    os.path.dirname(os.path.realpath(FILE)))


def get_local_url(filename):
    return 'file:///{0}/{1}'.format(os.path.join(TESTDIR, 'data'), filename)


def test_hnews():
    link_annotation = page_finder.LinkAnnotation()
    link_annotation.load(
        extract_all_links(get_local_url('Hacker News 1.html')))
    link_annotation.mark_link('https://news.ycombinator.com/news?p=2')
    link_annotation.load(
        extract_all_links(get_local_url('Hacker News 2.html')))

    best = link_annotation.best_links_to_follow()

    assert(best[0] == 'https://news.ycombinator.com/news?p=2')
    assert(best[1] == 'https://news.ycombinator.com/news?p=3')

    link_annotation.prune(100)
    assert(len(link_annotation.links) <= 100)

    assert(best[0] == 'https://news.ycombinator.com/news?p=2')
    assert(best[1] == 'https://news.ycombinator.com/news?p=3')


def test_equal_distance():
    link_annotation = page_finder.LinkAnnotation()
    link_annotation.mark_link('http://page_1')
    more_links = [
        'http://page_2',
        'http://page_3',
        'http://page_4',
        'http://page_5',
        'http://page_6',
        'http://page_7',
    ]
    link_annotation.load(more_links)
    for link in more_links:
        assert link_annotation.is_follow_link(link)
