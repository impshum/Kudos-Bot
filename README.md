## Kudos Bot

Allows Reddit users to give kudos to each other on a chosen subreddit.

![](ss.jpg?raw=true)

### Instructions

- Install requirements ```pip install -r requirements.txt```
- Create Reddit (script) app at https://www.reddit.com/prefs/apps/ and get your id, tokens etc
- Edit conf.ini with your details
- Run it ```python run.py```

#### Info

The bot only fires when a comment **starts with** target keyword.

Only allows users to give 1 kudos per post per day. This resets every day.

To set flair css edit the stylesheet on Reddit and add something like this for the flair css. We're working on the class kudos here...

    .flair-kudos {
        background-color: #000;
        color: #fff;
        padding: 2px 19px;
        font-weight: 600;
    }

If you're not using Unix you won't see the colours in the terminal (command prompt). Here's how to get them working: https://recycledrobot.co.uk/words/?print-python-colours

### Tip

BTC - 1AYSiE7mhR9XshtS4mU2rRoAGxN8wSo4tK
