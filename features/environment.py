from behave import fixture, use_fixture

from application import app


@fixture
def app_client(context, *args, **kwargs):
    """Setup test client for Flask app"""
    app.config["TESTING"] = True
    context.client = app.test_client()
    yield context.client


def before_feature(context, feature):
    use_fixture(app_client, context)
