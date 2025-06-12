from flask import Blueprint, render_template

intro_bp = Blueprint('intro', __name__, url_prefix='/intro')

@intro_bp.route('/')
def show_intro():
    return render_template('intro.html')
