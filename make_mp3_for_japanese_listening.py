#!/usr/bin/env python3

#
# Time-stamp: <2026/05/11 22:25:29 (UT+08:00) daisuke>
#

def main ():
    # importing argparse module
    import argparse
    # importing pathlib module
    import pathlib
    # importing urllib module
    import urllib.request
    # importing beautiful soup module
    import bs4
    # importing gtts module
    import gtts.cli

    # initialising a parser
    descr  = f'Downloading newspaper articles and generating MP3 files'
    parser = argparse.ArgumentParser (description=descr)

    # adding arguments
    list_tts = ['edge', 'gtts']
    list_lang = ['ja']
    list_gender = ['female', 'male']
    dic_voice = {
        'female': 'ja-JP-NanamiNeural',
        'male':   'ja-JP-KeitaNeural',
    }
    default_useragent = 'Mozilla/5.0 (X11; NetBSD x86_64; rv:140.0) Gecko/20100101 Firefox/140.0'
    parser.add_argument ('-t', '--tts', choices=list_tts, default='gtts', \
                         help='text-to-speech engine (default: gtts)')
    parser.add_argument ('-g', '--gender', choices=list_gender, \
                         default='female', \
                         help='gender of synthesised speech (female or male)')
    parser.add_argument ('-l', '--lang', choices=list_lang, default='ja', \
                         help='language option for gtts (default: ja)')
    parser.add_argument ('-u', '--useragent', \
                         default=default_useragent, \
                         help='user agent')
    parser.add_argument ('files', nargs='+', help='files')

    # parsing arguments
    args = parser.parse_args ()

    # input parameters
    list_files   = args.files
    tts_engine   = args.tts
    language     = args.lang
    voice_gender = args.gender
    voice_name   = dic_voice[voice_gender]
    user_agent   = args.useragent

    # processing files one-by-one
    for file_url in list_files:
        # extracting date (YYYYMMDD)
        path_url = pathlib.Path (file_url)
        date     = path_url.stem
        # opening file
        with open (file_url) as fh_in:
            # reading file line-by-line
            for line in fh_in:
                # skipping line if the line starts with '#'
                if (line[0] == '#'):
                    continue
                # extracting URL
                if (line[:8] == 'https://'):
                    url_article = line.strip ()
                    # downloading HTML files
                    if ('kids.gakken.co.jp' in url_article):
                        file_text = f'japanese_listening_{date}_gakken.txt'
                        file_mp3  = f'japanese_listening_{date}_gakken.mp3'
                    elif ('yasashii.asahi.com' in url_article):
                        file_text = f'japanese_listening_{date}_asahi.txt'
                        file_mp3  = f'japanese_listening_{date}_asahi.mp3'
                    elif ('www.yomiuri.co.jp' in url_article):
                        file_text = f'japanese_listening_{date}_yomiuri.txt'
                        file_mp3  = f'japanese_listening_{date}_yomiuri.mp3'
                    elif ('mainichi.jp' in url_article):
                        file_text = f'japanese_listening_{date}_mainichi.txt'
                        file_mp3  = f'japanese_listening_{date}_mainichi.mp3'
                    else:
                        continue
                print (f'now processing "{url_article}"...')
                print (f'  now downloading HTML file...')
                # request object
                req = urllib.request.Request (url_article)
                req.add_header ('User-Agent', user_agent)
                # opening URL
                with urllib.request.urlopen (req) as fh_in:
                    # downloading data
                    html_article = fh_in.read ().decode ('utf-8')
                print (f'  finished downloading HTML file!')
                print (f'  now extracting article from HTML file...')
                # creating BeautifulSoup object
                soup_article = bs4.BeautifulSoup (html_article, 'html.parser')
                # extracting article content
                if ('kids.gakken.co.jp' in url_article):
                    if (soup_article.find ('h1', class_='level_01')):
                        html_title = soup_article.find ('h1', class_='level_01')
                        text_title = html_title.get_text ()
                    if (soup_article.find ('div', class_='article_con')):
                        html_body = soup_article.find ('div', class_='article_con')
                        text_body = html_body.get_text ()
                elif ('yasashii.asahi.com' in url_article):
                    if (soup_article.find ('h1', id='page-title')):
                        html_title = soup_article.find ('h1', id='page-title')
                        text_title = html_title.get_text ()
                    if (soup_article.find ('div', id='main')):
                        html_body = soup_article.find ('div', id='main')
                        text_body = html_body.get_text ()
                elif ('www.yomiuri.co.jp' in url_article):
                    if (soup_article.find ('h1', class_='title-article c-article-title')):
                        html_title = soup_article.find ('h1', class_='title-article c-article-title')
                        text_title = html_title.get_text ()
                    if (soup_article.find ('div', class_='p-main-contents')):
                        html_body = soup_article.find ('div', class_='p-main-contents')
                        text_body = html_body.get_text ()
                        text_body = text_body.replace ('　', '\n\n')
                elif ('mainichi.jp' in url_article):
                    if (soup_article.find ('h1', class_='title-page')):
                        html_title = soup_article.find ('h1', class_='title-page')
                        text_title = html_title.get_text ()
                    if (soup_article.find ('section', class_='articledetail-body')):
                        html_body = soup_article.find ('section', class_='articledetail-body').find ('p')
                        text_body = html_body.get_text ()
                        text_body = text_body.replace ('▲', '\n\n')
                # text body of the article
                text_article = f'{text_title}\n\n{text_body}'
                print (f'  finished extracting article from HTML file!')
                print (f'  now writing article into text file...')
                # writing text into file
                with open (file_text, 'w') as fh_out:
                    fh_out.write (text_article)
                print (f'  finished writing article into text file!')
                # making mp3 file
                print (f'  now, making MP3 file...')
                if (tts_engine == 'gtts'):
                    tts = gtts.gTTS (text=text_article, lang=language, tld='com')
                    with open (file_mp3, 'wb') as fh_out:
                        tts.write_to_fp (fh_out)
                print (f'  finished making MP3 file!')
                print (f'finished processing "{url_article}"...')

# if this file is executed in the top-level code environment
if (__name__ == '__main__'):
    # execute main function
    main ()
