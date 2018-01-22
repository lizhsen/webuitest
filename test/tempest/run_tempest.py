#!/usr/bin/env python


# Copyright (C) 2015 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)
# ./runtest.py -b build_data.json -a tag -f test.manifest

import sys
import os
import ConfigParser
from optparse import OptionParser

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def run(name, run, notrun):
    api_path = '/root/tempest-13.0.0/tempest/api/'

    run_string = ''
    notrun_string = ''
    if run == 'all':
        run_string = '%s%s' % (api_path, name)
    else:
        for item in run.split('\n'):
            run_string = run_string + api_path + name + '/' + item + ' '

    if notrun == 'none':
        print('run all cases in %s' % (api_path + name))
    else:
        for item in notrun.split('\n'):
            notrun_string = notrun_string + ' -e ' + item
    log_output_string = '--with-xunit --xunit-file=%s.xml --xunit-testsuite-name=%s' % (name, name)
    cmd = 'nosetests %s -v %s %s' % (log_output_string, run_string, notrun_string)
    #print(cmd)
    os.system(cmd)

def main():
    # Get options
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--test-manifest", dest="tests_list",
            help="The test list file")

    (options, args) = parser.parse_args()

    cp = ConfigParser.SafeConfigParser()
    # cp is recipe.ini parser
    if options.tests_list:
        config_path=os.path.join(BASEDIR, options.tests_list)
        cp.read(config_path)
    else:
        print('you must input recipe file')

    for module in cp.sections():
        run_list = cp.get(module, 'run')
        notrun_list = cp.get(module, 'not_run')
        # run module test, and put result into one xml file
        run(module, run_list, notrun_list)

    return 0

if __name__ == "__main__":
    try:
        ret = main()
    except Exception:
        ret = 1
        import traceback
        traceback.print_exc(5)
    sys.exit(ret)
