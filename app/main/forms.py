# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp, DataRequired
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField(u'您的姓名', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    name = StringField(u'真实姓名', validators=[Length(0, 64)], render_kw={"placeholder": "your realname",
                        "style": "background: url(/static/username.png)no-repeat 15px center; text-indent: 28px; height:35px; width:280px; border-width:1px"})
    location = StringField(u'地理位置', validators=[Length(0, 64)], render_kw={"placeholder": "your location",
                        "style": "background: url(/static/location.png)no-repeat 15px center; text-indent: 28px; height:35px; width:280px; border-width:1px"})
    about_me = TextAreaField(u'自述', render_kw={"placeholder": "Please give some describe of yourself...",
                        "style": "text-indent: 20px; height:100px; width:400px; border-width:1px"})
    submit = SubmitField(u'确定提交', render_kw={"style": "width:100px; height:40px; background-color:#126fda; font-weight:bold;"})


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能包括字母数字小数点或下划线')])
    confirmed = BooleanField(u'确认')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'自述')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已注册')


class PostForm(Form):
    title = StringField(u'文章标题', validators=[DataRequired(message='请输入文字...'),
                                             Length(0, 40, message='文章标题请限制40字以内')],
                render_kw={'style': 'width:40%; border-width:1px; border-color:#126fda;'})
    category = SelectField('文章分类：', 
        choices=[('Python', 'Python'), ('Flask', 'Flask'), ('Django','Django'), 
                 ('算法导论', '算法导论'), ('数据库', '数据库'),
                 ('Hadoop', 'Hadoop'), ('Spark', 'Spark'),
                 ('随笔', '随笔')], coerce=str, 
                 render_kw={'style': 'width:20%; border-width:1px; border-color:#126fda; \
                 background: url("http://ourjs.github.io/static/2015/arrow.png") no-repeat scroll right center transparent;\
                  padding-right: 14px; appearance:none; -moz-appearance:none; -webkit-appearance:none;'})
    body = PageDownField(u"记录您的点滴...", validators=[DataRequired(message='请输入文字...')],
        render_kw={'style': 'border-color:#126fda; border-width:1px; height:200px;'})
    submit = SubmitField(u'发表博客', render_kw={"style": "width:100px; height:40px; background-color:#126fda; font-weight:bold;"})
    

class EditPostForm(Form):
    body = PageDownField("记录你的点滴...", validators=[DataRequired()])
    submit = SubmitField('confirm change')


class CommentForm(Form):
    body = StringField(u'写下您的评论', validators=[Required()],
        render_kw={'style': 'border-width:1px; border-color:#126fda; height:200px; width:872px;'})
    submit = SubmitField(u'提交', render_kw={"style": "width:80px; height:40px; background-color:#126fda; font-weight:bold;"})


class SearchForm(Form):
    search = StringField('search', validators = [Required()])
    #submit = SubmitField(u'搜索')