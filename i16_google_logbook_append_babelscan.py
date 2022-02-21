"""
I16 Google Drive Logbook
Loads a scan using Babelscan, saves the image and pushes it to the Google Logbook

Requires:
 - Google API credentials "i16_user_google_creds.json"
 - an experiment_parameter json file, generated from experiment_parameters.py
 - a nexus data file

Usage:
$ python i16_google_logbook_append_babelscan.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json '12345.nxs' fit

By Dan Porter
Beamline I16
Diamond Light Source Lid

14-Feb-2022
"""

import sys
import os

pth = os.path.expanduser('~/OneDrive - Diamond Light Source Ltd/PythonProjects')
sys.path.insert(0, pth + '/babelscan')

from i16_google_logbook_scripts import append_image
import babelscan

CONFIG = '/dls_sw/i16/software/python/babelscan/config_files/i16.config'
IMAGE_LOC = 'scan_image.png'

if __name__ == '__main__':
    # --- Command line usage ---
    exppar_file = sys.argv[1]
    scan_file = sys.argv[2]
    if exppar_file.endswith('.json'):
        if CONFIG:
            i16 = babelscan.instrument_from_config(CONFIG)
            scan = i16.scan(scan_file)
        else:
            scan = babelscan.file_loader(scan_file)
        print(scan)
        if sys.argv[-1] == 'fit':
            print('Fitting default axes')
            scan.fit()
            print('Creating plot')
            fig = scan.plot.detail(yaxis=['signal', 'fit'])
        else:
            print('Creating plot')
            fig = scan.plot.scananddetector()
        fig.savefig(IMAGE_LOC)
        append_image(exppar_file, IMAGE_LOC)
    else:
        print('You must enter an experimental parameter file, for example:')
        print(' python i16_google_logbook_append_text.py /dls_sw/i16/scripts/2022/mm12345-1/mm12345-1.json \'file.nxs\'')

