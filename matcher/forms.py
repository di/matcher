from wtforms import Form, IntegerField, StringField, validators


class NewMatchForm(Form):
    title = StringField(
        "Title for your donation drive",
        [validators.DataRequired()],
        render_kw={"placeholder": "My Awesome Drive", "size": "35"},
    )
    name = StringField(
        "Your name (optional)", render_kw={"placeholder": "Anonymous", "size": "35"}
    )
    twitter = StringField(
        "Your Twitter handle (optional)",
        render_kw={"placeholder": "your_twitter_handle", "size": "35"},
    )
    goal = IntegerField(
        "Goal amount (USD, integer)",
        [validators.DataRequired(), validators.NumberRange(min=10)],
        render_kw={"placeholder": "10.00", "size": "35"},
    )


class NewDonationForm(Form):
    name = StringField(
        "Your name (optional)",
        default="Anonymous",
        render_kw={"placeholder": "Anonymous", "size": "35"},
    )
    twitter = StringField(
        "Your Twitter handle (optional)",
        render_kw={"placeholder": "your_twitter_handle", "size": "35"},
    )
    transaction_id = StringField(
        "Transaction # from your donation confirmation email",
        [validators.DataRequired()],
        render_kw={"placeholder": "XXXXXXXXXXXXXXXXX", "size": "35"},
    )
