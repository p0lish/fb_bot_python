""" Ez webview """

from flask import Blueprint, render_template

WEB = Blueprint('web', __name__, template_folder='./templates')

@WEB.route('/places')
def places_page():
	return render_template('places.html')