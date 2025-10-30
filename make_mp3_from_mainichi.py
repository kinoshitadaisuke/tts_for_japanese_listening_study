#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/10/30 09:28:00 (UT+08:00) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing urllib module
import urllib.request

# importing beautiful soup module
import bs4

# importing edge_tts module
import edge_tts

# importing asyncio module
import asyncio

# importing nest_asyncio module
import nest_asyncio

# importing pathlib module
import pathlib

# importing gtts module
import gtts.cli

# initialising a parser
descr  = f'Downloading Mainichi article and generating MP3 file'
parser = argparse.ArgumentParser (description=descr)

# adding arguments
list_tts = ['edge', 'gtts']
list_lang = ['ja']
list_gender = ['female', 'male']
dic_voice = {
    'female': 'ja-JP-NanamiNeural',
    'male':   'ja-JP-KeitaNeural',
}
parser.add_argument ('-u', '--url', default='', \
                     help='URL of Mainichi article')
parser.add_argument ('-t', '--tts', choices=list_tts, default='gtts', \
                     help='text-to-speech engine (default: gtts)')
parser.add_argument ('-a', '--audio', default='mainichi.mp3', \
                     help='output audio file')
parser.add_argument ('-g', '--gender', choices=list_gender, default='female', \
                     help='gender of synthesised speech (female or male)')
parser.add_argument ('-l', '--lang', choices=list_lang, default='ja', \
                     help='language option for gtts (default: ja)')

# parsing arguments
args = parser.parse_args ()

# input parameters
url_mainichi = args.url
file_audio   = args.audio
tts_engine   = args.tts
language     = args.lang
voice_gender = args.gender
voice_name   = dic_voice[voice_gender]

# text file name
path_audio = pathlib.Path (file_audio)
file_text = path_audio.stem + '.txt'

# checking URL
if not ('https://mainichi.jp/' in url_mainichi):
    # printing a message
    print ("ERROR:")
    print ("ERROR: specified URL is not for Mainichi article.")
    print ("ERROR:")
    # exit
    sys.exit (0)

# fetching HTML file
with urllib.request.urlopen (url_mainichi) as fh_in:
    html_mainichi = fh_in.read ().decode ('utf-8')

# creating BeautifulSoup object
soup = bs4.BeautifulSoup (html_mainichi, 'html.parser')

# extracting article type
article_type = soup.find ('p', class_='articledetail-head-shoulder').get_text ()

# making a plain text article
if ('余録' in article_type):
    # extracting article title and body
    html_article_title = soup.find ('h1', class_='title-page')
    html_article_body  = soup.find ('section', class_='articledetail-body').find ('p')
    # converting HTML into plain text
    text_article_title = html_article_title.get_text ()
    text_article_body  = html_article_body.get_text ()
    text_article_body  = text_article_body.replace ('▲', '。\n\n')
elif ('ニュースのことば' in article_type):
    # extracting article title and body
    html_article_title = soup.find ('h1', class_='title-page')
    html_article_body  = soup.find ('section', class_='articledetail-body').find_all ('p')
    # converting HTML into plain text
    text_article_title = html_article_title.get_text ()
    text_article_body = ''
    for i in range (len (html_article_body)):
        text_article_body += html_article_body[i].get_text ()
    text_article_body  = text_article_body.replace ('　', '\n\n')
    text_article_title = text_article_title.replace ('　', '\n\n')
elif ('ＮＥＷＳの窓' in article_type):
    # extracting article title and body
    html_article_title = soup.find ('h1', class_='title-page')
    html_article_body  = soup.find ('section', class_='articledetail-body').find_all ('p')
    # converting HTML into plain text
    text_article_title = html_article_title.get_text ()
    text_article_body = ''
    for i in range (len (html_article_body) - 1):
        text_article_body += html_article_body[i].get_text ()
    text_article_body  = text_article_body.replace ('　', '\n\n')
    text_article_title = text_article_title.replace ('　', '\n\n')
elif ('毎小ニュース' in article_type):
    # extracting article title and body
    html_article_title = soup.find ('h1', class_='title-page')
    html_article_body  = soup.find ('section', class_='articledetail-body').find_all ('p')
    # converting HTML into plain text
    text_article_title = html_article_title.get_text ()
    text_article_body = ''
    for i in range (len (html_article_body)):
        text_article_body += html_article_body[i].get_text ()
    text_article_body  = text_article_body.replace ('　', '\n\n')
    text_article_title = text_article_title.replace ('　', '\n\n')
else:
    print (f'# ERROR:')
    print (f'# ERROR: non-supported article type')
    print (f'# ERROR:')
    sys.exit (0)

# combining title and body
text_article = f'{text_article_title}\n\n{text_article_body}'

# writing extracted plain text into a file
with open (file_text, 'w') as fh_out:
    fh_out.write (text_article)

if (tts_engine == 'edge'):
    async def make_mp3_async (text, voice, file_output):
        communicate = edge_tts.Communicate (text, voice)
        await communicate.save (file_output)

    #def make_mp3 (text, voice, file_output):
    #    communicate = edge_tts.Communicate (text, voice)
    #    communicate.save_sync (file_output)

    # making MP3 file
    asyncio.run (make_mp3_async (text_article, voice_name, file_audio))
    #make_mp3 (text_article, voice_name, file_audio)
elif (tts_engine == 'gtts'):
    tts = gtts.gTTS (text=text_article, lang=language, tld='com')
    with open (file_audio, 'wb') as fh_out:
        tts.write_to_fp (fh_out)
