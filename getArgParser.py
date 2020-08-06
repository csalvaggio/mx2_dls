import argparse
import sys

# returns argparser or prints help if no args
def getArgParser():

    description = 'Capture spectrum from Ocean Optics Flame Spectrometer'

    parser = argparse.ArgumentParser(description=description)
    helpMessage='desired integration time for spectrum scan in'+\
                 ' MicroSeconds [if not given auto exposure is used] '+\
                 ' [will not be synced to gps if int time given]'
    parser.add_argument('-t','--intTime',
                        dest = 'intTime',
                        type = float,
                        default = -1,
                        help=helpMessage)
    helpMessage = 'number of scans desired default = [1]'
    parser.add_argument('-N','--numberOfScans',
                        dest = 'numberOfScans',
                        type = int,
                        default = 1,
                        help=helpMessage)
    helpMessage = 'option to apply the dark correction. '+\
                  'if true, option applied'
    helpMessage += 'default is [True]'
    parser.add_argument('-D','--correct_dark_counts',
                        dest = 'correct_dark_counts',
                        default = 'True',
                        help=helpMessage)
    helpMessage = 'option to apply non linearity correction.'+\
                  ' if true option applied'
    helpMessage += 'default option is [False]'
    parser.add_argument('-l','--correct_nonlinearity',
                        dest = 'correct_nonlinearity',
                        default = False,
                        help=helpMessage)
    helpMessage = 'option to save spectrum into text file. '+\
        'If true option applied'
    helpMessage += 'Default option is True'
    parser.add_argument('-s','--saveScan',
                         dest = 'saveScan',
                        default = True,
                         help=helpMessage)
    helpMessage = 'number of scans to take and average'
    parser.add_argument('-n','--scansToAverage',
                        dest = 'scansToAverage',
                        type = int,
                        default = 1,
                        help=helpMessage)
    helpMessage = 'prefix to add to file name before the '+\
                  'default time stamp'
    parser.add_argument('-p','--prefix',
                        dest = 'prefix',
                        type = str,
                        default="test",
                        help=helpMessage)
    helpMessage = 'boolean to determine if dark current is read '
    parser.add_argument('-d','--dark',
                        dest = 'dark',
                        default=True,
                        help=helpMessage)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    return parser
