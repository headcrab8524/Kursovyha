from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import *
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
    username = StringField('Логин/Nickname*', validators=[DataRequired()])
    password = PasswordField('Пароль/Password*', validators=[DataRequired()])
    password2 = PasswordField('Пароль (подтверждение)/Password (again)*',
                              validators=[DataRequired(), EqualTo('password')])
    email = StringField('Электронная почта/E-mail address*', validators=[DataRequired(), Email()])
    birthdate = DateField('Дата рождения/Date of birth', validators=[DataRequired()])
    sex = SelectField('Ваш пол/ Your gender', choices=['Мужской', 'Женский'], validators=[DataRequired()])
    country = StringField('Страна/Country', validators=[DataRequired()])
    avatar = FileField('Аватар/Avatar')
    policy = BooleanField('Согласен с политикой конфиденциальности/Agree with privacy policy*',
                          validators=[DataRequired()])
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
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired('Пожалуйста, введите имя пользователя.')]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired('Пожалуйста, введите пароль.')]
    )
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class MakeGameForm(FlaskForm):
    gamename = StringField('Название', validators=[DataRequired()])
    picture = FileField('Обложка', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class MakeNewModForm(FlaskForm):
    gamename = SelectField('Выберите игру:*', choices=[], validators=[DataRequired()])
    materialname = StringField('Введите название материала:*', validators=[DataRequired()])
    materialtext = CKEditorField('Введите описание вашего материала:*', validators=[DataRequired()])
    image = FileField('Изображение (максимальный размер 300 Кб)')
    language = SelectField('Язык локализации мода:*',
                           choices=['Мультиязычный', 'Русский', 'Английский', 'Испанский', 'Итальянский', 'Немецкий',
                                    'Французский', 'Японский', 'Китайский', 'Иврит'], validators=[DataRequired()])
    mainlink = StringField('Основной архив мода №1 (ссылка):', validators=[DataRequired()])
    maintext = StringField('Краткое описание основного архива №1 (текст):', validators=[DataRequired()])
    sublink = StringField('Дополнительный архив мода:')
    subtext = StringField('Краткое описание доп. архива:')
    tubelink = StringField('Ссылка видео с YouTube:')
    tags = SelectField('Выберите тег вашей модификации:*', choices=[], validators=[DataRequired()])
    adddate = DateField('Дата добавления:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(MakeNewModForm, self).__init__(*args, **kwargs)
        self.gamename.choices.extend([(tt.id, tt.name) for tt in Game.query.all()])
        self.tags.choices.extend([(tt.id, tt.Name) for tt in GameTags.query.all()])
