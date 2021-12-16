 #-*-coding:utf-8-*-
import eyed3
import json
import MySQLdb
import time
import os

def if_empty_give_now_date(param=''):
    '''
    @ desc 如果值为空 就赋默认值 否则不做操作
    @ param param 要验证的值
    '''
    # 可否使用如下代码
    '''
    if not param:
      return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return param
    '''
    if not param:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return param

def packDict(path):
    audiofile = eyed3.load(path)
    if audiofile:
        title = audiofile.tag.title
        artist = audiofile.tag.artist
        album = audiofile.tag.album
        recording_date = audiofile.tag.recording_date.year if audiofile.tag.recording_date else None # only year
        genre = audiofile.tag.genre.name if audiofile.tag.genre else None
        album_artist = audiofile.tag.album_artist
        lyrics = audiofile.tag.lyrics[0].text if len(audiofile.tag.lyrics) > 0 else None
        minute = int(audiofile.info.time_secs/60)
        second = int(audiofile.info.time_secs%60)
        second = second if second > 10 else '0{0}'.format(second)
        time = '{0}:{1}'.format(minute, second)
        size = round(audiofile.info.size_bytes/1024/1024, 2)
        create_date = if_empty_give_now_date()
        update_date = if_empty_give_now_date()
        is_delete = 0
        audio_dict = dict(
            title=title,
            artist=artist,
            album=album,
            recording_date=recording_date,
            genre=genre,
            album_artist=album_artist,
            lyrics=lyrics,
            time=time,
            size=size,
            create_date=create_date,
            update_date=update_date,
            is_delete=is_delete
            )
        return audio_dict
    return {}

def inserdb(info):
    table = info.get('table')
    audio = info.get('audio')
    columns = ','.join(audio.keys())
    qmarks = ', '.join(['%s'] * len(audio.keys()))
    values = audio.values()
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="common_api", port=3306,charset="utf8")
    cursor = db.cursor()
    try:
        qry = "Insert Into %s (%s) Values (%s);" % (table, columns, qmarks)
        cursor.execute(qry, values)
        db.commit()
    except Exception as e:
        print(str(e))
        db.rollback


def execute():
    path = 'D:/work/other/手机歌曲/'
    for _, _, fs in os.walk(path):
        for f in fs:
            audio = packDict(path + f)
            if audio:
                table='music'
                info = dict(audio=audio,table=table)
                inserdb(info)

def getOne():
    print (packDict('D:/work/other/手机歌曲/红装.mp3'))


if __name__ == '__main__':
    execute()
    # getOne()