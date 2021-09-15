from selenium import webdriver
import json
import math
import datetime
import time
from bs4 import BeautifulSoup
import os

driver = webdriver.PhantomJS()


# Clear console screen(only works in cmd)
def clear():
    os.system("cls")


# Double
def double(list):
    for i in range(len(list)):
        start = list[i].index("-")
        a = list[i][0:start]  # str
        end = list[i].index("=")
        b = list[i][int(start) + 1:end]  # str
        add = str(b) + "-" + str(a) + str(list[i][int(end):])
        list.append(add)


# Get start time and store in global variable 'starttime'
def get_start_time():
    global starttime
    time_link = "https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=ch&date=" + date + "&venue=" + venue + "&raceno=" + raceno + ""
    driver.get(time_link)
    doc = driver.page_source
    soup = BeautifulSoup(doc, "html.parser")
    nobr = soup.findAll("nobr")
    if nobr is not None and len(nobr) > 0:
        starttime = nobr[4].text
        starttime = starttime[0:2] + starttime[3:5]
    else:
        get_start_time()


# Get win odd and return to variable 'win_list'
def get_win_odd():
    winlink = "https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=" + date + "&venue=" + venue + "&start=" + raceno + "&end=" + raceno + ""
    driver.get(winlink)
    win_doc = driver.page_source
    win_soup = BeautifulSoup(win_doc, "html.parser").text
    if win_soup is not None:
        # Link to json
        win_js = json.loads(win_soup)
        win_js = win_js["OUT"].split(";")
        for i in range(len(win_js)):
            if win_js[i][1] != "=":  # e.g.12=

                if win_js[i][5] == "=":  # e.g.12=13=
                    win_js[i] = win_js[i][3:5]
                else:
                    win_js[i] = win_js[i][3:6]

            else:  # e.g.1=

                if win_js[i][4] == "=":  # e.g.12=13=
                    win_js[i] = win_js[i][2:4]
                else:
                    win_js[i] = win_js[i][2:5]
        # Json to list(Only Win no Place)
        winlist = []
        noh = (len(win_js) - 1) / 2
        for i in range(1, int(noh + 1)):
            winlist.append(float(win_js[i]))
        return winlist
    else:
        get_win_odd()


