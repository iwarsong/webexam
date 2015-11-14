#!/usr/bin/env python
#-*- coding:utf-8
import re
import codecs

lib = u'人资普考2015'
section = u'培训及人才开发'
level = u'普通'
filename = '6.txt'
filename_out = '1.out.txt'

def get_file_context():
    f = codecs.open(filename, "r", "utf-8")
    lines = f.readlines()
    f.close()

    return lines

def get_title(line):
    pattern_re = r'\d*\.'
    title = ''
    m = re.findall(pattern_re,line)
    if len(m)>0:
        title = re.sub(pattern_re,'',line)
    return title

def get_options(line):
    char_order = ('B.','C.','D.','E.','F.')
    line = line.replace('A.','')
    for c in char_order:
        line = line.replace(c,'$$')
    options = line.split('$$')

    return options

def get_answer(line):
    answer_char=('A','B','C','D','E','F')
    answer = ''
    for c in answer_char:
        if c in line:
            answer += c
    return answer

def get_subject_type(answer):
    if len(answer)>1:
        return u'多选题'
    if len(answer) == 1:
        return u'单选题'

    return ''

def process_subject(file_lines):
    subjects = []
    line_index = 0
    while True:
        if line_index+2 >= len(file_lines):
            break
        str_title = file_lines[line_index].strip()
        str_options = file_lines[line_index+1].strip()
        str_answer = file_lines[line_index+2].strip()
        if str_title == '' or str_options == '' or str_answer == '':
            break

        title = get_title(str_title)
        options = get_options(str_options)
        answer = get_answer(str_answer)
        subject_type = get_subject_type(answer)

        if len(options)<4:
            print u'line %s get options fail,please check' %(line_index+1)
            print len(options)
            #print str_title,str_options,str_answer
            return None
        if subject_type == '':
            print u'line %s get subject type fail,please check' %(line_index+1)
            #print str_title,str_options,str_answer            
            return None
        subject = []
        subject.append(subject_type)
        subject.append(lib)
        subject.append(section)
        subject.append(level)
        subject.append(title)
        subject.append(answer)
        for o in options:
            subject.append(o.strip())
        subjects.append(subject)

        line_index += 3

    return subjects

def save_file(subjects):
    f = codecs.open(filename_out, "w", "utf-8")
    for s in subjects:
        f.write('\t'.join(s))
        f.write('\r\n')
    f.close()

def main():
    file_lines = get_file_context()
    subjects = process_subject(file_lines)
    if subjects is not None:
        save_file(subjects)
        print 'total:%s'%(len(subjects))

if __name__ == '__main__':
    main()
