#!/usr/bin/python3

import os
import cv2
import time
import sys
import pymysql
import time
import requests
import socket
from multiprocessing import Pool
import configparser
import substream

config = configparser.ConfigParser()
config.read("/root/scripts/VIDEO/config.ini")
host_ip = socket.gethostbyname(socket.gethostname())


def get_cursor():
    connection = pymysql.connect(
        host=config['MySQL']['host'],
        user=config['MySQL']['user'],
        password=config['MySQL']['password'],
        database=config['MySQL']['database'])

    return connection.cursor(), connection


def select_ip_list():
    cursor, connection = get_cursor()
    cursor = connection.cursor()
    query = """SELECT `ip`, CONCAT(REPLACE(`ip`,'.','_'), '-' , `country_code`, '-', `region`, '-', `city`) as 'name_camera'
               FROM rtsp_scan where `url` is NULL and `up` = %s;"""
    cursor.execute(query, (os.uname()[1],))
    return cursor.fetchall()



cursor, connection = get_cursor()
cursor = connection.cursor()
query = "SELECT `path`, `login`, `passwd` FROM `view_support_path_default`"
cursor.execute(query)
link_list = cursor.fetchall()


def insert_url(link_one, ip, link, login, passwd):
    cursor, con = get_cursor()
    cursor = con.cursor()

    query = """UPDATE `rtsp_scan` SET `url` = %s, `up` = %s, `link` = %s, `login` = %s, `passwd` = %s
               WHERE `ip` = %s;"""
    cursor.execute(query, (link_one, os.uname()[1], link, login, passwd, ip))
    con.commit()


def job(ip):

    try:
        cap = cv2.VideoCapture(ip[0])
        ret, frame = cap.read()
        if ret:
            print(ip)
            name_file = f"/var/www/html/scan/{ip[2]}.jpg"
            url_link = f"http://admin:sdcsdtu-GdgLLJmm@{host_ip}/scan/{ip[2]}.jpg"
            cv2.imwrite(name_file, frame)

            insert_url(ip[0], ip[1], url_link, ip[3], ip[4])
            return

        else:
            return
    except Exception as e:
        return


def main():
    for link in link_list:
        rtsp_list = []
        for ip in select_ip_list():
            rtsp_list.append([link[0].replace('ip_for_replace', ip[0]), ip[0], ip[1], link[1], link[2]])

        start = time.time()
        with Pool(processes=200) as p:
            p.map(job, rtsp_list)
        print("And start sleep")
        end = time.time()
        sl_tm = 300 - int((end - start))
        print(sl_tm)
        if sl_tm > 0:
            time.sleep(sl_tm) # чекаємо 5 хв


if __name__ == "__main__":
    start_time = time.time()
    main()
    done = time.time() - start_time

    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
    
    if TOKEN and CHAT_ID:
        SEND_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(SEND_URL, json={'chat_id': CHAT_ID, 'text': f"41_scan_stream_default done - {int(done)}"})
        
    substream.main() 
