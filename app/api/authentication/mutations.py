import graphene
import graphql_jwt
from django.conf import settings
from graphql_extensions.auth.decorators import login_required
from rolepermissions.roles import assign_role

from ..helpers.constants import (ADMIN_MAIL_BODY_MSG, AGENCY_MAIL_BODY_MSG,
                                 AGENCY_SIGNUP_SUCCESS, SIGNUP_SUCCESS,
                                 SUCCESS_ACTION, USER_MAIL_BODY_MSG,
                                 ACCOUNT_ACTIVATION_MSG)
from ..helpers.jwt_helper import generate_jwt
from ..helpers.permission_required import role_required, token_required
from ..helpers.validate_input import check_email_validity
from ..helpers.validation_errors import error_dict
from .helpers.email_helper import template_email
from .helpers.user_helpers import validate_user_email
from .models import User
from .object_types import (AdminType, PasswordResetInput, UserInput, UserType,
                           UserUpdateInput)
from .validators.validate_input import UserValidations


class CreateAdmin(graphene.Mutation):
    '''Handle creation of a admin user and saving to the db'''
    # items that the mutation will return
    admin = graphene.Field(AdminType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        admin = UserInput(required=True)

    @staticmethod
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        status = "Success"
        admin_validator = UserValidations()
        admin_data = admin_validator.validate_user_registration_data(
            kwargs.get("admin", ''))
        new_user = User.objects.create_superuser(**admin_data)
        assign_role(new_user, 'admin')

        admin_link = '{}users/activate/{}'.format(
            f"{info.context.get_raw_uri()}".replace(".109", ".109:8087"),
            generate_jwt(new_user.email, new_user.id))
        admin_data = {
            'username': new_user.username,
            'link': admin_link,
            'message_body': ADMIN_MAIL_BODY_MSG.format(new_user.username),
            "body": ACCOUNT_ACTIVATION_MSG
        }
        mail_subject = "{} admin account activation".format(new_user.username)
        message = "Verify your account"
        template_email('verify_account.html', new_user.email, mail_subject,
                       message, **admin_data)
        return CreateAdmin(status=status, admin=new_user, message=AGENCY_SIGNUP_SUCCESS)


class CreateUser(graphene.Mutation):
    '''Handle creation of a user and saving to the db'''
    # items that the mutation will return
    user = graphene.Field(UserType)
    status = graphene.String()
    message = graphene.String()

    class Arguments:
        '''Arguments to be passed in during the user creation'''
        input = UserInput(required=True)

    @staticmethod
    @token_required
    @login_required
    def mutate(self, info, **kwargs):
        '''Mutation for user creation. Actual saving happens here'''
        error_msg = error_dict['admin_only'].format("create a user")
        role_required(info.context.user, ['admin'], error_msg)
        status = "Success"
        validator = UserValidations()
        data = validator.validate_user_registration_data(
            kwargs.get("input", ''))
        data['is_staff'] = True
        new_user = User.objects.create_user(**data)
        assign_role(new_user, 'manager')
        user_link = '{}users/activate/{}'.format(
            f"{info.context.get_raw_uri()}".replace(".109", ".109:8087"),
            generate_jwt(new_user.email, new_user.id))
        user_data = {
            'username': new_user.username,
            'link': user_link,
            'message_body': USER_MAIL_BODY_MSG.format(new_user.agency.name),
            'body': ACCOUNT_ACTIVATION_MSG
        }
        mail_subject = "Account activation for {}".format(new_user.username)
        message = "Verify your account"
        template_email('verify_account.html', new_user.email, mail_subject,
                       message, **user_data)
        return CreateUser(status=status, user=new_user,
                          message=SIGNUP_SUCCESS.format("Staff"))


class UpdateUser(graphene.Mutation):
    '''Handle update of a user details'''
    class Arguments:
        input = UserUpdateInput(required=True)

    status = graphene.String()
    user = graphene.Field(UserType)
    message = graphene.String()

    @staticmethod
    @token_required
    @login_required
    def mutate(root, info, **kwargs):
        validator = UserValidations()
        data = validator.validate_user_update_data(kwargs.get("input", ''),
                                                   info.context.user)
        user_instance = info.context.user
        status = "Success"
        message = SUCCESS_ACTION.format("User updated")

        password = data.pop('password', None)

        for (key, value) in data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(user_instance, key, value)

        if password:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            user_instance.set_password(password)
            user_instance.is_password_set = True

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        user_instance.save()
        return UpdateUser(status=status, user=user_instance, message=message)


class PasswordReset(graphene.Mutation):
    '''Handle update of a user details'''
    class Arguments:
        input = PasswordResetInput(required=True)

    status = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):
        input_ = kwargs.get("input", '')
        check_email_validity(input_['email'])
        user = validate_user_email(input_['email'])
        status = "Success"
        message = "Reset your password"
        user_link = '{}reset-password/{}'.format(
            settings.PASSWORD_RESET_URL,
            generate_jwt(user.email, user.id, password_reset=True,
                         username=user.username))
        user_data = {
            'username': user.username,
            'link': user_link,
            'button': "Reset Password",
            'message_body': "This is a password reset request",
            'body': "To reset your password, click the link below"
        }
        mail_subject = "Password reset for {}".format(user.name)
        message = "A password reset link has been sent to your email"
        template_email('verify_account.html', user.email, mail_subject,
                       message, **user_data)
        return PasswordReset(status=status, message=message)


class CustomObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    create_admin = CreateAdmin.Field()
    create_user = CreateUser.Field()
    password_reset = PasswordReset.Field()
    update_user = UpdateUser.Field()
    token_auth = CustomObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
