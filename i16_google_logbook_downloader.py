"""
I16 Google Drive Logbook Downloader
Downloads the Google Docs logbook to pdf in the scripts folder

Requires:
 - Google API credentials "i16_user_google_creds.json"
 - an experiment_parameter json file, generated from experiment_parameters.py

Usage:
$ python i16_google_logbook_downloader.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json

By Dan Porter
Beamline I16
Diamond Light Source Lid

14-Feb-2022
"""

import sys

from i16_google_logbook_maker import download_logbook


if __name__ == '__main__':
    # --- Command line usage ---
    filearg = sys.argv[-1]
    if filearg.endswith('.json'):
        download_logbook(filearg)
    else:
        print('You must enter an experimental parameter file, for example:')
        print(' python i16_google_logbook_downloader.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json')

