from flask import Flask, render_template, url_for, redirect, request, current_app
from markdown2 import markdown
from jinja2 import Environment, PackageLoader
import os
import pypandoc
from datetime import datetime
import subprocess
import requests
from flask_flatpages import FlatPages
import sys
from flask_frozen import Freezer
from itertools import tee, islice, chain
from flask_pager import Pager

DEBUG = True

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['PAGE_SIZE'] = 10
app.config['VISIBLE_PAGE_COUNT'] = 8

pages = FlatPages(app)
freezer = Freezer(app)
app.config['PAGE_SIZE'] = 10

posts = {}
for markdown_post in os.listdir('pages'):
  if markdown_post.endswith('md'):
   file_path = os.path.join('pages', markdown_post)
   with open(file_path, 'r') as file:
     posts[markdown_post] = markdown(file.read(), extras=['metadata'])
     #convertin = subprocess.call('./bash.sh')

env = Environment(loader=PackageLoader('app', 'templates'))
test_template = env.get_template('index.html')
posts_metadata = [posts[post].metadata for post in posts]

datas = []
date = []
url = []
lat = []
date_list = []
history = []

for data in posts_metadata:
 url.append(data['url'])
 if data['category'] == 'history':
  history.append(data)

 url.sort()
 my_date = datetime.strptime(data['list1'],"%Y.%m.%d")
 time = my_date.date()
 date.append(time)
 x = sorted(date)
 li = list(zip(x,url))
 latest_article = sorted(li, key=lambda tuple:tuple[0])
 latest = latest_article[-4:]
 d = data['list1']
 date_list.append(d)
 date_list.sort()
 new = list(zip(date_list,url))
 #count = range(len(url))
 #nxt_prev = list(zip(count,url))
def previous_and_next(some_iterable):
 prevs, items, nexts = tee(some_iterable, 3)
 prevs = chain([None], prevs)
 nexts = chain(islice(nexts, 1, None), [None])
 return zip(prevs,items, nexts)

for prev, items,next in previous_and_next(new):
 print('')


for url_post in latest:
  url_posts = url_post[1]
  lat.append(url_posts)
for j in lat:
 for y in posts_metadata:
  if y['url'] == j:
   datas.append(y)



@app.route('/')
def test():
 csslink = url_for('static', filename='css/main2.css')
 return render_template('index.html',history=history, posts=datas, articles=datas, csslink=csslink, featured=datas[-1])


@app.route('/<path:path>.html')
def page(path):
    page = pages.get_or_404(path)
    csslink = url_for('static', filename='css/main2.css')
    return render_template('page.html', page=page, csslink=csslink, new=new, prev=prev,items=items,next=next)


@freezer.register_generator
def pagelist():
    for page in pages:
        yield url_for('page', path=page.path)

@app.route('/archive')
def archive():
    csslink = url_for('static', filename='css/main2.css')
    page = int(request.args.get('page', 1))
    count = 400
    pager = Pager(page, count)
    pages = pager.get_pages()
    skip = (page - 1) * current_app.config['PAGE_SIZE']
    limit = current_app.config['PAGE_SIZE']
    data_to_show = posts_metadata[skip: skip + limit]
    return render_template('archive.html',csslink=csslink,posts=posts_metadata , pages=pages, data_to_show=data_to_show)

@app.route('/history_archive')
def history_archive():
 csslink = url_for('static', filename='css/main2.css')
 page = int(request.args.get('page', 1))
 count = 400
 pager = Pager(page, count)
 pages = pager.get_pages()
 skip = (page - 1) * current_app.config['PAGE_SIZE']
 limit = current_app.config['PAGE_SIZE']
 data_to_show = posts_metadata[skip: skip + limit]
 return render_template('history_archive.html',csslink=csslink,posts=posts_metadata,pages=pages,data_to_show=data_to_show)

@app.route('/insight_archive')
def insight_archive():
 csslink = url_for('static', filename='css/main2.css')
 page = int(request.args.get('page', 1))
 count = 400
 pager = Pager(page, count)
 pages = pager.get_pages()
 skip = (page - 1) * current_app.config['PAGE_SIZE']
 limit = current_app.config['PAGE_SIZE']
 data_to_show = posts_metadata[skip: skip + limit]

 return render_template('insight_archive.html',csslink=csslink,posts=posts_metadata,data_to_show=data_to_show,pages=pages)

@app.route('/technology_archive')
def technology_archive():
 csslink = url_for('static', filename='css/main2.css')
 page = int(request.args.get('page', 1))
 count = 400
 pager = Pager(page, count)
 pages = pager.get_pages()
 skip = (page - 1) * current_app.config['PAGE_SIZE']
 limit = current_app.config['PAGE_SIZE']
 data_to_show = posts_metadata[skip: skip + limit]

 return render_template('technology_archive.html',csslink=csslink,posts=posts_metadata,data_to_show=data_to_show,pages=pages)

@app.route('/market_archive')
def market_archive():
 csslink = url_for('static', filename='css/main2.css')
 page = int(request.args.get('page', 1))
 count = 400
 pager = Pager(page, count)
 pages = pager.get_pages()
 skip = (page - 1) * current_app.config['PAGE_SIZE']
 limit = current_app.config['PAGE_SIZE']
 data_to_show = posts_metadata[skip: skip + limit]

 return render_template('market_archive.html',csslink=csslink,posts=posts_metadata,data_to_show=data_to_show,pages=pages)

@app.route('/xenopoetisc_archive')
def xenopoetisc_archive():
 csslink = url_for('static', filename='css/main2.css')
 page = int(request.args.get('page', 1))
 count = 400
 pager = Pager(page, count)
 pages = pager.get_pages()
 skip = (page - 1) * current_app.config['PAGE_SIZE']
 limit = current_app.config['PAGE_SIZE']
 data_to_show = posts_metadata[skip: skip + limit]

 return render_template('xenopoetisc_archive.html',csslink=csslink,posts=posts_metadata,data_to_show=data_to_show,pages=pages)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=5001)
