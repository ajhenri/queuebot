import os
import time
import constants
import commands
from slackclient import SlackClient
from collections import deque

# Name of the bot
BOT_NAME = 'queuebot'
# Instantiate the Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_API_KEY'))

'''
The Bot object which will describe the behavior of the Slack queuebot.
'''
class Bot:

    def __init__(self):
        self.users = []
        self.circular = False
        self.items = []
        self.phrases = []

        slack_users = slack_client.api_call(
            "users.list",
            presence=True
        )

        if slack_users['ok']:
            for user in slack_users['members']:
                if 'name' in user and user.get('name') == BOT_NAME:
                    self.id = user.get('id')
                elif 'presence' in user and user.get('presence') == 'active':
                    self.users.append(user.get('name'))

            self.items = deque(self.users)
        else:
            print('Slack Error: ' + slack_users['error'])

    '''
    Read a command from the parsed Slack input.

    Args:
        text (str): the user's input from slack
        channel (str): the current channel from which input came
    '''  
    def read_command(self, text, channel):
        response = commands.unknown_command
        command = text.split(' ')[0]
        if command in commands.dispatch:
            response = commands.dispatch[command](text, self)

        if 'items' in response:
            self.items = response['items']
        if 'circular' in response:
            self.circular = response['circular']
        if 'phrases' in response:
            self.phrases = response['phrases']
        
        slack_client.api_call("chat.postMessage", channel=channel,
                            text=response['text'], as_user=True)

    '''
    Parse the slack output.

    Args:
        output_list (list): the slack rtm output
    '''  
    def parse_slack_output(self, output_list):
        bot_tag = "<@" + self.id + ">"
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'type' in output:
                    if output['type'] == 'hello':
                        res = slack_client.api_call("chat.postMessage", channel='#general',
                            text=commands.hi['text'], as_user=True)
                if output and 'text' in output:
                    if bot_tag in output['text']: #return everything after the @bot string
                        return output['text'].split(bot_tag)[1].strip().lower(), \
                                output['channel']
                    else:
                        has_phrase = False
                        for phrase in self.phrases: #check if output text is in the designated phrases
                            if phrase in output['text']:
                                has_phrase = True #means the bot should take it's 'cue'
                                break
                        if has_phrase:
                            return constants.CALL_QUEUE_COMMAND, output['channel']

        return None, None

    ''' Mutators '''
    def setQueue(self, q):
        self.items = q

    ''' Accessors '''
    def getQueue(self):
        return self.items

    def getUsers(self):
        return self.users

    def isCircular(self):
        return self.circular
    

if __name__ == "__main__":
    bot = Bot()

    if slack_client.rtm_connect():
        print("Connection established. Queuebot is up and running!")
        while True:
            command, channel = bot.parse_slack_output(slack_client.rtm_read())
            if command and channel:
                bot.read_command(command, channel)
            time.sleep(constants.READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")