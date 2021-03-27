'''
    Cumination
    Copyright (C) 2015 Whitecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import os
import sqlite3
import base64

from six.moves import urllib_parse
import six
import json
import random
import datetime
import time
import requests


from resources.lib import utils
from resources.lib import wbcsmodels

from resources.lib.sites import cambro

from resources.lib.adultsite import AdultSite
from datetime import datetime, timedelta

import resolveurl

from kodi_six import xbmc, xbmcgui

from bs4 import BeautifulSoup

today = datetime.today()
yesterday = today - timedelta(days=1) - timedelta(hours=6)

bu = 'https://chaturbate.com/'
site = AdultSite(
    'camrips', '[COLOR hotpink]Camrips[/COLOR]', bu, 'camrips.png', 'camrips', True)

addon = utils.addon

HTTP_HEADERS_IPAD = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4'}


@site.register(default_mode=True)
def Main():
    female = True if addon.getSetting("chatfemale") == "true" else False
    male = True if addon.getSetting("chatmale") == "true" else False
    couple = True if addon.getSetting("chatcouple") == "true" else False
    trans = True if addon.getSetting("chattrans") == "true" else False

    site.add_dir('[COLOR orangered] CBexplorer top - Couples[/COLOR]',
                 '/most-popular-couples.json', 'list_top', site.img_next, yesterday.strftime('%Y-%m-%d'))
    site.add_dir('[COLOR orangered] CBexplorer top - Women[/COLOR]',
                 '/most-popular-women.json', 'list_top', site.img_next, yesterday.strftime('%Y-%m-%d'))
    site.add_dir('[COLOR orangered] CBexplorer top - Squirt[/COLOR]',
                 '/tag-squirt-most-popular.json', 'list_top', site.img_next,  yesterday.strftime('%Y-%m-%d'))

    site.add_dir('[COLOR yellow] CBexplorer - Growing Follower count  [/COLOR]',
                 '/user_followers.json', 'list_top', site.img_next,  yesterday.strftime('%Y-%m-%d'))
    site.add_dir('[COLOR yellow] CBexplorer - Growing Followers growth  [/COLOR]',
                 '/user_follower_gain.json', 'list_top', site.img_next,  yesterday.strftime('%Y-%m-%d'))

    site.add_dir('[COLOR lime] CBexplorer - Growing Followers couple  [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,offline')
    site.add_dir('[COLOR lime] CBexplorer - Growing Followers female  [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,offline')

    site.add_dir('[COLOR deeppink] CBexplorer - Growing Followers couple online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,online')
    site.add_dir('[COLOR deeppink] CBexplorer - Growing Followers female online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,online')

    site.add_dir('[COLOR lime] CBexplorer - viewers couple  [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,viewers')
    site.add_dir('[COLOR lime] CBexplorer - viewers female  [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,viewers')

    site.add_dir('[COLOR deeppink] CBexplorer - viewers couple online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,viewers_online')
    site.add_dir('[COLOR deeppink] CBexplorer - viewers female online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,viewers_online')

    site.add_dir('[COLOR lime] CBexplorer - followers couple - max [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,followers_max')
    site.add_dir('[COLOR lime] CBexplorer - followers female  - max [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,followers_max')

    site.add_dir('[COLOR deeppink] CBexplorer - followers couple - max  online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,followers_max_online')
    site.add_dir('[COLOR deeppink] CBexplorer - followers female - max  online [/COLOR]',
                 '/user_follower_gain.json', 'list_followers_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,followers_max_online')

    site.add_dir('[COLOR lime] CBexplorer - followers couple - squirt online [/COLOR]',
                 '/user_follower_gain.json', 'list_squirt_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='c,squirt_online')
    site.add_dir('[COLOR lime] CBexplorer - followers female  - squirt online [/COLOR]',
                 '/user_follower_gain.json', 'list_squirt_stat', site.img_next,  today.strftime('%d.%m.%y'), keyword='f,squirt_online')

    site.add_dir('[COLOR mediumslateblue] CBexplorer - Month squirt [/COLOR]',
                 '/30days/women_tag-squirt-most-popular.json', 'list_top', site.img_next,  yesterday.strftime('%Y-%m-%d'), keyword='month-squirt')

    site.add_dir('[COLOR orange]Squirt[/COLOR]',
                 'https://camspider.com/api/search?search=squirt&viewersMin=50&f=no&m=no&c=no&t=no&hdOnly=no&newOnly=no&exact=no&language=', 'List_CamSpider', '', '')

    site.add_dir('[COLOR hotpink]Female[/COLOR]', bu +
                 'female-cams/?page=1', 'List', '', '')
    site.add_dir('[COLOR hotpink]Couple[/COLOR]', bu +
                 'couple-cams/?page=1', 'List', '', '')
    site.add_dir('[COLOR hotpink]New Cams - Female[/COLOR]',
                 bu + 'new-cams/female/?page=1', 'List', '', '')
    site.add_dir('[COLOR hotpink]New Cams - Couple[/COLOR]',
                 bu + 'new-cams/couple/?page=1', 'List', '', '')
    site.add_dir('[COLOR hotpink]Squirt[/COLOR]',
                 'https://camspider.com/api/search?search=squirt&viewersMin=50&f=no&m=no&c=no&t=no&hdOnly=no&newOnly=no&exact=no&language=', 'List_CamSpider', '', '')

    # site.add_dir('[COLOR red]Refresh Camrips images[/COLOR]',
    #              '', 'clean_database', '', Folder=False)
    # site.add_dir('[COLOR hotpink]Look for Model[/COLOR]',
    #              bu, 'Search', site.img_search)
    # site.add_dir('[COLOR hotpink]Featured[/COLOR]',
    #              bu + '?page=1', 'List', '', '')
    site.add_dir('[COLOR yellow]Current Hour\'s Top Cams[/COLOR]',
                 bu + 'api/ts/contest/leaderboard/', 'topCams', '', '')

    site.add_dir('[COLOR turquoise] CBexplorer sorted top - Couples[/COLOR]',
                 '/most-popular-couples.json', 'list_sorted', site.img_next, yesterday.strftime('%Y-%m-%d'), keyword='c')
    site.add_dir('[COLOR turquoise] CBexplorer sorted top - Women[/COLOR]',
                 '/most-popular-women.json', 'list_sorted', site.img_next, yesterday.strftime('%Y-%m-%d'), keyword='f')
    site.add_dir('[COLOR turquoise] CBexplorer sorted top - Squirt[/COLOR]',
                 '/tag-squirt-most-popular.json', 'list_sorted', site.img_next,  yesterday.strftime('%Y-%m-%d'), keyword='f')

    site.add_dir('[COLOR mediumslateblue] CBexplorer top - Couples[/COLOR]',
                 '/most-popular-couples.json', 'list_top', site.img_next, yesterday.strftime('%Y-%m-%d'), keyword='cambro')
    site.add_dir('[COLOR mediumslateblue] CBexplorer top - Women[/COLOR]',
                 '/most-popular-women.json', 'list_top', site.img_next, yesterday.strftime('%Y-%m-%d'), keyword='cambro')

    site.add_dir('[COLOR yellow]Update Database[/COLOR]', 'https://cbexplorer.com/stats/',
                 'update_database', '', yesterday.strftime('%Y-%m-%d'))
    utils.eod()


@site.register()
def List(url, page=1, keyword=''):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    listhtml = utils._getHtml(url)
    match = re.compile(
        r'room_list_room".+?href="([^"]+).+?src="([^"]+).+?<div[^>]+>([^<]+)</div>.+?href[^>]+>([^<]+)<.+?age[^>]+>([^<]+).+?title="([^"]+).+?location.+?>([^<]+).+?cams">([^<]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, status, name, age, subject, location, duration in match:
        name = utils.cleantext(name.strip())
        age = utils.cleantext(age.strip())
        subject = utils.cleantext(subject.strip()) + "[CR][COLOR deeppink]Location: [/COLOR]" + utils.cleantext(
            location.strip()) + "[CR]" + utils.cleantext(duration.strip())
        status = utils.cleantext(status.replace("[CR]", "").strip())
        name = name + " [COLOR deeppink][" + age + "][/COLOR] " + status

        utils.kodilog(videopage)
        site.add_dir(name, videopage,
                     'list_webcamshows_model', img, desc=subject, play=True)
    nextp = re.compile(
        r'<a\s*href="([^"]+)"\s*class="next', re.DOTALL | re.IGNORECASE).search(listhtml)
    if nextp:
        page = page + 1 if page else 2
        next = bu[:-1] + nextp.group(1)
        site.add_dir('Next Page (' + str(page) + ')',
                     next, 'List', site.img_next, page)

    utils.eod()


@site.register()
def update_database(url, page=1, keyword=''):

    wbcmodels_in_db = wbcsmodels.fetch_all_models_in_db_name_and_date()
    if wbcmodels_in_db:
        names = [model[0] for model in wbcmodels_in_db]
        name_date_dict = dict(wbcmodels_in_db)
    else:
        names = []
        name_date_dict = {}

    url_c = '/most-popular-couples.json'
    url_w = '/most-popular-women.json'
    url_sq = '/tag-squirt-most-popular.json'

    list_c = utils._getHtml3(url+page+url_c)[0:250]
    list_w = utils._getHtml3(url+page+url_w)[0:250]
    list_sq = utils._getHtml3(url+page+url_sq)
    list_all = list_c + list_w + list_sq
    listhtml = []

    for i in range(0, len(list_all)):
        if list_all[i] not in list_all[i+1:]:
            listhtml.append(list_all[i])

    total_added = 0
    total_visited = 0

    for model in listhtml:
        name = model["u"]
        max_u = model["max_u"]
        num_f = model["num_f"]
        gender = model["g"]

        model_logout = str(model["lo"]).replace(
            'T', ' ').replace('Z', '')[:-1][:19]

# Test if can skip ...
        if name in names:
            model_last_entry_date = name_date_dict[name][:19]
            try:
                model_last_entry_date_obj = datetime.strptime(
                    model_last_entry_date, "%Y-%m-%d %H:%M:%S")
            except TypeError:
                model_last_entry_date_obj = datetime(
                    *(time.strptime(model_last_entry_date, "%Y-%m-%d %H:%M:%S")[0:6]))
            try:
                model_logout_obj = datetime.strptime(
                    model_logout, "%Y-%m-%d %H:%M:%S")
            except TypeError:
                model_logout_obj = datetime(
                    *(time.strptime(model_logout, "%Y-%m-%d %H:%M:%S")[0:6]))

            if model_last_entry_date_obj > model_logout_obj:
                utils.kodilog('skipped')
                continue

 ##### GET FROM webcamshows #########
        try:
            total_visited += 1
            link_model = 'https://www.webcamshows.org/models/{}/'.format(
                name)
            response = requests.get(link_model, allow_redirects=False)
            soup = BeautifulSoup(response.content, "html.parser")
            article = soup.find(
                "article", {"class": "card pure-u-1 pure-u-md-1-2 pure-u-lg-1-3"})

            img = article.find("img")['src']
            url_text = article.find_all("a")[2].find(
                'h3').text

            if 'Camsoda' in url_text:
                url = url_text.replace('Camsoda Webcamshow', '').split()[1]
            elif 'Cam4' in url_text:
                url = url_text.replace('Cam4 Webcamshow', '').split()[1]
            else:
                url = url_text.replace(
                    'Chaturbate Webcamshow', '').split()[1]
            found = True
        except:
            found = False

# If found, add to database
        if found:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            if name in names:
                wbcsmodels.update_wbcsmodel(
                    'wbcsmodels.wbcsmodels', name, url, img, max_u, num_f, date, gender)
            else:
                wbcsmodels.addwbc(
                    'wbcsmodels.wbcsmodels', name, url, img, max_u, num_f, date, gender)
            total_added += 1
        if not found:
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            url = '01/01/2021'
            img = 'https://pussygenerator.com/bio/chaturbate_profile_images/{}/{}-1.jpg'.format(
                name, name)
            max_u = 1
            num_f = 1
            gender = 'f'
            if name in names:
                wbcsmodels.update_wbcsmodel('wbcsmodels.wbcsmodels',
                                            name, url, img, max_u, num_f, date, gender)
            else:
                wbcsmodels.addwbc(
                    'wbcsmodels.wbcsmodels', name, url, img, max_u, num_f, date, gender)
    try:
        today_new = datetime.strptime(page, '%Y-%m-%d')
    except TypeError:
        today_new = datetime(*(time.strptime(page, '%Y-%m-%d')[0:6]))

    yesterday_new = today_new - timedelta(days=1)

    site.add_dir(yesterday_new.strftime('%Y-%m-%d'), 'https://cbexplorer.com/stats/',
                 'update_database', '', yesterday_new.strftime('%Y-%m-%d'))
    utils.eod()
    utils.dialog.ok("Adding files library",
                    "Total visited: {}   Total added: {}".format(total_visited, total_added))


@ site.register()
def List_CamSpider(url, page=1, keyword=''):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    listhtml = utils._getHtml(url)

    listhtml = json.loads(listhtml)

    models = [model for model in listhtml if (
        model['gender'] == 'f') or (model['gender'] == 'c')]

    if len(models) > 201:
        models = models[0:200]

    for model in models:
        username = model["username"]

        num_users = model["num_users"]
        num_followers = '?'
        gender = model["gender"]
        if model["age"] != 'null':
            age = model["age"]
        else:
            age = 99
        tags = '?'

        if model['is_hd'] == True:
            video_res = 'HD'
        else:
            video_res = 'SD'

        img = '{}?{}'.format(model["image_url"],
                             random.randint(1000000000, 9000000000))

        seconds_online = model["seconds_online"]

        username = model["username"]
        name = '{} [COLOR deeppink] [{}] [/COLOR]  [{}]'.format(
            username, age, video_res)

        room_topic = model["room_subject"].encode('utf-8')

        subject = '\n\n[B]Activity: [/B] {}, {} viewers  \n[B]Followers: [/B] {}  \n[B]Age: [/B] {} \n[B]Gender: [/B] {} \n\n[B]Tags: [/B] {} \n\n[B]Room topic: [/B]  {}'.format(
            seconds_online, num_users, num_followers, age, gender, tags, room_topic)
        videopage = '/{}/'.format(username)

        site.add_dir(name, videopage,
                     'list_webcamshows_model', img, play=True, desc=subject)

    utils.eod()


@ site.register()
def list_top(url, page=1, keyword=''):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    base_url = 'https://cbexplorer.com/stats/'
    full_url = base_url + page + url
    listhtml = utils._getHtml3(full_url)
    wbcmodels_in_db_url = wbcsmodels.fetch_all_models_in_db_name_and_url()
    wbcmodels_in_db_img = wbcsmodels.fetch_all_models_in_db_name_and_img()

    if wbcmodels_in_db_url:
        names = [model[0] for model in wbcmodels_in_db_url]
        name_date_dict = dict(wbcmodels_in_db_url)
        name_img_dict = dict(wbcmodels_in_db_img)
    else:
        names = []
        name_date_dict = {}

    for model in listhtml[0:400]:
        name = model['u']

        if 'a' in model:
            age = model['a']
        else:
            age = '?'

        if 'follower' in url:
            followers = model['f']
            follower_gain = model['fg']

            subject = "\n[B]Age:[/B] {}\n[B]Followers: [/B] {}\n\n[B]Follower Gain:[/B] {}".format(
                age, followers, follower_gain)
        elif keyword == 'month-squirt':
            followers = model['score']
            if 'pr' in model:
                follower_gain = model['pr']
            else:
                follower_gain = 'new'
            subject = "\n[B]Age:[/B] {}\n[B]Score: [/B] {}\n\n[B]Prev Position:[/B] {}".format(
                age, followers, follower_gain)
        else:
            num_followers = model['num_f']
            max_users = model['max_u']
            subject = model['t']
            subject = "\n[B]Age:[/B] {}\n[B]Followers: [/B] {} \n[B]Max Users: [/B] {}\n\n[B]Room topic:[/B] {}".format(
                age, num_followers, max_users, subject)

        if name not in names:
            img = 'https://pussygenerator.com/bio/chaturbate_profile_images/{}/{}-1.jpg'.format(
                model['u'], model['u'])
            date = 'not in db'
            name = "{} [{}]".format(name, date)
        else:
            img = name_img_dict[name]
            date = name_date_dict[name][:19]

            try:
                real_date = datetime.strptime(
                    date, "%d/%m/%Y")
            except TypeError:
                real_date = datetime(
                    *(time.strptime(date, "%d/%m/%Y")[0:6]))

            delta = today - real_date

            if delta.days > 2:
                name = "{} [{}]".format(name, date)
            else:
                name = "{} [COLOR yellow][{}][/COLOR] ".format(
                    name, real_date.strftime('%d-%m-%Y'))

        if keyword == 'cambro':
            site.add_dir(name, model['u'],
                         'list_webcamshows_model', img, desc=subject, keyword='cambro')
        else:
            site.add_dir(name, model['u'],
                         'list_webcamshows_model', img, desc=subject)

    try:
        today_new = datetime.strptime(page, '%Y-%m-%d')
    except TypeError:
        today_new = datetime(*(time.strptime(page, '%Y-%m-%d')[0:6]))

    yesterday_new = today_new - timedelta(days=1)

    site.add_dir(yesterday_new.strftime('%Y-%m-%d'), url,
                 'list_top', '', yesterday_new.strftime('%Y-%m-%d'))
    utils.eod()


@ site.register()
def list_followers_stat(url, page=1, keyword=','):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    models = get_models_followers(page, keyword.split(',')[
                                  0], keyword.split(',')[1])

    wbcmodels_in_db_url = wbcsmodels.fetch_all_models_in_db_name_and_url()
    wbcmodels_in_db_img = wbcsmodels.fetch_all_models_in_db_name_and_img()

    if wbcmodels_in_db_url:
        names = [model[0] for model in wbcmodels_in_db_url]
        name_date_dict = dict(wbcmodels_in_db_url)
        name_img_dict = dict(wbcmodels_in_db_img)
    else:
        names = []
        name_date_dict = {}

    for model in models:
        name = model[0]
        username = name
        followers = model[1]

        subject = "[B]Followers: [/B] {}".format(
            followers)

        if name not in names:
            img = 'https://pussygenerator.com/bio/chaturbate_profile_images/{}/{}-1.jpg'.format(
                username, username)
            date = 'not in db'
            name = "{} [{}]".format(name, date)
        else:
            img = name_img_dict[name]
            date = name_date_dict[name][:19]

            try:
                real_date = datetime.strptime(
                    date, "%d/%m/%Y")
            except TypeError:
                real_date = datetime(
                    *(time.strptime(date, "%d/%m/%Y")[0:6]))

            delta = today - real_date

            if delta.days > 2:
                name = "{} [{}]".format(name, date)
            else:
                name = "{} [COLOR yellow][{}][/COLOR] ".format(
                    name, real_date.strftime('%d-%m-%Y'))

        site.add_dir(name, '/' + username + '/',
                     'list_webcamshows_model', img, desc=subject, play=True)

    try:
        today_new = datetime.strptime(page, '%d.%m.%y')
    except TypeError:
        today_new = datetime(*(time.strptime(page, '%d.%m.%y')[0:6]))

    yesterday_new = today_new - timedelta(days=1)

    site.add_dir(yesterday_new.strftime('%d.%m.%y'), url,
                 'list_followers_stat', '', yesterday_new.strftime('%d.%m.%y'), keyword=keyword)
    utils.eod()


@ site.register()
def list_squirt_stat(url, page=1, keyword=','):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    models = get_models_followers(page, keyword.split(',')[
                                  0], keyword.split(',')[1], pages=10)

    wbcmodels_in_db_url = wbcsmodels.fetch_all_models_in_db_name_and_url()
    wbcmodels_in_db_img = wbcsmodels.fetch_all_models_in_db_name_and_img()

    if wbcmodels_in_db_url:
        names = [model[0] for model in wbcmodels_in_db_url]
        name_date_dict = dict(wbcmodels_in_db_url)
        name_img_dict = dict(wbcmodels_in_db_img)
    else:
        names = []
        name_date_dict = {}

    listhtml = utils._getHtml(
        'https://camspider.com/api/search?search=squirt&viewersMin=50&f=no&m=no&c=no&t=no&hdOnly=no&newOnly=no&exact=no&language=')
    listhtml = json.loads(listhtml)
    squirt_names = [model["username"] for model in listhtml if (
        model['gender'] == 'f') or (model['gender'] == 'c')]

    for model in models:
        name = model[0]

        if name not in squirt_names:
            continue

        username = name
        followers = model[1]

        subject = "[B]Followers: [/B] {}".format(
            followers)

        if name not in names:
            img = 'https://pussygenerator.com/bio/chaturbate_profile_images/{}/{}-1.jpg'.format(
                username, username)
            date = 'not in db'
            name = "{} [{}]".format(name, date)
        else:
            img = name_img_dict[name]
            date = name_date_dict[name][:19]

            try:
                real_date = datetime.strptime(
                    date, "%d/%m/%Y")
            except TypeError:
                real_date = datetime(
                    *(time.strptime(date, "%d/%m/%Y")[0:6]))

            delta = today - real_date

            if delta.days > 2:
                name = "{} [{}]".format(name, date)
            else:
                name = "{} [COLOR yellow][{}][/COLOR] ".format(
                    name, real_date.strftime('%d-%m-%Y'))

        site.add_dir(name, '/' + username + '/',
                     'list_webcamshows_model', img, desc=subject, play=True)

    try:
        today_new = datetime.strptime(page, '%d.%m.%y')
    except TypeError:
        today_new = datetime(*(time.strptime(page, '%d.%m.%y')[0:6]))

    yesterday_new = today_new - timedelta(days=1)

    site.add_dir(yesterday_new.strftime('%d.%m.%y'), url,
                 'list_followers_stat', '', yesterday_new.strftime('%d.%m.%y'), keyword=keyword)
    utils.eod()


@ site.register()
def list_sorted(url, page=1, keyword=''):
    if addon.getSetting("chaturbate") == "true":
        clean_database(False)

    wbcmodels_in_db = wbcsmodels.select_models_by_gender(keyword)
    utils.kodilog(wbcmodels_in_db)

    # if len(wbcmodels_in_db) > 400:
    #     wbcmodels_in_db = wbcmodels_in_db[0:400]

    for model in wbcmodels_in_db:
        name = model[0]
        date = model[1]
        img = model[3]
        max_u = model[4]
        num_f = model[5]

        gender = model[7]

        username = name

        subject = "\n[B]Followers: [/B] {} \n[B]Max Users: [/B] {}\n\n[B]Last update:[/B] {} \n\n[B]Gender:[/B] {}".format(
            num_f, max_u, date, gender)

        try:
            real_date = datetime.strptime(
                date, "%d/%m/%Y")
        except TypeError:
            real_date = datetime(
                *(time.strptime(date, "%d/%m/%Y")[0:6]))

        delta = today - real_date

        if delta.days > 3:
            name = "{} [{}]".format(name, date)
        else:
            name = "{} [COLOR yellow][{}][/COLOR] ".format(
                name, real_date.strftime('%d-%m-%Y'))

        site.add_dir(name, username,
                     'list_webcamshows_model', img, desc=subject)

    utils.eod()


@ site.register()
def list_webcamshows_model(url, page=1, keyword=''):

    if keyword == 'cambro':
        cambro.Search(
            'https://www.cambro.tv/search/', keyword=url+'/')

    else:
        if addon.getSetting("chaturbate") == "true":
            clean_database(False)

        if 'page' in url:
            url = 'https://www.webcamshows.org{}'.format(url)
            username = url.split('/')[2]
        else:
            url = 'https://www.webcamshows.org/models/{}/'.format(url)
            username = url.split('/')[1]

        listhtml = utils._getHtml(url)

        soup = BeautifulSoup(listhtml, "html.parser")
        articles = soup.findAll(
            "article", {"class": "card pure-u-1 pure-u-md-1-2 pure-u-lg-1-3"})

        for article in articles:
            img = article.find("img")['src']
            videopage = article.find("a")['href']

            post_title = article.find_all("a")[2].find(
                'h3').text.replace('Chaturbate Webcamshow', '')

            post_title_text = article.find_all("a")[2].find(
                'h3').text

            if 'Camsoda' in post_title_text:
                post_title = post_title_text.replace('Camsoda Webcamshow', '')
            elif 'Cam4' in post_title_text:
                post_title = post_title_text.replace('Cam4 Webcamshow', '')
            else:
                post_title = post_title_text.replace(
                    'Chaturbate Webcamshow', '')

            duration = article.find_all("p", {"class": "post_duration"})[
                1].text.replace('access_time', '')

            name = "{} [COLOR yellow] {}[/COLOR]".format(post_title, duration)
            subject = name.replace("&amp;", "&").replace("&lt;", "<").replace(
                "&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')

            site.add_download_link(name, videopage, 'Playvid_wbc',
                                   img, subject, noDownload=True)
        try:
            current_page_text = soup.find(
                "span", {"class": "pagination__current"}).text.replace('Page', '')
            next_page_url = soup.find(
                "a", {"class": "pagination__link pagination__link--next"})['href']
            site.add_dir(current_page_text + '  [COLOR lime]   Next [/COLOR]', next_page_url,
                         'list_webcamshows_model', img, desc=subject, play=True)
        except:
            pass

    utils.eod()


@ site.register(clean_mode=True)
def clean_database(showdialog=True):
    conn = sqlite3.connect(utils.TRANSLATEPATH(
        "special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute(
                "SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".highwebmedia.com")
            for row in list:
                conn.execute(
                    "DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try:
                    os.remove(utils.TRANSLATEPATH(
                        "special://thumbnails/" + row[1]))
                except:
                    pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" %
                         ".highwebmedia.com")
            if showdialog:
                utils.notify('Finished', 'Chaturbate images cleared')
    except:
        pass


@ site.register()
def Playvid(url, name):
    playmode = int(addon.getSetting('chatplay'))
    listhtml = utils._getHtml(url, headers=HTTP_HEADERS_IPAD)
    goal = get_goal(name)

    r = re.search(r'initialRoomDossier\s*=\s*"([^"]+)', listhtml)
    if r:
        data = six.b(r.group(1)).decode('unicode-escape')
        data = data if six.PY3 else data.encode('utf8')
        data = json.loads(data)
    else:
        data = False

    if data:
        m3u8stream = data['hls_source']
    else:
        m3u8stream = False

    if playmode == 0:
        if m3u8stream:
            videourl = "{0}|{1}".format(
                m3u8stream, urllib_parse.urlencode(HTTP_HEADERS_IPAD))
        else:
            utils.notify('Oh oh', 'Couldn\'t find a playable webcam link')
            return

    elif playmode == 1:
        if data:
            streamserver = "rtmp://{}/live-edge".format(data['flash_host'])
            modelname = data['broadcaster_username']
            username_full = data['viewer_username']
            username = 'anonymous'
            room_pass = data['room_pass']
            swfurl = 'https://ssl-ccstatic.highwebmedia.com/theatermodeassets/CBV_TS_v1.0.swf'
            edge_auth = data['edge_auth']
            videourl = "%s app=live-edge swfUrl=%s pageUrl=%s conn=S:%s conn=S:%s conn=S:3.22 conn=S:%s conn=S:%s conn=S:%s playpath=mp4" % (
                streamserver, swfurl, url, username_full, modelname, username, room_pass, edge_auth)
        else:
            utils.notify('Oh oh', 'Couldn\'t find a playable webcam link')
            return

    # name_and_goal = name + goal
    vp = utils.VideoPlayer(name, goal=goal)
    vp.play_from_direct_link(videourl)


@site.register()
def Playvid_wbc(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    # vp.progress.update(25, "[CR]Loading video page[CR]")
    videopage = utils.getHtml(url, '')
    if '<iframe' in videopage:
        videolink = re.compile(
            r'''<iframe.+?src=["']?([^'"\s]+)''', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
        videolink = base64.b64decode(
            urllib_parse.unquote(videolink.split('embed/?')[-1]))
        videolink = videolink.decode('utf-8') if utils.PY3 else videolink
        vp.play_from_link_to_resolve(videolink)
    else:
        utils.notify('Oh oh', 'Couldn\'t find a playable link')
        return None


@ site.register()
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        site.search_dir(url, 'Search')
    else:
        title = urllib_parse.quote_plus(keyword)
        searchUrl = searchUrl + title + '/'
        Playvid(searchUrl, title)


@ site.register()
def topCams(url):
    response = utils._getHtml(url)
    jsonTop = json.loads(response)['top']
    for iTop in jsonTop:
        subject = 'Name: ' + iTop['room_user'] + '\n'
        subject = subject + 'Points: ' + str(iTop['points']) + '\n'
        subject = subject + 'Watching: ' + str(iTop['viewers'])
        site.add_download_link(iTop['room_user'], bu + iTop['room_user'] + '/', 'Playvid',
                               iTop['image_url'], subject, noDownload=True)
    utils.eod()


@ site.register()
def get_goal(name):
    url = "https://chaturbate.com/api/panel_context/{}".format(name.split(' ')[
        0])
    response = utils._getHtml3(url)
    try:
        result = response
    except:
        return 'not online'
    try:
        goalstring = ""
        if (len(result['layers']) > 0):
            for item in result['layers']:
                if 'text' in item:
                    goalstring = goalstring + " " + item['text'] + " "
        else:
            values = ['row_1', 'row_2', 'row_3']
            panelarr = [result['table'][item]['col_1']['value']
                        for item in values if item in result]
            for item in panelarr:
                if item:
                    goalstring = goalstring + " " + item + " "

        if (goalstring != ""):
            return goalstring
        else:
            return 'no goal'
    except:
        try:
            print('here')
            values = ['row1_label', 'row1_value', 'row2_label', 'row2_value']
            panelarr = [result[item] for item in values if item in result]
            goalstring = ""
            for item in panelarr:
                if item:
                    goalstring = goalstring + " " + item + " "

            if (goalstring != ""):
                return goalstring
            else:
                return 'no goal'
        except:
            return 'no goal'


def get_models_followers(date, gender, online, pages=6):
    models = []
    for page in range(1, pages):

        if online == 'online':
            url = 'https://webcamstats.com/followers.html?data={}&gender={}&online=on&page={}'.format(
                date, gender, page)
        elif online == 'viewers_online':
            url = 'https://webcamstats.com/viewers.html?data={}&gender={}&online=on&page={}'.format(
                date, gender, page)
        elif online == 'viewers':
            url = 'https://webcamstats.com/viewers.html?data={}&gender={}&page={}'.format(
                date, gender, page)
        elif online == 'followers_max_online':
            url = 'https://webcamstats.com/followers.html?data={}&gender={}&followers_from=&followers_to=30000&online=on&page={}'.format(
                date, gender, page)
        elif online == 'followers_max':
            url = 'https://webcamstats.com/followers.html?data={}&gender={}&followers_from=&followers_to=30000&page={}'.format(
                date, gender, page)
        elif online == 'squirt_online':
            url = 'https://webcamstats.com/viewers.html?data={}&gender={}&online=on&page={}'.format(
                date, gender, page)
        else:
            url = 'https://webcamstats.com/followers.html?data={}&gender={}&page={}'.format(
                date, gender, page)
        response = requests.request("GET", url, verify=False)
        soup = BeautifulSoup(response.text)
        rows = soup.findAll("tr")

        for row in rows:
            td_s = row.findAll("td")
            if td_s:
                name = td_s[1].find('a').text
                followers = td_s[2].text
                model_dict = (name, str(followers))
                models.append(model_dict)

    return models
