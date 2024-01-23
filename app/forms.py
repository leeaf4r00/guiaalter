from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    # Campo de nome de usuário com validações de presença e comprimento
    username = StringField('Username', validators=[
        DataRequired(message="Este campo é obrigatório"),
        Length(min=6, max=20,
               message="O nome de usuário deve ter entre 6 e 20 caracteres")
    ])

    # Campo de e-mail com validações de presença e formato de e-mail
    email = StringField('Email', validators=[
        DataRequired(message="Este campo é obrigatório"),
        Email(message="Por favor, forneça um endereço de e-mail válido")
    ])

    # Campo de senha com validações de presença e comprimento mínimo
    password = PasswordField('Password', validators=[
        DataRequired(message="Este campo é obrigatório"),
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres")
        # Você pode adicionar validações adicionais aqui para verificar a complexidade da senha
    ])

    # Campo de confirmação de senha para verificar se as senhas correspondem
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Este campo é obrigatório"),
        EqualTo('password', message="As senhas devem corresponder")
    ])

    # Botão de envio
    submit = SubmitField('Cadastrar')
