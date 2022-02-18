"""
I16 Google Drive Logbook
Append image to logbook

Requires:
 - Google API credentials "i16_user_google_creds.json"
 - an experiment_parameter json file, generated from experiment_parameters.py
 - an image file

Usage:
$ python i16_google_logbook_append_image.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json 'file.png'

By Dan Porter
Beamline I16
Diamond Light Source Lid

14-Feb-2022
"""

import sys

from i16_google_logbook_maker import append_image


if __name__ == '__main__':
    # --- Command line usage ---
    filearg = sys.argv[-2]
    image_loc = sys.argv[-1]
    if filearg.endswith('.json'):
        append_image(filearg, image_loc)
    else:
        print('You must enter an experimental parameter file, for example:')
        print(' python i16_google_logbook_append_text.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json \'file.png\'')

