init -990 python:
    store.mas_submod_utils.Submod(
        author="huhu233",
        name="A test",
        description="A test submod for audio visualization.",
        version='1.0.1'
    )

init 5 python:
    addEvent(
            Event(
                persistent.event_database,
                eventlabel="test_topic1",
                category=["test"],
                prompt="test",
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )

#init 5 python:
#    addEvent(
#            Event(
#                persistent.event_database,
#                eventlabel="test_topic_pip",
#                category=["test"],
#                prompt="安装依赖包",
#                pool=True,
#                unlocked=True
#            ),
#        restartBlacklist=True
#        )

init 5 python:
    addEvent(
            Event(
                persistent.event_database,
                eventlabel="test_topic_sentmsg",
                category=["test"],
                prompt="开始发送信息",
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )

init 5 python:
    addEvent(
            Event(
                persistent.event_database,
                eventlabel="test_topic_sentmsg_end",
                category=["test"],
                prompt="关闭线程",
                pool=True,
                unlocked=True
            ),
        restartBlacklist=True
        )

label test_topic_sentmsg_end:
    python:
        end_msg = 1
    m "已关闭。"
    return

label test_topic_sentmsg:
    python:
        import threading
        from socket import *
        import inspect
        import ctypes
        end_msg = 0
        def _async_raise(tid, exctype):
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        def stop_thread(thread):
            _async_raise(thread.ident, SystemExit)
        def debug_sent1(debug_text):
            HOST = '127.0.0.1'
            PORT = 21567
            BUFSIZ =1024
            ADDR = (HOST,PORT)
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            chk = 0
            try:
                tcpCliSock.connect(ADDR)
                data1 = str(debug_text)
                tcpCliSock.send(data1.encode())
                data1 = tcpCliSock.recv(BUFSIZ)
                chk = 1
            except:
                pass
            if chk == 1:
                tcpCliSock.close()
            else:
                pass
        class sentmsg_Thread(threading.Thread):
            def __init__(self,msg):
                threading.Thread.__init__(self)
                self.msg = msg
            def run(self):
                debug_sent1(renpy.music.get_playing(channel='music'))
                i_endtest = 0
                time_temp = 0
                while True:
                    time_temp2 = time_temp
                    time_temp = renpy.music.get_pos(channel='music')
                    if i_endtest <= time_temp:
                        i_endtest = time_temp
                        if time_temp != time_temp2:
                            debug_sent1(time_temp)
                        if end_msg == 1:
                            stop_thread(self)
                    else:
                        stop_thread(self)
        thread_1 = sentmsg_Thread("msg")
        thread_1.start()
    m "已开启。"
    return

#label test_topic_pip:
#    m "正在检测"
#    python:
#        i_packtest = 0
#        import os
#        try:
#            os.system("pip install --target game/python-packages numpy pydub")
#            i_packtest = 1
#        except:
#            i_packtest = 2
#    if i_packtest == 1:
#        m "正在安装，请重新启动mas。"
#    elif i_packtest == 2:
#        m "安装失败。"
#    return
        





label test_in1:
    m "test."
    return
label test_in2:
    m "连接失败."
    return
label test_in3:
    m "连接成功."
    return


label test_topic1:
    python:
        import os
        sent_text = ""
        music_file = renpy.music.get_playing(channel='music')
        sent_text += str(music_file)
        music_time = renpy.music.get_pos(channel='music')
        sent_text += str(music_time)
        #command = "start cmd /K echo "+command_temp
        #os.system(command)
        #renpy.call("test_in1")
    m "Wait."
    python:
        from socket import *
        def debug_sent(debug_text):
            HOST = '127.0.0.1'
            PORT = 21567
            BUFSIZ =1024
            ADDR = (HOST,PORT)
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            chk = 0
            try:
                tcpCliSock.connect(ADDR)
                data1 = str(debug_text)
                data1 = str(data1)
                tcpCliSock.send(data1.encode())
                data1 = tcpCliSock.recv(BUFSIZ)
                chk = 1
            except:
                pass
            if chk == 1:
                tcpCliSock.close()
                renpy.call("test_in3")
            else:
                renpy.call("test_in2")
        debug_sent("Hello form Monika")
    m "Wait more..."
    python:
        debug_sent(sent_text)
    m "OK."
    return
