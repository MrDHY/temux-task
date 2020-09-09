#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time  : 2020/9/8 20:46

import time
import schedule
import subprocess


def force_start_process(shell_info):
    """
    启动shell命令
    :param shell_info:
    :return:
    """
    result = subprocess.Popen(shell_info, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    stdout = str(result.stdout.read().decode()).strip()
    # 说明frida服务已经启动
    if stdout.find("Address already in use") != -1:
        return True

    # 进程数为1
    if stdout == "1":
        return True
    print("shell result {}".format(stdout))


def job():
    # 启动frida
    frida_shell = "/data/local/tmp/fs -D -l 172.16.18.90"
    # 查看抖音进程数
    douyin_process_count = "ps -ef|grep com.ss.android.ugc.aweme|grep -v grep|grep -v" \
                           " com.ss.android.ugc.aweme:bm|grep -v com.ss.android.ugc.aweme:push|wc -l"

    # 启动抖音
    douyin_shell = "am start -n com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.splash.SplashActivity"

    force_start_process(frida_shell)
    # 查看抖音的进程数
    douyin_process = force_start_process(douyin_process_count)
    if not douyin_process:
        force_start_process(douyin_shell)


def main():
    # 每5秒执行一次
    schedule.every(5).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
