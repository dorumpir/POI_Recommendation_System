from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, SearchbarForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import admin_required

from draw_graph import draw_all_distribution
from methods import run, train 
from input_data import read_n_parse
from methods import evaluate as ev

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchbarForm()
    if form.validate_on_submit():
        return redirect(url_for('.search', 
                                user_id=form.user_id.data,
                                category=form.category.data))
    return render_template('index.html', user_id="", category=-1, form=form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchbarForm()
    form.user_id.data = user_id = request.args.get('user_id', 0, type=int)
    form.category.data = category = request.args.get('category', -2, type=int)
    page = request.args.get('page', 1, type=int)
    '''
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    '''
    from ..Pagination import Pagination
    datas = run(user_id=user_id)
    pagination = Pagination(datas['result'])
    pagination.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'])
    posts = pagination.items

    return render_template('search_result.html', user_id=user_id, category=category, 
                            posts=posts, pagination=pagination, form=form, pois=datas['pois'])


@main.route('/dataset-description', methods=['GET'])
def dataset_description():
    content = []
    path = 'C:\\Users\\lmq\Desktop\\biyesheji\\dataset_tsmc2014\\dataset_TSMC2014_readme.txt'
    with open(path, 'r') as f:
        l = f.readline()
        while l:
            content.append(l)
            l = f.readline()
    return render_template('dataset_description.html', content=content)


#################################
@main.route('/dataset-analysis', methods=['GET'])
def dataset_analysis():
    #ufpath, pfpath = draw_all_distribution()
    ufpath = "file:///C:/Users/lmq/Desktop/biyesheji/lbsn/flasky/lbsn/graphs/users_distribution.png"
    pfpath = "file:///C:/Users/lmq/Desktop/biyesheji/lbsn/flasky/lbsn/graphs/pois_distribution.png"
    return render_template('dataset_analysis.html', ufpath=ufpath, pfpath=pfpath)


@main.route('/user-analysis', methods=['GET', 'POST'])
def user_analysis():
    return render_template('user_analysis.html')


@main.route('/poi-analysis', methods=['GET', 'POST'])
def poi_analysis():
    return render_template('poi_analysis.html')


@main.route('/evaluate')
def evaluate():
    datas = read_n_parse()
    datas = ev(datas)
    flash('Evaluate over.')
    return render_template('evaluate.html', prf=datas['evaluation'])


@main.route('/reinput')
def reinput():
    datas = run()
    flash('Read new dataset over.')
    return redirect(url_for('.index'))


@main.route('/retrain')
def retrain():
    datas = read_n_parse()
    datas = train(datas)
    flash('Train new model over. alpha = %f'%datas['alpha'])
    return redirect(url_for('.index'))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/poi/<poi_id>')
def poi(poi_id):
    pass


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
