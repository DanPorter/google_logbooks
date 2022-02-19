"""
I16 Google Drive Logbook scripts
Functions to create, modify, download Google Docs Logbooks

Requires:
 - Google API credentials "i16_user_google_creds.json"
 - an experiment_parameter json file, generated from experiment_parameters.py

By Dan Porter
Beamline I16
Diamond Light Source Lid

14-Feb-2022
"""
import json
import os

from google_drive_api import GoogleDriveApi

# Edit these:
CREDS_JSON = 'i16_user_google_creds.json'  # Credentials file
TEMPLATE = '1fF1CU3UJq_qlqn43D9AWLovTr1sLK8HuOK9AIWk_HRI'  # GoogleAPI_ExampleLogbook
LOGBOOK_LIST = '1VumxVxyzXFuLOMsIIPvUYUEhgIOQo_aiKFhVSYucO0Y'  # I16 Logbook List

# Sign-in to GoogleDriveAPI
gdrive = GoogleDriveApi(CREDS_JSON)


def read_exppars(filename='mm12345-1.json'):
    """Read json file with experiment parameters"""
    with open(filename, 'r') as f:
        exppars = json.load(f)
    return exppars


def write_exppars(exppars):
    """Write experimental parameters to json file"""
    filename = exppars['experiment_parameters']
    with open(filename, 'wt') as f:
        json.dump(exppars, f, indent=2)
    print('Saved experiment parameter file to: %s' % filename)


def create_new_logbook(exp_pars_file='mm12345-1.json'):
    """
    Use Google Drive API to:
        - Create new Google Docs logbook from template
        - Change permissions and create sharable link
        - update experimental parameters json file with sharable link
        - Merge experimental parameters from json file with template
        - Update Logbook list file with new file and link
    :param exp_pars_file: str filepath of experimental parameters json file
    :return: None
    """
    # Read merge fields JSON
    exppars = read_exppars(exp_pars_file)

    if gdrive.is_file(exppars['logbook_name']):
        print('Logbook already exists!')
        return

    # --- New Logbook ---
    logbook = gdrive.copy_file(TEMPLATE, exppars['logbook_name'])

    # Change permission of copied file
    logbook.change_permission()
    exppars['logbook_id'] = logbook.id
    exppars['logbook_link'] = logbook.link
    exppars['replace_fields']['{{logbook_link}}'] = logbook.link
    print('\nThe sharable link is:\n%s\n' % logbook.link)

    # Update json file
    write_exppars(exppars)

    # Merge new logbook with replacement fields
    logbook.merge(exppars['replace_fields'])

    # --- Update Experiment list Doc ---
    newtxt = '%s %s\n{{new_logbook}}' % (exppars['logbook_name'], logbook.link)
    gdrive.merge_template(LOGBOOK_LIST, {'{{next_experiment}}': newtxt})
    print("finished!")


def download_logbook(exp_pars_file='mm12345-1.json'):
    """
    Use Google Drive API to:
        - download pdf of GoogleDoc logbook
    :param exp_pars_file: str filepath of experimental parameters json file
    :return: None
    """
    # Read merge fields JSON
    exppars = read_exppars(exp_pars_file)

    if not exppars['logbook_id']:
        print("Logbook doesn't exists!")
        return

    output_pdf = os.path.join(exppars['scriptdir'], exppars['logbook_name'] + '.pdf')
    gdrive.download_pdf(exppars['logbook_id'], output_pdf)


def append_text(exp_pars_file='mm12345-1.json', text_to_append=''):
    """
    Use Google Drive API to:
        - download pdf of GoogleDoc logbook
    :param exp_pars_file: str filepath of experimental parameters json file
    :param text_to_append: str text to append to file
    :return: None
    """
    # Read merge fields JSON
    exppars = read_exppars(exp_pars_file)

    if not exppars['logbook_id']:
        print("Logbook doesn't exists!")
        return

    gdrive.append_text(exppars['logbook_id'], text_to_append)


def append_image(exp_pars_file='mm12345-1.json', image_loc=''):
    """
    Use Google Drive API to:
        - download pdf of GoogleDoc logbook
    :param exp_pars_file: str filepath of experimental parameters json file
    :param image_loc: str filename of image to append
    :return: None
    """
    # Read merge fields JSON
    exppars = read_exppars(exp_pars_file)

    if not exppars['logbook_id']:
        print("Logbook doesn't exists!")
        return

    gdrive.append_image(exppars['logbook_id'], image_loc)