import pyperclip
from colorama import Fore
import time
import os
import pyautogui
import pyperclip
from threading import Thread
import cv2
import numpy as np
import random
import time
import platform
import subprocess
import os
import mss
import requests

# region imagesearch module
# region retina
is_retina = False
if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True) == 0
# endregion

# region region_grabber
def region_grabber(region):
    if is_retina: region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]
    region = x1, y1, width, height
    with mss.mss() as sct:
        return sct.grab(region)
# endregion

# region click_image
def click_image(image, pos, action, timestamp, offset=5):
    img = cv2.imread(image)
    if img is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     timestamp)
    pyautogui.click(button=action)
# endregion

# region imagesearch
def imagesearch(image, precision=0.8):
    with mss.mss() as sct:
        im = sct.grab(sct.monitors[0])
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
        # im.save('testarea.png') useful for debugging purposes, this will save the captured region as "testarea.png"
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        if template is None:
            raise FileNotFoundError('Image file not found: {}'.format(image))
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc
# endregion

# region imagesearch_loop
# endregion
def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        #print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos
# endregion

f = open("./chat.txt", "r", encoding="utf-8")
chatting = f.readline()

def auto_accept():
    while True:
        accept_pos = imagesearch_loop("./image/accept.png", 0.1)
        if accept_pos[0] != 1:
            click_image("./image/accept.png", accept_pos, 'left', 0.1)
        #print(' [>] 수락 완료')
        time.sleep(10)

def auto_ban():
    print(' [>] 밴창 대기중...')
    ban1_pos = imagesearch_loop("./image/ban1.png", 0.1)
    if ban1_pos[0] != 1:
        click_image("./image/ban1.png", ban1_pos, 'left', 0.1)
    print(' [>] 밴 챔피언 선택 완료')
    print(' [>] 밴 버튼 대기중...')
    ban2_pos = imagesearch_loop("./image/ban2.png", 0.1)
    time.sleep(0.5)
    if ban2_pos[0] != 1:
        click_image("./image/ban2.png", ban2_pos, 'left', 0.1)
    print(' [>] 밴 버튼 클릭')
    main()

def auto_chat():
    print(' [>] 라인 잡기 대기중...')
    search_pos = imagesearch_loop("./image/search1.png", 0.01)
    chat_pos = imagesearch_loop("./image/chat.png", 0.1)
    if chat_pos[0] != 1:
        click_image("./image/chat.png", chat_pos, 'left', 0.1)
    for i in range(7):
        pyperclip.copy(chatting)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
    main()
    
def auto_pick():
    time.sleep(100)
def working():
    while True:
        os.system('title [ Hyuk Console ] 오토수락 작동상태 : Good ●')
        time.sleep(0.1)
        os.system('title [ Hyuk Console ] 오토수락 작동상태 : Good  ●')
        time.sleep(0.1)
        os.system('title [ Hyuk Console ] 오토수락 작동상태 : Good   ●')
        time.sleep(0.1)
        
def r(num, rand):
    return num + rand * random.random()

def main():
    os.system('cls')
    print(Fore.LIGHTCYAN_EX+'''
 │ LOL Auto Client                              
 │ Made by Hyuk

 1 > [랭크] 오토밴
 2 > [랭크] 오토밴 + 오토픽 (추가중)
 3 > [일반] 라인잡기
 4 > [설명] 설정법

 [>] 프로그램 시작시 오토수락은 자동으로 켜집니다
 [>] 오토밴은 '없음' 으로 밴됩니다
 [>] 라인잡기 설정법 : 폴더 안에 있는 chat.txt 파일을 열고 수정해주시면됩니다
 [>] 예) 탑으로 저장할시 채팅칠떄 탑으로 쳐지고 ㅈㄱ이라고 저장할시 채팅칠떄 ㅈㄱ이라고 쳐집니다
 [>] 현재 설정된 라인 : '''+chatting+Fore.RESET+'\n')
    num_select = int(input(' [>] 번호를 선택해주세요 : '))
    if num_select == 1:
        auto_ban()
    if num_select == 2:
        #auto_ban()
        #auto_pick()
        print(' [>] 추가중입니다')
        os.system('pause')
        main()
    if num_select == 3:
        auto_chat()
    if num_select == 4:
        print(' [>] 라인잡기 설정법 : 폴더 안에 있는 chat.txt 파일을 열고 수정해주시면됩니다')
        print(' [>] 예) 탑으로 저장할시 채팅칠떄 탑으로 쳐지고 ㅈㄱ이라고 저장할시 채팅칠떄 ㅈㄱ이라고 쳐짐')
        os.system('pause')
        main()
    else:
        print(' [>] 없는 기능입니다.')
        os.system('pause')
        main()

def test():
    while True:
        print('1')

if __name__ == '__main__':
    t = Thread(target = auto_accept)
    tr = Thread(target=working)
    #t.daemon = True #프로세스 종료시 쓰레드 종료
    t.start()
    tr.start()
    main()