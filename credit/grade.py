# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import string
import types

import ConfigParser
import logging
import logging.config
CONF_LOG = 'G:/Python/Pycharm/GPA/credit/logging.conf'
logging.config.fileConfig(CONF_LOG)
logger = logging.getLogger('root')
class Term:
    time = ""
    id = ""
    courses_list = []
    def __init__(self, id, time, courses_list):
        self.id = id
        self.time = time
        self.courses_list = courses_list
    def __str__(self):
        return self.id+' '+self.time+' '+self.name+' '+self.courses_list

class Course:
    id = ""
    time = ""
    name = ""
    weight = 0.0
    grade = 0.0
    def __init__(self, id, time, name, weight, grade):
        self.id = id
        self.time = time
        self.name = name
        self.weight = weight
        self.grade = grade
    def __str__(self):
        return self.id+' '+self.time+' '+self.name+' '+str(self.weight)+' '+str(self.grade)


class NPU:

    def __init__(self,name,passwd):
        #登录URL
        self.loginUrl = 'http://us.nwpu.edu.cn/eams/login.action'
        #本学期成绩URL
        self.gradeUrl = 'http://us.nwpu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR'
        self.cookies = cookielib.MozillaCookieJar('cookie.txt')
        self.postdata = urllib.urlencode({
            'username':name,
            'password':passwd,
            'encodedPassword':'',
            'session_locale':'zh_CN',
         })
        logger.info(name+'   login')
        #成绩对象数组
        #构建opener
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    #获取本学期成绩页面
    def getPage(self):
        try:
            request  = urllib2.Request(url = self.loginUrl,data = self.postdata)
            #建立连接，模拟登陆
            result = self.opener.open(request)
            self.cookies.save(ignore_discard = True, ignore_expires = True)
            #打印登录内容
            #print 'asdf'
            #print result.read()
            #获得成绩界面的html
            result = self.opener.open(self.gradeUrl)
            return result.read().decode('utf-8')
        except urllib2.URLError,e:
            #print '连接失败'
            logger.error('login error 账号或密码错误')
            if hasattr(e,"reason"):
                print e
                logger.error("error:"+e.reason)
                return None
    #成功，返回列表，失败返回空
    def getGrades(self, page):
        #print page
        reg = 'not find#$$'
        tablelen11= '<tr>\s*?<th  w.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?</tr>'
        tablelen12= '<tr>\s*?<th  w.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?</tr>'
        tablelen13= '<tr>\s*?<th  w.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?</tr>'
        tablelen14= '<tr>\s*?<th  w.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?<th.*?</th>\s*?</tr>'
        if re.search(u'补考成绩', page) and re.search(u'实验成绩', page) and re.findall(tablelen14, page,re.S):
            print '14'
            reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        elif (re.search(u'补考成绩', page) or re.search(u'实验成绩', page)) and re.search(tablelen13, page,re.S):
            print '13'
            reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        elif re.search(tablelen12, page,re.S):
            print '12'
            reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        elif re.search(tablelen11, page,re.S):
            print '11'
            reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        #if re.findall(u'补考成绩', page):
            #print '含补考成绩'
            #reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        #else:
            #reg = '<tr>\s*?<td>(.*?)</td>.*?<td.*?<td.*?<td><a href=".*?>(.*?)</a>.*?<t.*?'+'<td>(.*?)</td.*?<td.*?<td.*?<td.*?<td.*?<td.*?<t.*?>\s*(\w*).*?<.*?<t.*?</tr>'
        myItems = re.findall(reg, page, re.S)
        if myItems:
            logger.info('查询成功')
        else:
            logger.info('查询失败')
        grade_dict = {}
        terms = []
        term_list = []
        cnt = 1
        for item in myItems:
            #print item[0],item[1],item[2],item[3]
            #print item[0].encode('utf-8'),item[1].encode('utf-8'),item[2].encode('utf-8'),item[3].encode('utf-8')
            #print type(item[0]), type(item[1]), type(item[2]), type(item[3])
            if re.match('^\d+\.?\d*$', item[2]) and re.match('^\d+\.?\d*$', item[3]):
                courseid = 'course_'+str(cnt)
                cnt = cnt+1
                if not grade_dict.has_key(item[0].encode('utf-8')):
                    grade_dict[item[0].encode('utf-8')] = []
                    terms.append(item[0].encode('utf-8'))
                grade_dict[item[0].encode('utf-8')].append(Course(courseid, item[0].encode('utf-8'),item[1].encode('utf-8'),string.atof(item[2]),string.atof(item[3])))
        termcnt = 1
        for k in terms:
            termid = 'term_'+str(termcnt)
            termcnt = termcnt + 1
            list = grade_dict[k]
            term_list.append(Term(termid, list[0].time, list))
            # for i in list:
            #     print i
        return term_list
    def getCredit(self, termlist):
        #计算总绩点
        sum = 0.0
        weight = 0.0
        for term in termlist:
            for course in term.courses_list:
                sum = sum + course.weight*course.grade
                weight = weight + course.weight

        return sum,weight


if __name__ == 'grade':
    # page = npu.getPage()
    # list = npu.getGrades(page)
    # for term in list:
    #     print  term.id, term.time
    #     for course in term.courses_list:
    #         print course.id, course.name
    # sum, weight = npu.getCredit(list)
    # print sum/weight
    logger.info('我被调用了')