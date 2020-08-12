import os
import enum
import argparse

from env.get_account import *

from automation import make_tms_list as tms
from automation import make_ems_list as ems
from automation import make_redir_list as redir
from automation import make_url_list as weburl
from automation import make_bizno_list as bizno
from automation import check_pm_list as pm
from automation import url_creator as url
from automation import pf_extractor as pf
from automation import pf_extractor2 as pf2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing Type')
    parser.add_argument('--type', metavar='N', type=str, nargs='?', default="real",
                        help='Automation Type : url / tms / redir / weburl / bizno / ems / pf / pf2 / pm')
    args = parser.parse_args()
    args = args.type

    input_path = f'{os.getcwd()}/Desktop/generator/input.csv'
    input_uri_path = f'{os.getcwd()}/Desktop/generator/input_uri.csv'
    input_url_path = f'{os.getcwd()}/Desktop/generator/input_url.csv'
    url_path = f'{os.getcwd()}/Desktop/generator/URL.csv'
    tms_path = f'{os.getcwd()}/Desktop/generator/TMSlist.csv'
    redir_path = f'{os.getcwd()}/Desktop/generator/REDIRlist.csv'
    weburl_path = f'{os.getcwd()}/Desktop/generator/WEBURLlist.csv'
    bizno_path = f'{os.getcwd()}/Desktop/generator/BIZNOlist.csv'
    ems_path = f'{os.getcwd()}/Desktop/generator/EMSlist.csv'
    pf_path = f'{os.getcwd()}/Desktop/generator/PFlist.csv'
    pf_path2 = f'{os.getcwd()}/Desktop/generator/PFlist2.csv'
    setting_path = f'{os.getcwd()}/Desktop/generator/core/env/setting.json'

    admin_id = get_admin_id(setting_path)
    admin_pw = get_admin_pw(setting_path)

    if args == "url":
        url.run(input_path, url_path)
    elif args == "tms":
        tms.run(input_path, tms_path, admin_id, admin_pw)
    elif args == "redir":
        redir.run(input_uri_path, redir_path, admin_id, admin_pw)
    elif args == "weburl":
        weburl.run(input_url_path, weburl_path, admin_id, admin_pw)
    elif args == "bizno":
        bizno.run(input_path, bizno_path, admin_id, admin_pw)
    elif args == "ems":
        ems.run(input_path, ems_path, admin_id, admin_pw)
    elif args == "pf":
        pf.run(input_path, pf_path, admin_id, admin_pw)
    elif args == "pf2":
        pf2.run(input_path, pf_path2, admin_id, admin_pw)
    elif args == "pm":
        pm.run(input_path, admin_id, admin_pw)
    else:
        pass
