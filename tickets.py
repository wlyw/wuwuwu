#coding: utf-8

'''

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets -g 合肥 上海 2016-11-26
'''

import json
import chardet
import requests
from docopt import docopt
from pprint import pprint
from prettytable import PrettyTable
from colorama import init,Fore

init()

class TrainCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self,available_trains,options):
        '''
        available_trains: 查询到的火车列表
        options: 查询选项，如高铁，动车，etc...
        '''
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self,raw_train):
        duration = raw_train.get('lishi').replace(':','小时')+'分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    def trains(self):
        for raw_train in self.available_trains:
            train_no = raw_train['station_train_code']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + raw_train['from_station_name'] + Fore.RESET,
                                Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,
                                Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                    self._get_duration(raw_train),
                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num'],
                ]
                yield train
    
    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains():
            pt.add_row(train)
        print(pt)

def cli():
    'command-line interface'
    arguments = docopt(__doc__)
    #print(arguments)
    stations = json.load(open('stations.json'))

    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date,from_station,to_station)
    r = requests.get(url,verify=False)

    options = ''.join([key for key, value in arguments.items() if value is True])
    available_trains = r.json()['data']['datas']
    TrainCollection(available_trains,options).pretty_print()

if __name__ == '__main__':
    cli()