import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo
import sys
from socket import *
from time import ctime
import os


def print_img(ht, y_fn):
    img_temp = [[0 for i in range(len(y_fn))] for i in range(ht)]
    output_temp = ""
    for i_y in range(ht):
        for i_x in range(len(y_fn)):
            img_temp[i_y][i_x] = "⬛" if y_fn[i_x]>=ht-i_y-1 else "⬜"
    for i_y in range(ht):
        for i_x in range(len(y_fn)):
            output_temp += str(img_temp[i_y][i_x])
        output_temp += "" if i_y==ht-1 else "\n"
    """ os.system("cls") """
    print(output_temp)

def wavread(path):
    info = mediainfo(path)
    print(info['channels'])
    print(info['sample_rate'])
    wavfile = AudioSegment.from_file(path, format="mp3")
    datawav = wavfile._data
    datause = np.frombuffer(datawav,dtype = np.short)
    datause.shape = -1,2
    datause = datause.T
    return datause,int(info['sample_rate'])

""" def main(amount, pic_width, pic_height, width, cut_down, fft_delay, max_fq, damping, ht):
    pic_width = 1920
    pic_height = 1080
    amount = 30
    width = 40
    cut_down = 1000000
    fft_delay = 0.1
    compress = 10
    damping = 1.2
    max_fq = 2000
    ht = 10
    list_test = sys.argv
    path = str(list_test[1])
    wavdata,sample_rate = wavread(path)
    wavdata_sum = np.abs(wavdata[0]) + np.abs(wavdata[1])
    step_count = int(float(list_test[2])*sample_rate)
    y_fn = [0 for i in range(amount)]
    wavdata_temp = wavdata_sum[step_count : int(step_count+sample_rate*fft_delay)]
    wavfreq = np.fft.rfft(wavdata_temp)
    y_original = np.abs(wavfreq)
    y_sum = [0 for i in range(amount)]
    step_long_sum = (len(y_original)/amount)//(sample_rate/2/max_fq) if (len(y_original)/amount)//(sample_rate/2/max_fq)>=1 else 1
    for i in range(amount):
        y_temp = np.sum(y_original[int(step_long_sum*i):int(step_long_sum*(i+1))])
        y_sum[i] = y_temp//cut_down
        y_fn[i] += (y_sum[i]-y_fn[i])//damping
    print_img(ht, y_fn)"""

def chk():
    amount = 30
    cut_down = 1000000
    fft_delay = 0.1
    damping = 1.2
    max_fq = 2000
    ht = 10
    path = str(input("path"))
    wavdata,sample_rate = wavread(path)
    wavdata_sum = np.abs(wavdata[0]) + np.abs(wavdata[1])
    data_temp = 0
    while True:
        """ print('waiting for connection...') """
        tcpCliSock, addr = tcpSerSock.accept()
        """ print('...connnecting from:', addr) """
        try:
            while True:
                data = tcpCliSock.recv(BUFSIZ)
                if not data:
                    break
                #tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
                tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
                data_temp = float(data)
            tcpCliSock.close()
        except:
            pass


        step_count = int(data_temp*sample_rate)
        y_fn = [0 for i in range(amount)]
        wavdata_temp = wavdata_sum[step_count : int(step_count+sample_rate*fft_delay)]
        wavfreq = np.fft.rfft(wavdata_temp)
        y_original = np.abs(wavfreq)
        y_sum = [0 for i in range(amount)]
        step_long_sum = (len(y_original)/amount)//(sample_rate/2/max_fq) if (len(y_original)/amount)//(sample_rate/2/max_fq)>=1 else 1
        for i in range(amount):
            y_temp = np.sum(y_original[int(step_long_sum*i):int(step_long_sum*(i+1))])
            y_sum[i] = y_temp//cut_down
            y_fn[i] += (y_sum[i]-y_fn[i])//damping
        print_img(ht, y_fn)


HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)
 
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
print('waiting for connection...')
chk()
