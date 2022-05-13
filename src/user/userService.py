from src.user.userModel import User, db


def getUserByUsername(payload):
    user = User.query.filter_by(username=payload).first()
    return user


def getUserByUserId(payload):
    user = User.query.filter_by(user_id=payload).first()
    return user


def getUserByEmail(payload):
    user = User.query.filter_by(email=payload).first()
    return user


def addUser(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
