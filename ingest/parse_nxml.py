"""
Parse Pubmed Open Access subset / non commercial XML files
https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/

Files are "encoded in the NLM/JATS DTD". This is a formal spec, but some XML files may be in an older, non-normative
    version that will look similar.
http://www.niso.org/apps/group_public/download.php/15933/z39_96-2015.pdf
"""
import html
from typing import Union

from lxml import etree


###
# Text cleanup and convenience functions
###
parser = etree.XMLParser(remove_blank_text=True)


def unescape_node(text: Union[str, list, None]) -> Union[str, None]:
    """
    Convert the text of a node from XML-escaped text to a more human-readable string for indexing
    """
    if isinstance(text, None):
        return None

    if isinstance(text, list):
        text = ' '.join(text)

    return html.unescape(text)


def one_or_none(results: list) -> Union[object, None]:
    """Get at most one text value, and apply human-friendly post-processing"""
    return unescape_node(results[0]) if results else None

#####
#  Precompiled xpath expressions to be used across all documents
#####
x_journal = etree.XPath('/article/front/journal-meta/journal-title-group/journal-title/text()')

x_article_meta = etree.XPath('/article/front/article-meta')
# Relative expressions; pass in the article_meta as root node to (maybe) save some searching
x_article_title = etree.XPath('title-group/article-title/text()')
# There may be multiple kinds of abstract; avoid confusion by only fetching one without modifier attributes
# Fetch abstract as list of strings
x_article_abstract = etree.XPath('abstract[not(@*)]/descendant-or-self::*/text()')
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
x_figure_captions = etree.XPath('//fig/caption/descendant-or-self::*/text()')

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
        "journal": one_or_none(x_journal(doc)),


        "title": one_or_none(x_article_title(article_meta)),
        ## TODO : add authors later
        #"authors": x_article_title(article_meta),  # List. Do we want to store in a particular form? May provide first, last, affiliation and sometimes even ids depending widely on record. Is a nested doc appropriate?
        "abstract": unescape_node(x_article_abstract(article_meta)),  # May be multiple entries, eg "abstract-type=graphical" vs regular
        "keywords": [unescape_node(s) for s in x_article_keywords(article_meta)],

        "body": unescape_node(x_body_text(doc)),
        #"figure_captions": x_figure_captions(doc),  # TODO: Convert to list and store separately. /fig/caption/(any child)?
        "acknowledgments": unescape_node(x_acknowledgements(doc)),

        #"pub_date",  ## Figure out best extraction at a later date
        #"volume",

        "pmid": one_or_none(x_article_pmid(article_meta)),
        "pmc": one_or_none(x_article_pmc(article_meta)),
        "doi": one_or_none(x_article_doi(article_meta))
    }

