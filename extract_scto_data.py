#!/usr/bin/env python3

import requests


def pull_data(url, username, password, keyfile=None):

    # This function will extract records or media files from the SurveyCTO Rest API depending on the url provided
    # Include the keyfile parameter if your form or media file needs to be decrypted

    try:

        if keyfile == None:
            response = requests.get(
                url, auth=requests.auth.HTTPDigestAuth(username, password))
        else:
            files = {'private_key': open(keyfile, 'rb')}
            response = requests.post(
                url, files=files, auth=requests.auth.HTTPDigestAuth(username, password))

    except Exception as e:

        response = False
        print(e)

    return response


def save_media_file(file_bytes, file_name):

    f = open(file_name, 'wb')
    f.write(file_bytes)
    f.close()


def construct_url(form_id, servername):

    url = f'https://{servername}.surveycto.com/api/v2/forms/data/wide/json/{form_id}?date=0'

    return url


if __name__ == '__main__':

    # We'll demonstrate pulling data from an encrypted form and an unencrypted form
    # To pull data from an encrypted form we'll need the .pem file -- you should have downloaded this from the SurveyCTO web console when adding encryption to your form

    # Here we'll provide details for our encrypted and unencrypted forms. These will be used to construct the requests we send to the SurveyCTO API.
    form_config = [
        {
            'form_id': 'encrypted_test_form',
            'servername': 'mysctoservername',
            'username': 'mysctousername',
            'password': 'mysctopassword',
            'keyfile': 'path/to/encryption/keyfile.pem'
        },
        {
            'form_id': 'unencrypted_test_form',
            'servername': 'mysctoservername',
            'username': 'mysctousername',
            'password': 'mysctopassword',
        },
    ]

    #######################
    # Let's pull form records for the encrypted form

    form = form_config[0]
    url = construct_url(form['form_id'], form['servername'])

    # With the encryption key, we expect to see all the fields included in the response. If we don't include the encryption key the API will only return the unencrypted fields.
    response = pull_data(url, form['username'], form['password'], form['keyfile'])
    print(response.json())

    # If the form contains media files we can download them using one of the url's returned in the form records
    url = 'url_to_media_file'
    response = pull_data(url, form['username'], form['password'], form['keyfile'])

    file_name = 'myfilename.png' # Choose a filename for saving the media file
    save_media_file(response.content, file_name) # response.content contains the file bytes which we can save to disk or upload to a 3rd party service like S3


    #######################
    # Pulling data for the unencrypted form will be the exact same except we don't provide a keyfile for the pull_data function

    form = form_config[1]
    url = construct_url(form['form_id'], form['servername'])

    response = pull_data(url, form['username'], form['password'])
    print(response.json())

    # If the form contains media files we can download them using one of the url's returned in the form records
    url = 'url_to_media_file'
    response = pull_data(url, form['username'], form['password'])

    file_name = 'myfilename.png' # Choose a filename for saving the media file
    save_media_file(response.content, file_name) # response.content contains the file bytes which we can save to disk or upload to a 3rd party service like S3
