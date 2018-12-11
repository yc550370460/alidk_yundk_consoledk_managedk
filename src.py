# -*- coding:utf-8 -*-

from util.utils import *
from optparse import OptionParser
import json


if __name__ == "__main__":
    parser = OptionParser("%s parameters: AddCdnDomain\n" % sys.argv[0])
    parser.add_option("-i", "--id", dest="accesskeyid", help="specify access key id")
    parser.add_option("-s", "--secret", dest="accesskeysecret", help="specify access key secret")

    (options, args) = parser.parse_args()
    # args < 1
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    # help
    if args[0] == 'help':
        parser.print_help()
        sys.exit(0)

    # config
    if args[0] != 'config':
        option_not_exist = False if options.accesskeyid is not None or options.accesskeysecret is not None else True
        if option_not_exist:
            setup_credentials()
        else:
            print "Error: only parameter config can use options --id and --secret"
            sys.exit(1)
    else:
        if options.accesskeyid is None or options.accesskeysecret is None:
            print "Error: config miss parameters, use both --id=[accesskeyid] and --secret=[accesskeysecret]"
            sys.exit(1)
        configure_accesskeypair(args, options)
        print "Config successfully"
        sys.exit(0)

    # DescribeCdnService for test
    support_action = ["AddCdnDomain", "DescribeCdnService", "BatchSetCdnDomainConfig"]
    if sys.argv[1] in support_action:
        pass
    else:
        print("Error: not support parameter:%s" %sys.argv[1])
        parser.print_help()
        sys.exit(1)
    json_file = os.path.join(BASE_DIR, "config", sys.argv[1] + ".json")
    json_parameters = json.load(open(json_file))
    if not isinstance(json_parameters, list):
        raise Exception("Json format error, outer list format")

    # DescribeCdnService for test
    if sys.argv[1] == "DescribeCdnService":
        user_params = dict()
        user_params['Action'] = sys.argv[1]
        make_request(user_params)
        sys.exit(0)

    for item in json_parameters:
        if not item:
            raise Exception("Json format error, inner dict should not be blank")
        user_params = dict()
        user_params['Action'] = sys.argv[1]
        if not isinstance(item, dict):
            raise Exception("Json format error, inner dict format")
        for key, value in item.items():
            user_params[key] = value
        print user_params
        make_request(user_params)