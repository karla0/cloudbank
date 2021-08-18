from flask import ( Blueprint, flash, g, redirect, 
                    render_template, request, url_for
)

from werkzeug.exceptions import abort

from cloud_folder.auth import login_required
from cloud_folder.db import get_db

bp = Blueprint('bank', __name__)

@bp.route('/')
def index():
    db = get_db()
    clouds = db.execute(
        'SELECT c.id, cloudname, created, author_id, email'
        ' FROM cloud c JOIN user u ON c.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('bank/index.html', clouds=clouds)