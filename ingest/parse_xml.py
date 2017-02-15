"""
Parse Pubmed Open Access subset / non commercial XML files
https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/

Files are "encoded in the NLM/JATS DTD". This is a formal spec, but some XML files may be in an older, non-normative
    version that will look similar.
http://www.niso.org/apps/group_public/download.php/15933/z39_96-2015.pdf
"""
import lxml


def parse_xml(fn: str):
    """
    Parse xml contents and return (SOMETHING)
    :param fn:
    :return:
    """
    # TODO: Any of these entries, realistically, will need to be HTML-unescaped if entities are found.
    return {
        "journal",

        "title",
        "authors",  # List. Do we want to store in a particular form? May provide first, last, affiliation and sometimes even ids depending widely on record. Is a nested doc appropriate?
        "abstract",  # May be multiple entries, eg "abstract-type=graphical" vs regular
        "keywords" , # List of items

        "body",  # Body section. May need to decode HTML entities to unicode, and get content of all child tags regardless of nesting. (then space-join maybe?)
        "figure_captions",  # Store these separately. /fig/caption/(any child)?
        "acknowledgments",  # Might be interesting to see who gets acknowledged a lot?

        "pub_date",
        "volume",



        "pmid",
        "pmc",
        "doi"

    }

