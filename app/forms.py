from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    username = StringField('Логин/Nickname*', validators=[DataRequired()])
    password = PasswordField('Пароль/Password*', validators=[DataRequired()])
    password2 = PasswordField('Пароль (подтверждение)/Password (again)*', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Электронная почта/E-mail address*', validators=[DataRequired(), Email()])
    birthdate = DateField('Дата рождения/Date of birth', validators=[DataRequired()])
    sex = SelectField('Ваш пол/ Your gender', choices=['Мужской', 'Женский'], validators=[DataRequired()])
    country = StringField('Страна/Country', validators=[DataRequired()])
    avatar = FileField('Аватар/Avatar')
    policy = BooleanField('Согласен с политикой конфиденциальности/Agree with privacy policy*', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Войти')


class MakeGameForm(FlaskForm):
    gamename = StringField('Название', validators=[DataRequired()])
    picture = FileField('Обложка', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class MakeNewModForm(FlaskForm):
    gamename = SelectField('Выберите игру:*', choices=['Игра1', 'Игра2'], validators=[DataRequired()])
    materialname = StringField('Введите название материала:*', validators=[DataRequired()])
    materialtext = CKEditorField('Введите описание вашего материала:*', validators=[DataRequired()])
    image = FileField('Изображение (максимальный размер 300 Кб)')
    language = SelectField('Язык локализации мода:*', choices=['Мультиязычный', 'Русский', 'Английский', 'Испанский', 'Итальянский', 'Немецкий', 'Французский', 'Японский', 'Китайский', 'Иврит'], validators=[DataRequired()])
    mainlink = StringField('Основной архив мода №1 (ссылка):', validators=[DataRequired()])
    maintext = StringField('Краткое описание основного архива №1 (текст):', validators=[DataRequired()])
    sublink = StringField('Дополнительный архив мода:', validators=[DataRequired()])
    subtext = StringField('Краткое описание доп. архива:', validators=[DataRequired()])
    tubelink = StringField('Ссылка видео с YouTube:', validators=[DataRequired()])
    tags = StringField('Теги (через запятую):', validators=[DataRequired()])
    adddate = DateField('Дата добавления:', validators=[DataRequired()])
    submit = SubmitField('Добавить')
