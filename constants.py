''' List of constants necessary for the project. '''

# Name of the Slack bot.
BOT_NAME = 'queuebot'
# Command to list the available commands and how to use them.
HELP_COMMAND = "/help"
# Command to create/modify the queue.
SET_QUEUE_COMMAND = "/set"
# Command to cancel current queue.
CANCEL_QUEUE_COMMAND = "/cancel"
# Command to deque an item.
CALL_QUEUE_COMMAND = "/next"
# Delay between rtm reads.
READ_WEBSOCKET_DELAY = 1
