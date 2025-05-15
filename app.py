from flask import Flask, render_template, request, redirect, flash, url_for
from printers import get_connected_printers, print_file
import os

app = Flask(__name__)
app.secret_key = 'printer_secret'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    printers = get_connected_printers()
    message = None

    if request.method == 'POST':
        selected_printer = request.form.get('printer')
        file = request.files.get('file')

        if not selected_printer or not file:
            flash('Please select a printer and upload a file.')
            return redirect(url_for('index'))

        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)

        success, result_message = print_file(selected_printer, file_path)
        flash(result_message)
        os.remove(file_path)

    return render_template('index.html', printers=printers)
