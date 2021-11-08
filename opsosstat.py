#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Статистика по услугам оператора сотовой связи."""

import sys
import time
import argparse
import datetime
from pathlib import Path
import magic
import pandas as pd
import confuse

# sys.exit()

def get_config():
    """Get keys/values from YAML configuration file and/or options."""
    script_name = Path(__file__).stem
    conf_name = script_name + '.yaml'
    conf_path = Path(__file__).with_name(conf_name).absolute()
    conf = confuse.Configuration(script_name)
    conf.set_file(conf_path)
    desc = 'Статистика по услугам оператора сотовой связи'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--input',
        type=str,
        help='input file'
    )
    # parser.add_argument(
    #     '--output',
    #     type=str,
    #     help='output CSV file'
    # )
    args = parser.parse_args()
    conf.set_args(args, dots=True)
    return conf


def check_format(input_path):
    file_format = magic.from_file(str(input_path))
    # print(file_format)
    if (file_format == 'Microsoft OOXML'):
        return 'xlsx'
    elif (file_format.find('PDF document') != -1):
        return 'pdf'
    else:
        print('Неподдерживаемый формат входного файла.')
        print('Файл детализации должен быть в одном из форматов: PDF, XLSX.')
        sys.exit(1)


def main():
    """."""
    # get configuration keys/values
    config = get_config()
    input_file = config['input'].get()
    input_path = Path(input_file).absolute()
    file_format = check_format(input_path)
    print(file_format)


main()
