from flask import Flask, render_template, jsonify, send_file, request
from random import *
from flask_cors import CORS
import requests
import sys
import zipfile
from glob import glob
import os
from os.path import exists
import pandas as pd
import simplejson as json

applicant_df = None
applicant_order = None
order_file = None
app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/random')
def random_number():
    assert(applicant_df is not None)
    assert(order_file is not None)

    if (exists(order_file.replace('xlsx', 'csv'))):
        applicant_order = pd.read_csv(order_file.replace('xlsx', 'csv'),
        index_col=0)
    else:
        applicant_order = pd.read_excel(order_file)

    applicant_order.fillna(0, inplace=True)
    print(applicant_order.head())

    response = {
        'randomNumber': randint(1, 100),
        'order': applicant_order.to_dict(orient='record'),
    }
    return jsonify(response)

@app.route('/api/pdf/<username>')
def get_pdf(username):
    pdf_path = applicant_df.loc[username, 0]
    return send_file(pdf_path)

@app.route('/api/save', methods=['POST'])
def save_scores():
    data = json.loads(request.data)  # data is empty
    if (order_file is not None):
        applicant_order = pd.DataFrame(data)
        print(applicant_order.head())
        applicant_order.to_csv(order_file.replace('xlsx', 'csv'))
        return jsonify({'success': 1})
    return jsonify({'success': 0})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        order_file = sys.argv[1]
        zip_file = sys.argv[2]
        # make sure the files are right
        assert(order_file.endswith('.xlsx'))
        assert(zip_file.endswith('.zip'))

        # extract the zip file w/ all the pdfs
        zip_ref = zipfile.ZipFile(zip_file, 'r')
        zip_ref.extractall('/tmp/applicants')
        zip_ref.close()

        # get all the relevant files and names
        all_applicants_path = sorted(glob('/tmp/applicants/*/*'))
        all_applicants_names = [a.split('/')[-1] for a in all_applicants_path]
        applicant_pdfs = [os.path.join(all_applicants_path[i], '{}.pdf'.format(a)) for i, a in enumerate(all_applicants_names)]
        #_ = [assert(exists(a)) for a in applicant_pdfs]
        applicant_df = pd.DataFrame(index=all_applicants_names,
                                    data=applicant_pdfs)
        if (exists(order_file.replace('xlsx', 'csv'))):
            applicant_order = pd.read_csv(order_file.replace('xlsx', 'csv'),
            index_col=0)
        else:
            applicant_order = pd.read_excel(order_file)

        applicant_order.fillna(0, inplace=True)

        app.run('0.0.0.0', '5000')
    else:
        raise Exception('python run.py order.xlsx zipFile.zip')
