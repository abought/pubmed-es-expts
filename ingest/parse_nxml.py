"""
Parse Pubmed Open Access subset / non commercial XML files
https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/

Files are "encoded in the NLM/JATS DTD". This is a formal spec, but some XML files may be in an older, non-normative
    version that will look similar.
http://www.niso.org/apps/group_public/download.php/15933/z39_96-2015.pdf
"""
import datetime
import html
import logging
from typing import Union

from lxml import etree


logger = logging.getLogger(__name__)

###
# Text cleanup and convenience functions
###
parser = etree.XMLParser(remove_blank_text=True)


def unescape_text(text: Union[str, list, None]) -> Union[str, None]:
    """
    Convert the text of a node from XML-escaped text to a more human-readable string for indexing
    """
    if text is None:
        return None

    if isinstance(text, list):
        text = ' '.join(text)

    return html.unescape(text)


def one_or_none(results: list) -> Union[object, None]:
    """Return the first element of a list"""
    return unescape_text(results[0]) if results else None


def one_text(results: list) -> Union[str, None]:
    """Get at most one item, and apply human-friendly post-processing to text"""
    return unescape_text(one_or_none(results))


def pub_date_to_iso(pub_date_node) -> Union[str, None]:
    if pub_date_node is None:
        return None

    year = pub_date_node.findtext('year')
    month = pub_date_node.findtext('month')
    day = pub_date_node.findtext('day')

    # TODO: Improve handling of incomplete dates
    date = (year, month, day)
    if not all(date):
        logger.warning(f'Incomplete year definition {year} {month} {day}')
        return None
    else:
        date = [int(x) for x in date]
        return datetime.date(*date).isoformat()


def contrib_node_to_names(contrib_node) -> object:
    """Exract author info from a contributor node"""
    surname = contrib_node.find('name/surname')
    surname = None if surname is None else surname.text

    given_name = contrib_node.find('name/given-names')
    given_name= None if given_name is None else given_name.text

    if surname and given_name:
        full_name = ', '.join([surname, given_name])
    else:
        full_name = None

    if any([surname, given_name, full_name]):
        return {
            'surname': surname,
            'given-names': given_name,
            'full-name': full_name,
        }
    else:
        # This situation would be very surprising, but log to help us better understand the data
        logger.warning('Detected contributor record with no author name provided!')
        return None

#####
#  Precompiled xpath expressions to be used across all documents
#####
# Get text from any provided node
x_node_text = etree.XPath('descendant-or-self::*/text()')

x_journal = etree.XPath('/article/front/journal-meta/journal-title-group/journal-title/text()')

x_article_meta = etree.XPath('/article/front/article-meta')
# Relative expressions; pass in the article_meta as root node to (maybe) save some searching
x_article_pub_date = etree.XPath('pub-date')  # May be multiple pub dates, but- !- the pub-type/date-type attributes may contain inconsistent data
x_article_volume = etree.XPath('volume/text()')
x_article_issue = etree.XPath('issue/text()')
x_article_fpage = etree.XPath('fpage/text()')

x_article_title = etree.XPath('title-group/article-title/text()')
# There may be multiple kinds of abstract; avoid confusion by only fetching one without modifier attributes
# Fetch abstract as list of strings
x_article_abstract = etree.XPath('abstract')
x_article_keywords = etree.XPath('kwd-group/kwd/text()')

# Identifiers
x_article_pmid = etree.XPath('article-id[@pub-id-type="pmid"]/text()')
x_article_pmc = etree.XPath('article-id[@pub-id-type="pmc"]/text()')
x_article_doi = etree.XPath('article-id[@pub-id-type="doi"]/text()')

# Return a list of nodes (not text values)
x_article_authors = etree.XPath('contrib-group/contrib[@contrib-type="author"]')
x_article_editors = etree.XPath('contrib-group/contrib[@contrib-type="editor"]')

## These get a list of individual string segments; user can join into one string as needed
x_body_text = etree.XPath('/article/body/descendant-or-self::*/text()')
# Figures are allowed to appear many places in the document
## TODO: this gloms together every figure caption into one long list, which is not the desired behavior
x_figure_captions = etree.XPath('//fig/caption')

x_acknowledgements = etree.XPath('/article/back/ack/p/text()')


def parse_nxml(fn: str):
    """
    Parse xml contents and return (SOMETHING)
    :param fn:
    :return:
    """
    doc = etree.parse(fn, parser=parser)
    article_meta = x_article_meta(doc)[0]

    return {
        "journal": one_text(x_journal(doc)),

        "title": one_text(x_article_title(article_meta)),
        "authors": [contrib_node_to_names(n) for n in x_article_authors(article_meta)],

        # Each article can have multiple abstracts (eg graphical vs regular)
        "abstract": [unescape_text(x_node_text(n))
                     for n in x_article_abstract(article_meta)],
        "keywords": [unescape_text(s) for s in x_article_keywords(article_meta)],

        "body": unescape_text(x_body_text(doc)),
        "figure_captions": [unescape_text(x_node_text(n))
                            for n in x_figure_captions(doc)],
        "acknowledgments": unescape_text(x_acknowledgements(doc)),

        "date": pub_date_to_iso(one_or_none(x_article_pub_date(article_meta))),
        "volume": one_or_none(x_article_volume(article_meta)),
        "issue": one_or_none(x_article_issue(article_meta)),
        "fpage": one_or_none(x_article_fpage(article_meta)),

        "pmid": one_or_none(x_article_pmid(article_meta)),
        "pmc": one_or_none(x_article_pmc(article_meta)),
        "doi": one_or_none(x_article_doi(article_meta))
    }

