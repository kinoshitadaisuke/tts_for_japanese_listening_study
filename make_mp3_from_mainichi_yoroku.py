#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/06/06 12:47:36 (UT+08:00) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing urllib module
import urllib.request

# importing beautiful soup module
import bs4

# importing subprocess module
import subprocess

# initialising a parser
descr  = f'Downloading Mainichi Yoroku and generating MP3 file'
parser = argparse.ArgumentParser (description=descr)

# adding arguments
list_gender = ['female', 'male']
dic_voice = {
    'female': 'ja-JP-NanamiNeural',
    'male':   'ja-JP-KeitaNeural',
}
parser.add_argument ('-u', '--url', default='', \
                     help='URL of Mainichi Yoroku article')
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
if not ('https://mainichi.jp/articles/' in url_mainichi):
    # printing a message
    print ("ERROR:")
    print ("ERROR: specified URL is not for Mainichi Yoroku article.")
    print ("ERROR:")
    # exit
    sys.exit (0)

# fetching HTML file
with urllib.request.urlopen (url_mainichi) as fh_in:
    html_mainichi = fh_in.read ().decode ('utf-8')

# creating BeautifulSoup object
soup = bs4.BeautifulSoup (html_mainichi, 'html.parser')

# extracting article title and body
html_article_title = soup.find ('h1', class_='title-page')
html_article_body  = soup.find ('section', class_='articledetail-body').find ('p')

# converting HTML into plain text
text_article_title = html_article_title.get_text ()
text_article_body  = html_article_body.get_text ()
text_article_body  = text_article_body.replace ('▲', '。\n\n')

# writing extracted plain text into a file
with open (file_text, 'w') as fh_out:
    fh_out.write (text_article_title)
    fh_out.write (f'\n\n')
    fh_out.write (text_article_body)

# executing edge-tts command to make MP3 file
command_create_mp3 = f'{command_edgetts} -f {file_text} --write-media {file_audio} --voice {voice_name}'
subprocess.run (command_create_mp3, shell=True)
