#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/10/22 22:22:16 (UT+08:00) daisuke>
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

# import asyncio module
import asyncio

# initialising a parser
descr  = f'Downloading Mainichi article and generating MP3 file'
parser = argparse.ArgumentParser (description=descr)

# adding arguments
list_gender = ['female', 'male']
dic_voice = {
    'female': 'ja-JP-NanamiNeural',
    'male':   'ja-JP-KeitaNeural',
}
parser.add_argument ('-u', '--url', default='', \
                     help='URL of Mainichi article')
parser.add_argument ('-t', '--text', default='mainichi.txt', \
                     help='output text file')
parser.add_argument ('-a', '--audio', default='mainichi.mp3', \
                     help='output audio file')
parser.add_argument ('-g', '--gender', choices=list_gender, default='female', \
                     help='gender of synthesised speech (female or male)')
parser.add_argument ('-e', '--edgetts', default='edge-tts', \
                     help='edge-tts command')

# parsing arguments
args = parser.parse_args ()

# input parameters
url_mainichi    = args.url
file_text       = args.text
file_audio      = args.audio
voice_gender    = args.gender
voice_name      = dic_voice[voice_gender]
command_edgetts = args.edgetts

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

async def make_mp3 (text, voice, file_output):
    communicate = edge_tts.Communicate (text, voice)
    await communicate.save (file_output)
    
# making MP3 file
make_mp3 (text_article, voice_name, file_audio)
