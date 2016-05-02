# -*- coding: UTF-8 -*-
import re,urllib
import urllib2
import BeautifulSoup
# import pprint
# class MyPrettyPrinter(pprint.PrettyPrinter):
#     def format(self, _object, context, maxlevels, level):
#         if isinstance(_object, unicode):
#             return "'%s'" % _object.encode('utf8')
#         elif isinstance(_object, str):
#             _object = unicode(_object,'utf8')
#             return "'%s'" % _object.encode('utf8')
#         return ppself

resultFile= file('result.csv','wt')

f = file('file.txt')
line = f.readline()
while line:
    aaaa=line.split(',')
    line = f.readline()
    _object=unicode(aaaa[0],'utf8')
    title = "'%s'" % _object.encode('utf8')
    category = int(aaaa[1])
    title = title.strip("'")
    if(category==1):
        url='http://www.tosarang1.net/bbs/board.php?bo_table=torrent_kortv_ent&sca=&sfl=wr_subject&stx='+title+'&sop=and'
    elif(category==2):
        url='http://www.tosarang1.net/bbs/board.php?bo_table=torrent_kortv_social&sca=&sfl=wr_subject&stx='+title+'&sop=and'
    elif(category==3):
        url='http://www.tosarang1.net/bbs/board.php?bo_table=torrent_kortv_drama&sca=&sfl=wr_subject&stx='+title+'&sop=and'
    myurl = url
    # myurl = '''http://www.tosarang1.net/bbs/board.php?bo_table=torrent_kortv_ent&sca=&sfl=wr_subject&stx=%EB%AC%B4%ED%95%9C%EB%8F%84%EC%A0%84&sop=and'''
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    req = urllib2.Request(myurl)
    html = urllib.urlopen(myurl)
    req = urllib2.Request(myurl)
    req.add_header("User-agent", user_agent) # 헤더추가
    req.add_header("Cookie", "cookiename=cookievalue") # 쿠키 추가
    response = urllib2.urlopen(req)
    headers = response.info().headers #응답 헤더
    the_page = response.read()
    # print the_page
    pagecnt =0
    for i in re.findall('''<td class="subject">\n<a href='.*sop=and'>''', the_page, re.I):
        pagecnt=pagecnt+1
        a= i.strip('''<td class="subject">\n<a href='')+"\n"''')
        inurl ='http://www.tosarang1.net/'+a.strip("'../")
        in_req=urllib2.Request(inurl)
        in_req.add_header("User-agent", user_agent) # 헤더추가
        in_req.add_header("Cookie", "cookiename=cookievalue") # 쿠키 추가
        in_response = urllib2.urlopen(in_req)
        in_page = in_response.read()
        soup = BeautifulSoup.BeautifulSoup(in_page)

        for j in re.findall('''[0-9]{1,8}&nbsp;명''', in_page, re.I):
            resultFile.write(title+",")
            resultFile.write(j.strip('&nbsp;명')+",")
            
            sub_title = soup.title.string    
            #날짜찾기
            day = re.findall(r"[0-9]{6}",sub_title)
            if(len(day)!=0):
                resultFile.write(day[0]+",")
            else:
                resultFile.write("000000,")
            #회 찾기            
            ccnt = re.findall(r"E[0-9]{1,4}",sub_title)
            if(len(ccnt)!=0):
                resultFile.write(ccnt[0]+",\n")
            else:
                resultFile.write("E000"+",\n")
    print "check"
pnum = 2
while(pagecnt == 20):  #20개씩 체워진 컨텐츠에 4페이지까지있음 찾는다. 
    pagecnt=0
    myurl1 = myurl+'&page='+str(pnum)
    print myurl1
    eq1 = urllib2.Request(myurl1)
    html1 = urllib.urlopen(myurl1)
    req1 = urllib2.Request(myurl1)
    req1.add_header("User-agent", user_agent) # 헤더추가
    req1.add_header("Cookie", "cookiename=cookievalue") # 쿠키 추가


    response1 = urllib2.urlopen(req1)
    headers1 = response1.info().headers #응답 헤더
    the_page1 = response1.read()
    pagecnt =0
    print "z"
 
    for i in re.findall('''<td class="subject">\n<a href='.*sop=and&page='''+str(pnum), the_page1, re.I):
            print pagecnt
            pagecnt=pagecnt+1
            a= i.strip('''<td class="subject">\n<a href='')+"\n"''')
            inurl ='http://www.tosarang1.net/'+a.strip("'../")
            print inurl
            in_req=urllib2.Request(inurl)
            in_req.add_header("User-agent", user_agent) # 헤더추가
            in_req.add_header("Cookie", "cookiename=cookievalue") # 쿠키 추가
            in_response = urllib2.urlopen(in_req)
            in_page = in_response.read()
            soup = BeautifulSoup.BeautifulSoup(in_page)

            for j in re.findall('''[0-9]{1,8}&nbsp;명''', in_page, re.I):
                print soup.title.string+" - "+j.strip('&nbsp;명')+"\n"
    pnum=pnum+1
    print pagecnt


f.close()
resultFile.close()