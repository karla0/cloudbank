from flask import ( Blueprint, flash, g, redirect, 
                    render_template, request, url_for
)
from werkzeug.exceptions import abort

from cloud_folder.auth import login_required
from cloud_folder.db import get_db
from cloud_folder.aws_functions import get_uploaded_file

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

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        cloudname = request.form['cloudname']
        author_id = g.user['id']
        description = request.form['description']
        s3_location = get_uploaded_file(request)
        error = None

        if not cloudname:
            error = 'Cloud name is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO cloud (cloudname, description, author_id, s3_url)'
                ' VALUES (?, ?, ?, ?)',
                (cloudname, description ,author_id, s3_location)
            )

            db.commit()
            return redirect(url_for('bank.view_user_clouds'))

    return render_template('bank/create.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM cloud WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('bank.view_user_clouds'))

@login_required
def get_clouds():
    user_id = g.user['id']
    db = get_db()
    
    clouds = db.execute(
        """
        SELECT cloud.id, cloudname, created
        FROM cloud
        INNER JOIN user on user.id = cloud.author_id
        WHERE user.id = ?
        ORDER by created ASC
        """, (user_id,)
        ).fetchall()
    return clouds

def get_cloud(id):
    db = get_db()
    
    cloud = db.execute(
        'SELECT id, cloudname, description, author_id'
        ' FROM cloud'
        ' WHERE id = ?', 
        (id,)
    ).fetchone()

    if cloud is None:
        abort(404, f'Cloud ID: {id} not found.')

    if cloud['author_id'] != g.user['id']:
        abort(403)

    return cloud

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    cloud = get_cloud(id)

    if request.method == 'POST':
        cloudname = request.form['cloudname']
        description = request.form['description']
        error = None

        if not cloudname:
            error = 'Cloudname is required.'
        if not description:
            error = 'Description is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE cloud SET cloudname = ?, description = ?'
                ' WHERE id = ?',
                (cloudname, description, id)
            )
            db.commit()
            return redirect(url_for('bank.view_user_clouds'))
    return render_template('bank/update.html', cloud=cloud)

@bp.route('/view', methods=('GET',))
@login_required
def view_user_clouds():
    clouds = get_clouds()
    return render_template('bank/cloud_view.html', clouds=clouds)
    