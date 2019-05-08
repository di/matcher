from wtforms import Form, IntegerField, StringField, validators


class NewMatchForm(Form):
    title = StringField("Title for your donation drive", [validators.DataRequired()])
    goal = IntegerField(
        "Goal amount (USD, integer)",
        [validators.DataRequired(), validators.NumberRange(min=10)],
    )


class NewDonationForm(Form):
    name = StringField(
        "Your name (optional)",
        default="Anonymous",
        render_kw={"placeholder": "Anonymous"},
    )
    transaction_id = StringField(
        "Transaction # from your donation confirmation email",
        [validators.DataRequired()],
    )
