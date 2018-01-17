# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    author: Noémi Vadász
    last update: 2017.12.30.

    Script to preprocess the test file to magyarlanc (http://www.inf.u-szeged.hu/rgai/magyarlanc) dependency parser
    to run magyarlanc: java -Xmx2G -jar magyarlanc-3.0.jar -mode depparse -input in.txt -output out.txt
"""


def readtext():
    """
    read manually annotated results
    read results of vframe
    write the two results aligned by sentences for evaluation
    :return: None
    """

    with open('test_data/final_test.txt', encoding='UTF-8') as infile, \
            open('temp/to_magyarlanc', 'w', encoding='UTF-8') as outfile:

        for line in infile:
            for word in line.split():
                print(word.split('/')[0], end=' ', file=outfile)
            print('', file=outfile)

    outfile.close()

    return None


def main():
    readtext()


if __name__ == '__main__':
    main()
