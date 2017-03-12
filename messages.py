import json
import constants

messages = json.load(open('messages.json'))

'''
Get a message from the object model.

Args:
    m (str): the text key
'''  
def get_message(m):
    if m in messages:
        return messages[m]['text']

'''
Get a help message from the object model (which is structured differently)

Args:
    m (str): the text key
'''
def get_help_message(c):
    command = messages[constants.HELP_COMMAND][c]
    msg = '*' + command['name'] + '* : ' + command['synopsis'] + '\n'
    if 'usage' in command:
        msg += '> Usage: '
        msg += ' `' + command['usage'] + '` \n'
    if 'options' in command:
        msg += '> Options: '
        for option in command['options']:
            msg += '\n'
            msg += '> _' + option + ': ' + command['options'][option] + '_'

    return msg

'''
Gets all help messages.
'''  
def get_help_all():
    msg = 'Here\'s the list of commands you can use to communicate with me. \n'
    for c in messages[constants.HELP_COMMAND]:
        msg += '\n' + get_help_message(c) + '\n'
    return msg