import argparse

from update_functions import *

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('--seikyo', action='store_true')
parser.add_argument('--daily', action='store_true')
parser.add_argument('--ajiya', action='store_true')
parser.add_argument('--rishoku', action='store_true')
parser.add_argument('--manly', action='store_true')
parser.add_argument('--delete', action='store_true')

args = parser.parse_args()

if args.all:
    for i in range(3,13):
        seikyo_update(table_num=i)
    daily_update()
    ajiya_update()
    rishoku_update()
    manly_update()
    delete_oldmenu()

else:
    if args.seikyo:
        for i in range(3,13):
            seikyo_update(table_num=i)
    if args.daily:
        daily_update()
    if args.ajiya:
        ajiya_update()
    if args.rishoku:
        rishoku_update()
    if args.manly:
        manly_update()
    if args.delete:
        delete_oldmenu()
