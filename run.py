import time
from datetime import datetime
import praw
import configparser
import pickledb


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def do_kudos(kudos_db, user):
    if not kudos_db.exists(user):
        kudos_db.set(user, 1)
        kudos = 1
    else:
        up = kudos_db.get(user)
        kudos = up + 1
        kudos_db.set(user, kudos)
    kudos_db.dump()
    return kudos


def do_daily(daily_db, user, id):
    user_id = f'{user}{id}'
    if not daily_db.exists(user_id):
        daily_db.set(user_id, 1)
        daily_db.dump()
        return True
    else:
        print(f'{C.R}{user} is trying too hard!{C.W}')
        return False


def main():
    kudos_db = pickledb.load('data/kudos.db', False)
    daily_db = pickledb.load('data/daily.db', False)
    config = configparser.ConfigParser()
    config.read('conf.ini')
    reddit_user = config['REDDIT']['reddit_user']
    reddit_pass = config['REDDIT']['reddit_pass']
    client_id = config['REDDIT']['client_id']
    client_secret = config['REDDIT']['client_secret']
    target_subreddit = config['REDDIT']['target_subreddit']
    target_keyword = config['REDDIT']['target_keyword']
    flair_text = config['REDDIT']['flair_text']
    flair_css = config['REDDIT']['flair_css']
    test_mode = int(config['REDDIT']['test_mode'])

    reddit = praw.Reddit(
        username=reddit_user,
        password=reddit_pass,
        client_id=client_id,
        client_secret=client_secret,
        user_agent='Kudos Bot (by u/impshum)'
    )

    start_time = time.time()
    start_date = datetime.fromtimestamp(start_time).strftime("%D")
    day_of_year = datetime.fromtimestamp(start_time).strftime("%-j")

    print(f"""{C.Y}
╦╔═╦ ╦╔╦╗╔═╗╔═╗  ╔╗ ╔═╗╔╦╗
╠╩╗║ ║ ║║║ ║╚═╗  ╠╩╗║ ║ ║
╩ ╩╚═╝═╩╝╚═╝╚═╝  ╚═╝╚═╝ ╩  {C.C}v1.0{C.W}

Started: {start_date}
Keyword: {target_keyword}
""")

    for comment in reddit.subreddit(target_subreddit).stream.comments():
        created = int(comment.created_utc)
        if created >= start_time:
            body = comment.body
            if body.startswith(target_keyword):
                from_user = comment.author.name
                parent_id = comment.parent()
                submission = reddit.submission(id=parent_id)
                to_user = submission.author.name
                current_flair = submission.author_flair_text

                if to_user and from_user != to_user:
                    day_of_now = datetime.fromtimestamp(created).strftime("%-j")
                    if day_of_now != day_of_year:
                        print(f'{C.Y}Daily reset{C.W}')
                        day_of_year = day_of_now
                        daily_db.deldb()
                        daily_db.dump()
                    if do_daily(daily_db, from_user, parent_id):
                        kudos = do_kudos(kudos_db, to_user)
                        if not test_mode:
                            if current_flair:
                                if ' - ' in current_flair:
                                    current_flair = current_flair.split(' - ')[0]
                                    new_flair = f'{current_flair} - {kudos} {flair_text}'
                                elif flair_text in current_flair:
                                    new_flair = f'{kudos} {flair_text}'
                            else:
                                new_flair = f'{kudos} {flair_text}'

                            reddit.subreddit(target_subreddit).flair.set(to_user, new_flair, css_class=flair_css)

                        print(f'{C.G}+1{C.W} to {C.Y}{to_user}{C.W} from {C.P}{from_user}{C.W}')


if __name__ == '__main__':
    main()
