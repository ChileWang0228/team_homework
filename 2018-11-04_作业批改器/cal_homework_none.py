#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Operating system: KALI LINUX
@编译器：python3.7
@Created on 2018-11-05 14:42
@Author:ChileWang
@algorithm：
统计每一个同学的作业。
1、统计是否运行成功，如果成功，输出成功结果，如果失败，输出失败结果；
2、统计代码行数、字符数，备注行数，字符数；
"""
import subprocess
import os
import chardet
import codecs
import time


def file2utf8(path_dir, homework):
    with open('result_T07.log', 'a') as fw:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 插入时间
        fw.write('Time:%s\n' % current_time)
        student_name_dir = os.listdir(path_dir)
        for name in student_name_dir:
            excute_path = os.path.join(path_dir + name, homework)
            content = codecs.open(excute_path, 'rb').read()
            source_encoding = chardet.detect(content)['encoding']
            if source_encoding != 'utf-8':
                content = content.decode(source_encoding, 'ignore')  # .encode(source_encoding)
                codecs.open(excute_path, 'w', encoding='utf-8').write(content)
                print('convert [debug.py]....From %s --> utf-8' % source_encoding)
                fw.write('convert [debug.py]....From %s --> utf-8\n' % source_encoding)
            else:
                print('convert [debug.py]....From %s --> utf-8' % source_encoding)
                fw.write('convert [debug.py]....From %s --> utf-8\n' % source_encoding)


def get_homework_info(path_dir, homework):
    student_name_dir = os.listdir(path_dir)
    stdent_score = dict()
    for name in student_name_dir:
        stdent_score[name] = name
        excute_path = os.path.join(path_dir + name, homework)
        #  执行同学的代码，如果报错，输出到XXX_err.txt,如果成功，输出到XXX_log.txt
        excute_command = r'python ' + excute_path
        status, output = subprocess.getstatusoutput(excute_command)
        if status:
            log_dir = r'log/' + name + '_err.txt'
            with open(log_dir, 'a') as fw:
                fw.write(name + '代码执行错误！\n')
                fw.write(output)
        else:
            # 文件转换
            log_dir = r'log/' + name + '_log.txt'
            with open(log_dir, 'w') as fw:  # 将输出写入文件
                fw.write(output)
            with open(log_dir, 'r') as fr:  # 读取输出行数
                article = fr.readlines()
                output_lines = len(article)

            with open(excute_path, 'r') as fr:
                code_len = len(fr.read())  # 代码总长度
            with open(excute_path, 'r') as fr:
                code_lines = 0  # 代码行数
                beizhu_lines = 0  # 注释行数
                for line in fr:
                    code_lines += 1
                    beizhu = line.split('#')
                    if len(beizhu) > 1:
                        beizhu_lines += 1
                stdent_score['code_len'] = code_len
                stdent_score['beizhu_lines'] = beizhu_lines
                stdent_score['code_lines'] = code_lines
                print(name + '代码检查结果：')
                print('代码行数：%d,代码字符数:%d,注释行数：%d' % (stdent_score['code_lines'], stdent_score['code_len'], stdent_score['beizhu_lines']))
                print('运行成功，输出行数：%d' % output_lines)
                with open('result_T07.log', 'a') as fw:
                    fw.write(name + '代码检查结果：\n')
                    fw.write('代码行数：%d,代码字符数:%d,注释行数：%d\n' % (stdent_score['code_lines'], stdent_score['code_len'], stdent_score['beizhu_lines']))
                    fw.write('运行成功，输出行数：%d\n' % output_lines)
                    fw.write('\n')
        print()
    return stdent_score


if __name__ == "__main__":
    path = 'homework/'
    homework = 'debug.py'
    file2utf8(path, homework)  # 转utf-8码
    score_dict = get_homework_info(path, homework)
