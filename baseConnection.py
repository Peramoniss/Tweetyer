# Example in Python using the Neo4j driver
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "senhasegura"

driver = GraphDatabase.driver(uri, auth=(username, password))

CURR_ID = 0
CURR_PAGE = 0

def create_user(tx, name):
    tx.run("CREATE (u:User {name: $name})", name=name)

def post_tweet(tx, username, text):
    global CURR_ID
    tx.run("MATCH (u:User {name: $name})\nCREATE (p:Post {text: $text, id: $id, creation: datetime()})\nCREATE (u)-[:POSTED]->(p);", name=username, text=text, id=CURR_ID)
    CURR_ID += 1

def like_tweet(tx, username, post_id):
    tx.run("MATCH (p:Post {id: $id}), (u:User {name: $name})\nCREATE (u)-[:LIKED]->(p);", name=username, id=post_id)

def answer_tweet(tx, answer_post, original_post):
    global CURR_ID
    tx.run("MATCH (p:Post {id: $original}), (t:Post {id: $answer})\nCREATE (t)-[:ANSWERS]->(p);", original=original_post, answer=answer_post)
    CURR_ID += 1

def follow_user(tx, follower, followee):
    tx.run("MATCH (u:User {name: $followee}), (f:User {name: $follower})\nCREATE (f)-[:FOLLOWS]->(u);", followee=followee, follower=follower)

def show_feed(tx, username):
    # global CURR_PAGE
    # skip = CURR_PAGE * 10
    results = tx.run("MATCH (n:User {name: $name})\nMATCH ( (n)-[:FOLLOWS]->(y) )\nMATCH ( (y)-[:POSTED]->(p) )\nRETURN p.text as post, p.id as id, p.creation as creation, y.name as username, COUNT{ ()-[:LIKED]->(p) } as likes, COUNT{ ()-[:FOLLOWS]->(y) } as followers\nORDER BY likes DESC, followers DESC, creation DESC", name=username) #\nSKIP $skip\nLIMIT 10 TODO: Implement pagination to fasten the queries maybe?
    return list(results)

def match_answers(tx, id):
    results = tx.run("MATCH (p:Post {id: $id})\nMATCH (q)-[:ANSWERS]->(p)\nMATCH (u)-[:POSTED]->(q)\nRETURN q.text as post, q.id as id, q.creation as creation, u.name as username, COUNT{ ()-[:LIKED]->(q) } as likes, COUNT{ ()-[:FOLLOWS]->(u) } as followers\nORDER BY likes DESC, followers DESC, creation DESC;", id=id)
    return list(results)

def match_user(tx, name):
    results = tx.run("MATCH (u:User {name: $name})\nRETURN u;", name=name)
    return list(results)

def match_posts(tx, username):
    results = tx.run("MATCH (u:User {name: $name})\nMATCH (u)-[:POSTED]->(p)\nRETURN p.text as post, p.id as id, p.creation as creation, u.name as username, COUNT{ ()-[:LIKED]->(p) } as likes, COUNT{ ()-[:FOLLOWS]->(u) } as followers\nORDER BY likes DESC, followers DESC, creation DESC;", name=username)
    return list(results)

def match_like(tx, username, post_id):
    results = tx.run("MATCH (p:Post {id: $id}), (u:User {name: $name})\nMATCH (u)-[:LIKED]->(p)\nRETURN p;", name=username, id=post_id)
    return list(results)

# with driver.session(database="twitter") as session:
#     session.execute_write(create_user, "Joao")
#     results = session.execute_write(show_feed, "Joao")
#     for r in results:
#         print(r.data())

# driver.close()
