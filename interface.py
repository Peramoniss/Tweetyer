import baseConnection as db
import arrow
import os

USERNAME = None

# Example usage with your data:
# result = session.execute_read(...)
# print(format_time_ago(result['your_date_field']))

def leave():
    f = open('memory.sav', 'w')
    f.write(str(db.CURR_ID))
    f.close()
    exit(0)

def makeAPost(answer_to = None):
    text = ""
    while True:
        text = input("Write your thoughts: ")
        if len(text) < 255:
            break
        c = input("Your thoughts are too long. You want to rewrite (1) or trim (2)?")
        if c != '1':
            text = text[:255]
            break
        #else, repeats the process of writing the thoughts
    
    session.execute_write(db.post_tweet, USERNAME, text)
    if answer_to is not None:
        session.execute_write(db.answer_tweet, db.CURR_ID-1, answer_to)

    print("Posted")


def get_feed(session, results, pattern : str = '-'):
    for r in results:
        print(pattern*60)
        data_dict = r.data()
        # print(data_dict)
        date = arrow.get(data_dict['creation'].to_native()).humanize()
        heart = "♡⁠"
        liked = session.execute_read(db.match_like, USERNAME, data_dict['id'])
        if liked:
            heart = "❤︎"

        print(f'{data_dict['username']} says:\n" {data_dict['post']} "\n{data_dict["likes"]} {heart}\nPosted {date}')
        c = input("1 - Like this post; 2 - Next post; 3 - Answer post; 4 - See answers; 5 - Leave feed. Your choice: ")
        if c == '1':
            if liked:
                print("You already liked this post")
            else:
                session.execute_write(db.like_tweet, USERNAME, data_dict['id'])
                print("Post liked succesfully")
        elif c == '2':
            continue 
        elif c == '3':
            makeAPost(data_dict["id"])
        elif c == '4':
            answers = session.execute_read(db.match_answers, data_dict['id'])
            if not answers:
                ans = input("There are no answers. Do you wish to write your own (y/n)? ")
                if ans == 'y':
                    makeAPost(data_dict['id'])

                continue
            get_feed(session, answers, '~')
            print("No more comments for this post...")
        else:
            break

    print("="*60)

def logged_menu(session):
    while True:
        global USERNAME
        choice = input(f"Hello, {USERNAME}! What do you want to do?\n   1 - Show feed\n   2 - Make post\n   3 - Follow someone\n   4 - See your posts\n   5 - Log out\n   0 - Quit application\n")
        try:
            choice = int(choice)
        except:
            raise Exception("YOU FOOL. OBBEY THE RULES. CHOSE A VALID CHOICE!!!")
        if choice == 1:
            results = session.execute_read(db.show_feed, USERNAME)
            if not results:
                print("You currently have nothing in the feed.")
                continue

            get_feed(session, results)
            print(f'No more feed for you today...\n{"="*60}')
        elif choice == 2:
            makeAPost(None)
        elif choice == 3:
            followee = input("Chose an user to follow: ")
            if followee == USERNAME:
                print("You can't follow yourself")
                continue

            results = session.execute_read(db.match_user, followee)
            if not results:
                print("User not found")
                continue

            session.execute_write(db.follow_user, USERNAME, followee)
            print(f"{followee} followed succesfully!")
        elif choice == 4:
            results = session.execute_read(db.match_posts, USERNAME)
            if not results:
                print("You have no posts")
                continue
            
            get_feed(session, results, '*')
            print("This is all you have posted so far...")

        elif choice == 5:
            print("Logging out")
            USERNAME = None
            return 1
        else:
            leave()
            


def menu(session):
    global USERNAME
    reset = 0

    while True:
        choice = input("Hello! Chose your operation:\n   1 - Log In\n   2 - Sign In\n   0 - Quit application\n")
        try:
            choice = int(choice)
        except:
            raise Exception("YOU FOOL. OBBEY THE RULES. CHOSE A VALID CHOICE!!!")

        if choice == 1:
            print("Insert your username: ", end="")
            _name = input()
            results = session.execute_read(db.match_user, _name)
            if not results:
                print("Username not found...")
                return
            # print(results[0].data()['u']['name'])
            
            USERNAME = _name
            print("Logged In successfully! Redirecting...")
            reset = logged_menu(session)
        elif choice == 2:
            print("Insert your new username: ", end="")
            _name = input()
            results = session.execute_read(db.match_user, _name)
            if results:
                print("Username already exists. Try again...")
                return

            results = session.execute_write(db.create_user, _name)
            USERNAME = _name
            print('Registered successfully. Redirecting...')
            reset = logged_menu(session)
        else:
            print('Quitting application...')
        
        if not reset:
            leave()

if __name__ == '__main__':
    try:
        f = open('memory.sav', 'r')
        db.CURR_ID = int(f.read())
        f.close()
    except:
        db.CURR_ID = 0

    with db.driver.session(database="twitter") as session:
        # CREATE CONSTRAINT post_id_unique IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE
        while True:
            menu(session)
            print("="*60)

#leave()


# with db.driver.session(database="twitter") as session:
#     session.execute_write(db.create_user, "Ramon")
#     results = session.execute_read(db.show_feed, "Ramon")
#     for r in results:
#         print(r.data())

# db.driver.close()