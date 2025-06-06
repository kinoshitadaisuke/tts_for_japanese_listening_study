#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/06/06 13:16:50 (UT+08:00) daisuke>
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
descr  = f'Downloading NHK news article and generating MP3 file'
parser = argparse.ArgumentParser (description=descr)

# adding arguments
list_gender = ['female', 'male']
dic_voice = {
    'female': 'ja-JP-NanamiNeural',
    'male':   'ja-JP-KeitaNeural',
}
parser.add_argument ('-u', '--url', default='', \
                     help='URL of NHK news article')
parser.add_argument ('-t', '--text', default='nhk.txt', \
                     help='output text file')
parser.add_argument ('-a', '--audio', default='nhk.mp3', \
                     help='output audio file')
parser.add_argument ('-g', '--gender', choices=list_gender, default='female', \
                     help='gender of synthesised speech (female or male)')
parser.add_argument ('-e', '--edgetts', default='edge-tts', \
                     help='edge-tts command')

# parsing arguments
args = parser.parse_args ()

# input parameters
url_nhk         = args.url
file_text       = args.text
file_audio      = args.audio
voice_gender    = args.gender
voice_name      = dic_voice[voice_gender]
command_edgetts = args.edgetts

# checking URL
if not ('https://www3.nhk.or.jp/' in url_nhk):
    # printing a message
    print ("ERROR:")
    print ("ERROR: specified URL is not for NHK news article.")
    print ("ERROR:")
    # exit
    sys.exit (0)

# fetching HTML file
with urllib.request.urlopen (url_nhk) as fh_in:
    html_nhk = fh_in.read ().decode ('utf-8')

# creating BeautifulSoup object
soup = bs4.BeautifulSoup (html_nhk, 'html.parser')

# extracting article title and body
html_article_title = soup.find ('h1', class_='content--title')
html_article_body  = soup.find ('div', class_='content--detail-body')

# converting HTML into plain text
text_article_title = html_article_title.get_text ()
text_article_body  = html_article_body.get_text ()
text_article_title = text_article_title.replace (' ', '\n')

# writing extracted plain text into a file
with open (file_text, 'w') as fh_out:
    fh_out.write (text_article_title)
    fh_out.write (f'\n\n')
    fh_out.write (text_article_body)

# executing edge-tts command to make MP3 file
command_create_mp3 = f'{command_edgetts} -f {file_text} --write-media {file_audio} --voice {voice_name}'
subprocess.run (command_create_mp3, shell=True)
