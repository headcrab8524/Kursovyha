from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import *
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
    username = StringField('Логин/Nickname*', validators=[DataRequired('Обязательное поле')])
    password = PasswordField('Пароль/Password*', validators=[DataRequired('Обязательное поле')])
    password2 = PasswordField('Пароль (подтверждение)/Password (again)*',
                              validators=[DataRequired('Обязательное поле'), EqualTo('password', 'Пароли должны совпадать')])
    email = StringField('Электронная почта/E-mail address*', validators=[DataRequired('Обязательное поле'), Email('Неправильный email')])
    birthdate = DateField('Дата рождения/Date of birth', validators=[DataRequired('Обязательное поле')])
    sex = SelectField('Ваш пол/ Your gender', choices=['Мужской', 'Женский'], validators=[DataRequired('Обязательное поле')])
    country = StringField('Страна/Country', validators=[DataRequired('Обязательное поле')])
    avatar = FileField('Аватар/Avatar')
    policy = BooleanField('Согласен с политикой конфиденциальности/Agree with privacy policy*',
                          validators=[DataRequired('Обязательное поле')])
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
    gamename = SelectField('Выберите игру:*', choices=[], validators=[DataRequired('Обязательное поле')])
    materialname = StringField('Введите название материала:*', validators=[DataRequired('Обязательное поле')])
    desctex = TextAreaField('Введите описание карточки вашей модификации:*', validators=[DataRequired('Обязательное поле')])
    materialtext = CKEditorField('Введите описание вашего материала:*', validators=[DataRequired('Обязательное поле')])

    image = FileField('Изображение (максимальный размер 300 Кб)')
    language = SelectField('Язык локализации мода:*',
                           choices=['Мультиязычный', 'Русский', 'Английский', 'Испанский', 'Итальянский', 'Немецкий',
                                    'Французский', 'Японский', 'Китайский', 'Иврит'], validators=[DataRequired('Обязательное поле')])
    mainlink = StringField('Основной архив мода №1 (ссылка):*', validators=[DataRequired('Обязательное поле')])
    maintext = StringField('Краткое описание основного архива №1 (текст):*', validators=[DataRequired('Обязательное поле')])
    sublink = StringField('Дополнительный архив мода:')
    subtext = StringField('Краткое описание доп. архива:')
    tubelink = StringField('Ссылка видео с YouTube:')
    tags = SelectField('Выберите тег вашей модификации:*', choices=[], validators=[DataRequired('Обязательное поле')])
    adddate = DateField('Дата добавления:', validators=[DataRequired('Обязательное поле')])
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(MakeNewModForm, self).__init__(*args, **kwargs)
        self.gamename.choices.extend([(tt.id, tt.name) for tt in Game.query.all()])
        self.tags.choices.extend([(tt.id, tt.Name) for tt in GameTags.query.all()])

class CommentForm(FlaskForm):
    user_id = HiddenField('user id')
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Опубликовать')