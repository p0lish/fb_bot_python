
def simple_message_builder(message_text='', metadata=''):
    result = {
        "text": message_text
    }
    if metadata:
        result["metadata"] = metadata
    return result


def element_builder(title='',subtitle='',
                    image_url=None,
                    default_action=None,
                    buttons=None
                    ):
    if buttons is None:
        buttons = []
    if len(title) > 80:
        print('WARNING: title cannot be longer than 80 characters!')
    if len(subtitle) > 80:
        print('WARNING: subtitle cannot be longer than 80 characters!')
    if len(buttons) > 3:
        print('WARNING: Only 3 buttons can applicable')


    result = {
        'title': title,
        'subtitle': subtitle,
        'image_url': image_url,
        'default_action': default_action,
        'buttons': buttons
    }
    return result

def url_button_builder(title='',
                       url='',
                       webview_height_ratio='compact',
                       messenget_extensions=False,
                       fallback_url='',
                       webview_share_button='hide'
                       ):
    result = {
        'type': 'web_url',
        'title': title,
        'utl': url,
        'webview_height_ratio': webview_height_ratio,
        'messenget_extensions': messenget_extensions,
        'fallback_url': fallback_url,
        'webview_share_button': webview_share_button
    }
    return result


def postback_button_builder(title='', payload=''):
    result = {
        'type': 'postback',
        'title': title,
        'payload': payload
    }
    return result


def generic_message_builder(
        template_type='generic',
        sharable=False,
        image_aspect_ratio='horizontal',
        elements=None):

    if elements is None:
        elements = []
    attachment = {}
    if image_aspect_ratio not in ['horizontal', 'square']:
        image_aspect_ratio = 'horizontal'


    result = {
        "attachment": attachment
    }

    payload = {
        "template_type": template_type,
        "sharable": sharable,
        "image_aspect_ratio": image_aspect_ratio,
        "elements": elements[-10:]
    }

    attachment['payload'] = payload
    return result

