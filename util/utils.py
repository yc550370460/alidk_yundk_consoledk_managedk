# -*- coding:utf-8 -*-

import sys, os
import urllib
import base64
import hmac
from hashlib import sha1
import time
import uuid
import ConfigParser
import traceback
import requests

PWD = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(PWD))
CONFIGFILE= os.path.join(BASE_DIR, "config", "config.ini")
access_key_id = ''
access_key_secret = ''
cdn_server_address = 'https://cdn.aliyuncs.com'
CONFIGSECTION = 'Credentials'
cmdlist = '''
接口说明请参照pdf文档
'''


def percent_encode(str):
    res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)

    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])

    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = {'Format': 'JSON',
                  'Version': '2018-05-10',
                  'AccessKeyId': access_key_id,
                  'SignatureVersion': '1.0',
                  'SignatureMethod': 'HMAC-SHA1',
                  'SignatureNonce': str(uuid.uuid1()),
                  'Timestamp': timestamp
        }

    for key in user_params.keys():
        parameters[key] = user_params[key]
    print parameters
    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = cdn_server_address + "/?" + urllib.urlencode(parameters)
    return url


def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    print url
    resp = requests.get(url)
    print resp, resp.content


def configure_accesskeypair(args, options):
    config = ConfigParser.RawConfigParser()
    config.add_section(CONFIGSECTION)
    config.set(CONFIGSECTION, 'accesskeyid', options.accesskeyid)
    config.set(CONFIGSECTION, 'accesskeysecret', options.accesskeysecret)
    cfgfile = open(CONFIGFILE, 'w+')
    config.write(cfgfile)
    cfgfile.close()


def setup_credentials():
    config = ConfigParser.ConfigParser()
    try:
        config.read(CONFIGFILE)
        global access_key_id
        global access_key_secret
        access_key_id = config.get(CONFIGSECTION, 'accesskeyid')
        access_key_secret = config.get(CONFIGSECTION, 'accesskeysecret')
    except Exception, e:
        print traceback.format_exc()
        print("can't get access key pair, use config --id=[accesskeyid] --secret=[accesskeysecret] to setup")
        sys.exit(1)


if __name__ == '__main__':
    pass

