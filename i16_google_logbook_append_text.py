"""
I16 Google Drive Logbook
Append text to logbook

Requires:
 - Google API credentials "i16_user_google_creds.json"
 - an experiment_parameter json file, generated from experiment_parameters.py
 - a string of text to append

Usage:
$ python i16_google_logbook_append_text.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json 'text to append'

By Dan Porter
Beamline I16
Diamond Light Source Lid

14-Feb-2022
"""

import sys

from i16_google_logbook_scripts import append_text

if __name__ == '__main__':
    # --- Command line usage ---
    filearg = sys.argv[-2]
    text_to_append = sys.argv[-1]
    if filearg.endswith('.json'):
        append_text(filearg, text_to_append)
    else:
        print('You must enter an experimental parameter file, for example:')
        print(' python i16_google_logbook_append_text.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json \'text to append\'')

