# queuebot

The queuebot does exactly what it's name entails. It is a Slack bot that acts a queue, and it can find and tell you the next thing that has to be dequeued.

Calling the next in line can be triggered either manually or by user-defined phrases in Slack.
The queuebot can save you the trouble of figuring out the next person whose turn it is to do a specific thing.

## Installation

You must have Python 2.7+ and pip installed. Though it is not a requirement, it is ideal that you have virtualenv installed as well. Activate your virtual environment, and run the following:

```bash
$ git clone https://github.com/ajhenri/queuebot.git
$ cd queuebot
$ pip install -r requirements.txt
```

## Usage

You must have an [API token](#getting-the-api-token-for-your-slack-channel) to authenticate the bot on your Slack channel. Go to your bot settings and copy the api key. Open the Terminal, and run the following in your project folder:

```bash
export SLACK_BOT_API_KEY='Your Slack API token goes here'
```

`SLACK_BOT_API_KEY` is an environment variable that must be set before running the program.
Please make sure you do this before running the script.

Instruction | Examples | Description
--- | --- | ---
**/help** | `@queuebot /help` | Gives a list of available commands and shows how they can be used.
**/set** | `@queuebot /set` | Creates/modifies the queue to cycle through the items list upon hearing the said phrases. Options: -c, --items, --phrases
**/cancel** | `@queuebot /cancel` | Cancel the existing queue.
**/next** | `@queuebot /next` | Manually call the next item in the queue. 

NOTE: Instructions must always be prefixed with `@queuebot`.

## Launching the bot

Assuming you followed the installation and usage details, run the following:

```bash
$ python queuebot.py
```

As stated earlier, set your `SLACK_BOT_API_KEY` environment variable before running the queuebot script. If you don't want to do this each time, you can temporarily set the key in the project itself.

## Upcoming Improvements

* Allow for multiple queues to be set at once.
* Add interaction/buttons to get information from the user.
* Provide a different way to store the queue data.
* Written tests.

## License

Released under [MIT License](LICENSE). © Amanda J. Henri