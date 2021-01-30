moab_news_source_dict_list = [
    {
        "name":         "Utah Public Radio",
        "url":          "https://www.upr.org/term/moab",
        "links_xpath":  "//main//*[@property='dc:title']/a/@href",
    },
    {
        "name":         "KUER 90.1",
        "url":          "https://www.kuer.org/term/moab",
        "links_xpath":  "//*[@class='term-listing-heading']//*[@property='dc:title']/a/@href",
    },
    {
        "name":         "The Salt Lake Tribune",
        "url":          "https://www.sltrib.com/search/Moab",
        "links_xpath":  "//*[contains(concat(' ', normalize-space(@class), ' '), ' results-list ')]/article//*[contains(concat(' ', normalize-space(@class), ' '), ' resultText ')]/a/@href",
    },
    {
        "name":         "The New York Times",
        "url":          "https://www.nytimes.com/search?dropmab=false&query=%22Moab%22%2C%20Utah&sort=newest",
        "links_xpath":  "//a[contains(@href, 'searchResultPosition')]/@href",
    },
    {
        "name":         "KSL",
        "url":          "https://www.ksl.com/?sid=53574&nid=208&cx=partner-pub-3771868546990559%3Ar955z1-wmf4&cof=FORID%3A9&ie=ISO-8859-1&sa=Search&searchtype=kslcom&x=15&y=19&q=%22Moab%22#gsc.tab=0&gsc.q=%22Moab%22&gsc.sort=date&gsc.ref=more%3Aksl_news",
        "links_xpath":  "//*[@data-refinementlabel='ksl_news']/ancestor::*[contains(concat(' ', normalize-space(@class), ' '), ' gs-webResult ')]//a[@class='gs-title']/@href",
    },
    {
        "name":         "The Washington Post",
        "url":          "https://www.washingtonpost.com/newssearch/?query=Moab,%20Utah&sort=Date&datefilter=All%20Since%202005&contenttype=Article&contenttype=Video&contenttype=Photo%20Gallery&contenttype=Discussion&contenttype=Live_discussion",
        "links_xpath":  "//*[@class='pb-results-container']//a[@data-ng-bind-html='doc.headline']/@href",
    },
    {
        "name":         "KUTV",
        "url":          "https://kutv.com/search?find=Moab",
        "links_xpath":  "//*[contains(concat(' ', normalize-space(@class), ' '), ' sd-main-content ')]//li[contains(concat(' ', normalize-space(@class), ' '), ' teaser-list-item ')]/a/@href",
    },
]

moab_news_source_list = [
    NewsSource(from_dict = each_dict)
    for each_dict
    in moab_news_source_dict_list
]
