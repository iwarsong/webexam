#!/usr/bin/env python
#-*- coding:utf-8 -*-
from webexam.models import *
from webexam.database import db_session
import MySQLdb

def str_replace(title):
    sr={'&amp;':' ','&quot;':'"','lt;':'<','gt;':'>'}
    for k,v in sr.items():
        title = title.replace(k,v)
    return title

def load_lib():
    libs=[]
    db = MySQLdb.connect("192.168.56.110","root","mysql@cs2003","db_webexam")
    cursor = db.cursor()
    cursor.execute("select * from subjectlib where libcreatedate>='2013-9-1' order by libcreatedate desc")
    for x in cursor:
        libname = x[2].decode('utf-8')
        lib = Lib(libname=libname)
        db_session.add(lib)
        db_session.commit()
        sections = load_section(x[0],lib.id)
        obj_lib={'libname':libname,'guid':x[0],'id':lib.id,'sections':sections}
        libs.append(obj_lib)

        #print libname
        #break
    db.close()

    return libs

def load_section(libguid,libid):
    section_objs=[]
    db = MySQLdb.connect("192.168.56.110","root","mysql@cs2003","db_webexam")
    cursor = db.cursor()
    cursor.execute("select * from subjectsection where libid='%s'"%(libguid))
    for x in cursor:
        sectionname = x[2].decode('utf-8')
        sectionorder=x[3]
        section = Section(libid=libid,sectionname=sectionname,sortorder=sectionorder)
        db_session.add(section)
        db_session.commit()
        obj_section={'guid':x[0],'id':section.id}
        section_objs.append(obj_section)
        #break
    db.close()

    return section_objs

def load_subject(libs):
    subject_total = 0
    db = MySQLdb.connect("192.168.56.110","root","mysql@cs2003","db_webexam")
    cursor = db.cursor()
    for lib in libs:
        for section in lib['sections']:
            cursor.execute("select * from subject where subjectsectionid='%s'"%section['guid'])
            for x in cursor:
                subject = Subject()
                subject_type = x[1]
                if subject_type == 'Judge' or subject_type == 'SingleSel' or subject_type == 'MultiSel':
                    subject.subjecttype=subject_type
                    subject.sectionid=section['id']
                    subject.title = str_replace(x[2].decode('utf-8'))
                    subject.degree= 'normal'
                    db_session.add(subject)
                    db_session.commit()
                    #
                    options = load_option(x[0],subject.id)
                    load_answer(x[0],subject.id,options)
                    #
                    subject_total += 1
        print lib['libname']
    db.close()

    return subject_total

def load_option(subjectguid,subjectid):
    options = []
    db = MySQLdb.connect("192.168.56.110","root","mysql@cs2003","db_webexam")
    cursor = db.cursor()
    cursor.execute("select * from subjectoption where subjectid='%s' order by optionsortorder"%subjectguid)
    sortorder = 1
    for x in cursor:
        option = Option()
        option.subjectid = subjectid
        option.title = str_replace(x[2].decode('utf-8'))
        option.sortorder = sortorder
        sortorder += 1
        db_session.add(option)
        db_session.commit()
        option_obj = {'guid':x[0],'sortorder':str(option.sortorder)}
        options.append(option_obj)

    db.close()

    return options

def load_answer(subjectguid,subjectid,options):
    db = MySQLdb.connect("192.168.56.110","root","mysql@cs2003","db_webexam")
    cursor = db.cursor()
    cursor.execute("select * from subjectanswer where subjectid='%s'"%subjectguid)
    answer = Answer()
    answer.subjectid = subjectid
    a = []
    for x in cursor:
        if x[2] == 'True' or x[2] == 'False':
            a.append(x[2])
            break
        else:
            b = x[2].split(',')
            for c in b:
                for op in options:
                    if c == op['guid']:
                        a.append(op['sortorder'])
                        break
            break
    answer.answervalue = ''.join(a)
    db_session.add(answer)
    db_session.commit()

    db.close()

def main():
    libs = load_lib()
    total = load_subject(libs)
    print "Done...Total:%s"%total

if __name__ == '__main__':
    main()
