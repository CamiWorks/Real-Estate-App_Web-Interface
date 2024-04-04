from flask import Flask, render_template, url_for, request, redirect
from data_processing import Report 
import os 


app = Flask(__name__)

js_template = '''
  
  google.charts.setOnLoadCallback(###FUN###);
  function ###FUN###() {
    var data = google.visualization.arrayToDataTable([
      ['Definition', 'Value'],
      ###DATA###
    ]);

    var options = {
      title: '###TITLE###',
      pieHole: 0.4,
      slices: {
        0: { color: '#E7B34D' },
        1: { color: '#4D98E7' },
        2: { color: '#F0C96B' },
        3: { color: '#E79A4D' },
        4: { color: '#E7D64D' },
        5: { color: '#4DE7A1' },
        6: { color: '#4D61E7' },
        7: { color: '#D6A542' },
        8: { color: '#F0C96B' },
        9: { color: '#B34DE7' },
        10: { color: '#E74D4D' },
        11: { color: '#4D98E7' },
        12: { color: '#F0C96B' },
        13: { color: '#E79A4D' },
        14: { color: '#E7D64D' },
        15: { color: '#4DE7A1' },
        16: { color: '#4D61E7' },
        17: { color: '#D6A542' },
        18: { color: '#F0C96B' },
        19: { color: '#B34DE7' },
        20: { color: '#E74D4D' },
      }
    };
    var chart = new google.visualization.PieChart(document.getElementById('###ID###'));
    chart.draw(data, options);
  }

'''
provinces = [
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan"
]
def delete_file(filename):
    # Construct the full path of the file
    file_path = os.path.join(os.getcwd(), filename)

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
    else:
        ...
def creating_js(data, template):
    template_base = template
    price = '{:,}'.format(round(data[0], 2))
    score = round(data[1], 1)
    final_script = ''
    ids = []
    demographics = data[2]
    for header in demographics:
        template = template.replace('###TITLE###', header)
        tem_header = header.replace(' ', '').strip().lower()
        ids.append(tem_header)
        template = template.replace('###ID###', tem_header)
        template = template.replace('###FUN###', tem_header)
        data_script = ''
        for data_pair in demographics[header]:
            for data in data_pair:
                data_script += f'["{data}", {data_pair[data]}],'
        template = template.replace('###DATA###', data_script)
        final_script += template
        template = template_base

    return [final_script, price, score, ids]


@app.route("/")
def index():
    return render_template('realg.html', homestart=True)

@app.route("/sandbox")
def sandbox():
    return render_template("instruct.html")

@app.route("/terms-of-use")
def termsofuse():
    return render_template('termsofuse.html')

@app.route("/sandbox-report")
def report_creation():
    return render_template('sandbox.html', provinces=provinces)

@app.route('/error-processing')
def error_process():
    return render_template('processing_error.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
          api = request.form['api_key']
          address = request.form['address']
          city = request.form['city']
          province = request.form['province']
          address = f'{address.strip()}, {city.strip()}, {province.strip()}, Canada'
          my_report = Report(str(address), str(api))
          imported_data = my_report.data_return()
          js_scrip, price, score, html  = creating_js(imported_data, js_template)
          return render_template('report.html', address=address, data=[price,score], html=html, graphs=js_scrip)
        except:
          return redirect('error-processing')
    else:
        return redirect('index')

# @app.route("/test")
# def test():
#     return render_template('report.html', address='Montreal', data=['123234', '1234'], html='hello', graphs='none')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=2025)