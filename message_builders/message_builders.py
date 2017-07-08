
def simple_message_builder(message_text='', metadata=''):
    result = {
        "text": message_text
    }
    if metadata:
        result["metadata"] = metadata
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
        "elements": elements
    }

    if payload is not None:
        attachment['payload'] = payload
    return result

