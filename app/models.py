from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Dateregistration = db.Column(db.DateTime)
    Sex = db.Column(db.String(64))
    Birth_Date = db.Column(db.DateTime)
    Ava = db.Column(db.LargeBinary)
    Country = db.Column(db.String(120))
    IdGroup = db.Column(db.Integer, db.ForeignKey('group.id'), default=0)
    group = db.relationship('Group', backref=db.backref('User', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):
        return '<Group {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    Picture = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Game {}>'.format(self.name)


class Mod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    Picture = db.Column(db.LargeBinary)
    Description = db.Column(db.String)
    DescriptionCard = db.Column(db.String)
    Language = db.Column(db.String)
    DateCreation = db.Column(db.Date)
    GameId = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('Mod', lazy='dynamic'))
    AuthorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('Mods', lazy='dynamic'))
    GameTagId = db.Column(db.Integer, db.ForeignKey('game_tags.id'))
    gametag = db.relationship('GameTags', backref=db.backref('Mod', lazy='dynamic'))

    def __repr__(self):
        return '<Mod {}>'.format(self.name)


class ModLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.String)
    LinkName = db.Column(db.String)
    Modid = db.Column(db.Integer, db.ForeignKey('mod.id'), default=0)
    modid = db.relationship('Mod', backref=db.backref('ModLink', lazy='dynamic'))

    def __repr__(self):
        return '<ModLink {}>'.format(self.name)


class ModPicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Picture = db.Column(db.LargeBinary)
    Modid = db.Column(db.Integer, db.ForeignKey('mod.id'), default=0)
    mod = db.relationship('Mod', backref=db.backref('ModPicture', lazy='dynamic'))

    def __repr__(self):
        return '<ModPicture {}>'.format(self.name)


class ModVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.String)
    Modid = db.Column(db.Integer, db.ForeignKey('mod.id'), default=0)
    mod = db.relationship('Mod', backref=db.backref('ModVideo', lazy='dynamic'))

    def __repr__(self):
        return '<ModVideo {}>'.format(self.name)

class ModViews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Modid = db.Column(db.Integer, db.ForeignKey('mod.id'), default=0)
    mod = db.relationship('Mod', backref=db.backref('Mod', lazy='dynamic'))
    AuthorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('User', lazy='dynamic'))
    def __repr__(self):
        return '<ModVievs {}>'.format(self.name)

class ModComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Message = db.Column(db.String)
    Modid = db.Column(db.Integer, db.ForeignKey('mod.id'), default=0)
    mod = db.relationship('Mod', backref=db.backref('ModComment', lazy='dynamic'))
    MessageAuthorId = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    DateSend = db.Column(db.DateTime)
    messageauthor = db.relationship('User', backref=db.backref('ModComment.', lazy='dynamic'))

    def __repr__(self):
        return '<ModComment {}>'.format(self.name)


class GameTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    idGame = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('GameTags', lazy='dynamic'))

    def __repr__(self):
        return '<GameTags {}>'.format(self.Name)
