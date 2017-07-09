import requests
import sys
from os import environ as env

from flask import Flask, request, json
from webview.views import WEB

from message_builders.message_builders import simple_message_builder, generic_message_builder, button_message_builder, \
    postback_button_builder

def get_config_value(config_key, default_value):
    try:
        result = env[config_key]
    except KeyError:
        return default_value
    return result

VALIDATION_TOKEN = get_config_value('MESSENGER_VALIDATION_TOKEN', '')
PAGE_ACCESS_TOKEN = get_config_value('MESSENGER_PAGE_ACCESS_TOKEN', '')

auto_messages = {
    'welcome_message': 'Hi! Im Resrv. You can easily make reservations with my help. Please select your destination.',
    'not_implemented_function': 'Sorry but this function is not implemented yet.'
}


app = Flask(__name__)
app.register_blueprint(WEB)





@app.route('/', methods=['GET'])
def webhook_get():
    # when the endpoint is registered as a webhook, it must echo back
    #  the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VALIDATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook_post():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data.get("object", "") == "page":

        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                if messaging_event.get("message"):  # someone sent us a message

                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    message_data = simple_message_builder(message_text)
                    send_message(sender_id, message_data)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                    payload = messaging_event['postback'].get('payload', '')
                    postback_event_handler(sender_id, payload)
    return "ok", 200

def getstarted_function(recipient_id):

    buttons = [postback_button_builder(title='Start reservation', payload='START_RESERVATION')]
    message_data = button_message_builder(auto_messages['welcome_message'], buttons=buttons)
    send_message(recipient_id, message_data)



def postback_event_handler(recipient_id, received_message):
    commands_dispatcher = {
        'GET_STARTED_PAYLOAD': getstarted_function
    }
    if received_message in commands_dispatcher:
        commands_dispatcher[received_message](recipient_id, )
    else:
        message_data = simple_message_builder(auto_messages['not_implemented_function'])
        send_message(recipient_id, message_data=message_data)



def send_message(recipient_id, message_data):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_data))

    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": message_data
    }
    call_api(data)

def send_image_message():
    pass
def send_gif_message():
    pass
def send_button_message():
    pass
def send_generic_message():
    pass
def send_receipt_message():
    pass
def send_quick_reply():
    pass
def send_text_message():
    pass


def call_api(message_data):
    log("sending message {}".format(message_data))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=json.dumps(message_data))
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    log("VALIDATION TOKEN:: " + VALIDATION_TOKEN)
    log("ACCESS TOKEN: " + PAGE_ACCESS_TOKEN)
    app.run(debug=True)
