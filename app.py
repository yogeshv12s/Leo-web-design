from flask import Flask, request, render_template,redirect,url_for,flash
import pyodbc

app = Flask(__name__)

# SQL Server configuration
server = 'LAPTOP-GC5A9QHM'
database = 'yogesh2'
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

# Establishing connection
conn = pyodbc.connect('DRIVER=' + driver +
                      ';SERVER=' + server +
                      ';DATABASE=' + database +
                      ';Trusted_Connection=yes;')

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get data from form
    group = request.form['group']
    phase = request.form['phase']
    order_status = request.form['order_status']
    sample_type = request.form['sample_type']
    artwork = request.files['artwork']
    main_fabric = request.form['main_fabric']
    style_no = request.form['style_no']
    description = request.form['description']
    tech_pack = request.files['tech_pack']
    tech_pack_date = request.form['tech_pack_date']
    construction_details = request.form['construction_details']
    development_spec_link = request.form['development_spec_link']
    pd_meeting_date = request.form['pd_meeting_date']
    garment_risk_assessment = request.form['garment_risk_assessment']
    printing_risk_assessment = request.form['printing_risk_assessment']
    embroidery_risk_assessment = request.form['embroidery_risk_assessment']
    base_pattern = request.files['base_pattern']

    # Save uploaded files
    artwork_path = 'static/' + artwork.filename
    artwork.save(artwork_path)
    tech_pack_path = 'static/' + tech_pack.filename
    tech_pack.save(tech_pack_path)
    base_pattern_path = 'static/' + base_pattern.filename
    base_pattern.save(base_pattern_path)

    # Insert data into SQL table
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ProductDevelopment (Groups, Phase, OrderStatus, SampleType, Artwork, MainFabric, StyleNo, Description, TechPack, TechPackDate,
                                   ConstructionDetails, DevelopmentSpecLink, PDMeetingDate, GarmentRiskAssessment, PrintingRiskAssessment,
                                   EmbroideryRiskAssessment, BasePattern)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (group, phase, order_status, sample_type, artwork_path, main_fabric, style_no, description, tech_pack_path, tech_pack_date,
          construction_details, development_spec_link, pd_meeting_date, garment_risk_assessment, printing_risk_assessment,
          embroidery_risk_assessment, base_pattern_path))
    conn.commit()
    cursor.close()

    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
