import messages as m
import constants
from collections import deque

def help(command, bot):
    '''
    List the available commands and how to use them. 
    If a command is set, it will list that command only.

    Args:
        command (str): the user's text input
        bot (Bot): the active bot
    '''  
    if(command != None and command not in constants.HELP_COMMAND):
        command = command.split(constants.HELP_COMMAND)[1].strip()
        if command[0] != '/':
            command = '/' + command

        if(command in dispatch):
            return { 'text': m.get_help_message(command) }
        else:
            return { 'text': 'Sorry, this command was not found.' }
    else:
        return { 'text': m.get_help_all() }

def set_queue(command, bot):
    '''
    Create a queue with a list of items. Phrases passed will trigger a deque.
    If items is not set, the queue will automatically use the Slack user list.

    Args:
        command (str): the user's text input
        bot (Bot): the active bot
    '''  
    if(command):
        circular = '-c' in command
        items = bot.getUsers()
        phrases = []

        has_items = False 
        has_phrases = False
        arg1 = command.split("--items")
        if len(arg1) > 1:
            has_items = True
            arg2 = arg1[1].split("--phrases")
            if len(arg2) > 1:
                has_phrases = True

        if has_items and has_phrases:
            items = arg2[0].strip().split(",")
            phrases = arg2[1].strip().split(",")
        elif has_items:
            items = arg1[1].strip().split(",")

        return {
            'items': deque(items),
            'circular': circular,
            'phrases': phrases,
            'text': m.get_message('set_success') 
        }

def cancel_queue(command, bot):
    '''
    Cancel the current queue.

    Args:
        command (str): the user's text input
        bot (Bot): the active bot
    '''
    return {
        'items': deque(bot.getUsers()),
        'circular': False,
        'phrases': [],
        'text': m.get_message('cancel_success')
    }

def call_next(command, bot):
    '''
    Get the next in line from the queue.

    Args:
        command (str): the user's text input
        bot (Bot): the active bot
    '''  
    q = bot.getQueue()
    circular = bot.isCircular()

    next_person = None
    try:
        if circular:
            next_person = q[0]
            q.rotate(1)
        else:
            next_person = q.popleft()
    except:
        pass

    msg = m.get_message('next_error')
    if next_person != None:
        msg = m.get_message('next_success').replace('{name}', next_person)

    return {
        'items': q,
        'circular': circular,
        'text': msg
    }

''' Response for to saying hi. '''
hi = {
    'text': m.get_message('hi')
}

''' Response to gibberish. '''
unknown_command = {
    'text': m.get_message('not_sure')
}

''' Event dispatcher for list of known commands. '''
dispatch = {
    constants.HELP_COMMAND: help,
    constants.SET_QUEUE_COMMAND: set_queue,
    constants.CANCEL_QUEUE_COMMAND: cancel_queue,
    constants.CALL_QUEUE_COMMAND: call_next
}