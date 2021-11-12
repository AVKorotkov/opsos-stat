#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Статистика по услугам оператора сотовой связи."""

import sys
import time
import argparse
import datetime
from pathlib import Path
import magic
import openpyxl
import pandas as pd
# import pdftotext
import confuse
# import PyPDF2
import fitz
# from pdfreader import PDFDocument, SimplePDFViewer

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


def check_format(ifh):
    """Check input file format."""
    file_format = magic.from_buffer(ifh.read(2048))
    if file_format == 'Microsoft OOXML':
        file_format = 'xlsx'
    elif file_format.find('PDF document') != -1:
        file_format = 'pdf'
    else:
        print('Неподдерживаемый формат входного файла.')
        print('Файл детализации должен быть в одном из форматов: PDF, XLSX.')
        sys.exit(1)

    return file_format

def check_opsos(ifh):
    """Check opsos whether it is supported."""
    file_format = check_format(ifh)
    if file_format == 'xlsx':
        wbook = openpyxl.load_workbook(ifh)
        opsos = wbook.properties.creator.lower()
        if opsos != 'beeline':
            print('Неподдерживаемый оператор.')
            print('Поддерживаются только МТС, Билайн, Теле 2.')
            sys.exit(2)
    else:
        doc = fitz.open(ifh)
        if doc.metadata['author'] == 'МТС':
            opsos = 'mts'
        else:
            page = doc[0]
            text = page.get_text("text")
            if text.find('tele2.ru') != -1:
                opsos = 'tele2'
            elif text.find('beeline.ru') != -1:
                opsos = 'beeline'
            else:
                print('Неподдерживаемый оператор.')
                print('Поддерживаются только МТС, Билайн, Теле 2.')
                sys.exit(2)

    return file_format, opsos


def main():
    """Получение статистики по услугам оператора сотовой связи."""
    # get configuration keys/values
    config = get_config()
    input_file = config['input'].get()
    input_path = Path(input_file).absolute()
    with open(input_path, 'rb') as ifh:
        file_format, opsos = check_opsos(ifh)
        print(file_format)
        print(opsos)


main()

sys.exit()