def get_QP_odd():
    pooltotallink = "https://bet.hkjc.com/racing/getJSON.aspx?type=pooltot&date=" + date + "&venue=" + venue + "&raceno=" + raceno + ""
    driver.get(pooltotallink)
    pooltotaldoc = driver.page_source
    pooltotalsoup = BeautifulSoup(pooltotaldoc, "html.parser").text
    if pooltotalsoup is not None:
        pooltotal = json.loads(pooltotalsoup)
        Qpooltotal = pooltotal["inv"][2]["value"]  # str
        Ppooltotal = pooltotal["inv"][3]["value"]  # str

        # Calculate commission for pool total
        QCpooltotal = int(Qpooltotal) * 0.825  # float
        PCpooltotal = int(Ppooltotal) * 0.825  # float

        # Get Qodds
        Qodds = []
        Qoddslink = "https://bet.hkjc.com/racing/getJSON.aspx?type=qin&date=" + date + "&venue=" + venue + "&raceno=" + raceno + ""
        driver.get(Qoddslink)
        Qoddsdoc = driver.page_source
        Qoddssoup = BeautifulSoup(Qoddsdoc, "html.parser").text
        if Qoddssoup is not None:
            Qodd = json.loads(Qoddssoup)
            Qodd = Qodd["OUT"].split(";")
            Qodd.pop(0)
            for i in range(len(Qodd)):
                Qodd[i] = Qodd[i][0:-2]
            double(Qodd)
        else:
            get_QP_odd()

        # Sort
        numofhorse = math.ceil(math.sqrt(len(Qodd)))
        temp = []
        for i in Qodd:
            start = i.index("-")
            a = i[0:start]  # str
            end = i.index("=")
            b = i[int(start) + 1:end]  # str
            add = str(a) + "-" + str(b)
            temp.append(add)
        for i in range(numofhorse):
            Qodds.append([])
            for j in range(numofhorse):
                try:
                    Qodds[i].append([])
                    index = temp.index(str(i + 1) + "-" + str(j + 1))
                    Qodds[i][j] = Qodd[index]
                    if i + 1 <= 9:
                        if j + 1 <= 9:  # 1-2
                            Qodds[i][j] = Qodds[i][j][4:]
                        else:  # 1-11
                            Qodds[i][j] = Qodds[i][j][5:]
                    else:
                        if j + 1 <= 9:  # 13-8
                            Qodds[i][j] = Qodds[i][j][5:]
                        else:  # 13-13
                            Qodds[i][j] = Qodds[i][j][6:]
                except:
                    pass
        for i in range(len(Qodds)):
            if [] in Qodds[i]:
                Qodds[i].remove([])
            # print(Qodds[i])
        # print(Qodds)

        # Get Podds
        Podds = []
        Poddslink = "https://bet.hkjc.com/racing/getJSON.aspx?type=qpl&date=" + date + "&venue=" + venue + "&raceno=" + raceno + ""
        driver.get(Poddslink)
        Poddsdoc = driver.page_source
        Poddssoup = BeautifulSoup(Poddsdoc, "html.parser").text
        if Poddssoup is not None:
            Podd = json.loads(Poddssoup)
            Podd = Podd["OUT"].split(";")
            Podd.pop(0)
            for i in range(len(Podd)):
                Podd[i] = Podd[i][0:-2]
            double(Podd)

            numofhorse = math.ceil(math.sqrt(len(Podd)))

            # Sort
            temp = []
            for i in Podd:
                start = i.index("-")
                a = i[0:start]  # str
                end = i.index("=")
                b = i[int(start) + 1:end]  # str
                add = str(a) + "-" + str(b)
                temp.append(add)
            for i in range(numofhorse):
                Podds.append([])
                for j in range(numofhorse):
                    try:
                        Podds[i].append([])
                        index = temp.index(str(i + 1) + "-" + str(j + 1))
                        Podds[i][j] = Podd[index]
                        if i + 1 <= 9:
                            if j + 1 <= 9:  # 1-2
                                Podds[i][j] = Podds[i][j][4:]
                            else:  # 1-11
                                Podds[i][j] = Podds[i][j][5:]
                        else:
                            if j + 1 <= 9:  # 13-8
                                Podds[i][j] = Podds[i][j][5:]
                            else:  # 13-13
                                Podds[i][j] = Podds[i][j][6:]
                    except:
                        pass
            for i in range(len(Podds)):
                if [] in Podds[i]:
                    Podds[i].remove([])
                # print(Podds[i])
            # print(Podds)

        else:
            get_QP_odd()

        # Calculate money
        Qmoney = []
        for i in range(len(Qodds)):
            Qmoney.append([])
            for j in range(len(Qodds[i])):
                Qmoney[i].append([])
                if Qodds[i][j] != "SCR":
                    Qmoney[i][j] = float(QCpooltotal) / float(Qodds[i][j])
        # print(Qmoney)

        Pmoney = []
        for i in range(len(Podds)):
            Pmoney.append([])
            for j in range(len(Podds[i])):
                Pmoney[i].append([])
                if Qodds[i][j] != "SCR":
                    Pmoney[i][j] = float(PCpooltotal) / float(Podds[i][j])
        # print(Pmoney)

        # Sum up same horse
        Qsum = []
        for _ in range(len(Qodds)):
            Qsum.append([])
        for i in range(len(Qodds)):
            sum = 0
            for j in range(len(Qodds[i])):
                if Qmoney[i][j] != []:
                    sum = sum + float(Qmoney[i][j])
            Qsum[i] = sum
        # print(Qsum)

        Psum = []
        for _ in range(len(Podds)):
            Psum.append([])
        for i in range(len(Podds)):
            sum = 0
            for j in range(len(Podds[i])):
                if Pmoney[i][j] != []:
                    sum = sum + float(Pmoney[i][j])
            Psum[i] = sum
        # print(Psum)

        # Adjusted Pool Total
        QApooltotal = 0
        for i in Qsum:
            QApooltotal = QApooltotal + i
        QApooltotal = QApooltotal / 2
        # print(QApooltotal)

        PApooltotal = 0
        for i in Psum:
            PApooltotal = PApooltotal + i
        PApooltotal = PApooltotal / 2
        # print(PApooltotal)

        # Answer
        QAns = []
        for _ in range(len(Qodds)):
            QAns.append([])
        for i in range(len(Qodds)):
            QAns[i] = round(Qsum[i] / QApooltotal * 100 / 2, 2)
            # print(Qsum[i])
        # print(QAns)

        PAns = []
        for _ in range(len(Podds)):
            PAns.append([])
        for i in range(len(Podds)):
            PAns[i] = round(Psum[i] / PApooltotal * 100 / 2, 2)
        # print(PAns)

        return QAns, PAns

    else:
        get_QP_odd()


# Global variable
date = "2020-07-15"
venue = "HV"
raceno = "1"
starttime = ""
