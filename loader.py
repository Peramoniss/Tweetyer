import baseConnection as db
import json

def seed_database():
    # 1. Define Constraints (Crucial for performance and data integrity)
    constraints = [
        "CREATE CONSTRAINT post_id IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT user_username IF NOT EXISTS FOR (u:User) REQUIRE u.name IS UNIQUE"
    ]

    # 2. Define Sample Data
    seed_query = """
    MERGE (u1:User {name: 'Tweety'})
    MERGE (u2:User {name: 'Sylvester'})
    MERGE (u3:User {name: 'Sylvester Jr.'})
    MERGE (u4:User {name: 'Grandma'})
    MERGE (u5:User {name: 'Hector the Bulldog'})
    MERGE (u6:User {name: 'Claude Cat'})
    MERGE (u7:User {name: 'Hippety Hopper'})
    
    MERGE (u2)-[:FOLLOWS]->(u1)
    MERGE (u3)-[:FOLLOWS]->(u1)
    MERGE (u4)-[:FOLLOWS]->(u1)
    MERGE (u5)-[:FOLLOWS]->(u1)
    MERGE (u6)-[:FOLLOWS]->(u1)
    MERGE (u3)-[:FOLLOWS]->(u2)
    MERGE (u2)-[:FOLLOWS]->(u3)
    MERGE (u2)-[:FOLLOWS]->(u7)
    MERGE (u3)-[:FOLLOWS]->(u7)
    MERGE (u5)-[:FOLLOWS]->(u2)
    MERGE (u5)-[:FOLLOWS]->(u3)
    MERGE (u5)-[:FOLLOWS]->(u4)
    MERGE (u5)-[:FOLLOWS]->(u6)
    MERGE (u7)-[:FOLLOWS]->(u2)
    MERGE (u7)-[:FOLLOWS]->(u3)
    
    MERGE (p1:Post {id: 0, text: "I'm hungry!", creation: datetime()})
    MERGE (u2)-[:POSTED]->(p1)

    MERGE (p2:Post {id: 1, text: "Thufferin' Thuccotash!", creation: datetime()})
    MERGE (u2)-[:POSTED]->(p2)

    MERGE (p3:Post {id: 2, text: "I tawt I taw a putty tat!", creation: datetime()})
    MERGE (u1)-[:POSTED]->(p3)

    MERGE (p4:Post {id: 3, text: "I did, I did thaw a putty tat!", creation: datetime()})
    MERGE (u1)-[:POSTED]->(p4)
    MERGE (p4)-[:ANSWERS]->(p3)

    MERGE (u2)-[:LIKED]->(p3)
    MERGE (u3)-[:LIKED]->(p3)
    MERGE (u4)-[:LIKED]->(p3)
    MERGE (u5)-[:LIKED]->(p3)

    MERGE (u2)-[:LIKED]->(p1)
    MERGE (u3)-[:LIKED]->(p1)

    MERGE (u4)-[:LIKED]->(p2)
    MERGE (u4)-[:LIKED]->(p4)

    MERGE (u5)-[:LIKED]->(p1)
    MERGE (u6)-[:LIKED]->(p4)
    """

    f = open('memory.sav', 'w')
    f.write('4') # Saves correct id savepoint
    f.close()

    f = open('credentials.json', 'r')
    data = json.load(f)
    f.close()

    with db.driver.session(database=data["database"]) as session:  
        for c in constraints:
            session.run(c)
        session.run(seed_query)
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()