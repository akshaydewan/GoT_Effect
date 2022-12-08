from imdb import Cinemagoer
import sqlite3


def populate_advisory(title_id, cinemagoer, db_cursor):
    title = title_id[2:]  # strip the starting 'tt'
    advisory_data = cinemagoer.get_movie_parents_guide(title)['data']
    advisory_votes = advisory_data['advisory votes']
    nudity = advisory_votes.get('nudity', {'status': None})['status']
    violence = advisory_votes.get('violence', {'status': None})['status']
    profanity = advisory_votes.get('profanity', {'status': None})['status']
    alcohol = advisory_votes.get('alcohol', {'status': None})['status']
    frightening = advisory_votes.get('frightening', {'status': None})['status']
    insert = "UPDATE advisory " \
             "SET nudity = :nudity, " \
             "violence = :violence, " \
             "profanity = :profanity, " \
             "alcohol = :alcohol, " \
             "frightening = :frightening " \
             "WHERE title_id = :title_id"
    db_cursor.execute(insert, {"nudity": nudity, "violence": violence, "profanity": profanity, "alcohol": alcohol,
                               "frightening": frightening, "title_id": title_id})
    print("Populated ", title)


if __name__ == "__main__":
    # create an instance of the Cinemagoer class
    ia = Cinemagoer()

    # Establish a connection to the DB
    conn = sqlite3.connect("imdb.db")
    cur = conn.cursor()

    # Fetch movies with missing advisory ratings
    query = "SELECT title_id FROM advisory WHERE " \
            "nudity IS NULL AND " \
            "violence IS NULL AND " \
            "frightening IS NULL AND " \
            "profanity IS NULL AND " \
            "alcohol IS NULL " \
            "LIMIT 200"
    result_set = cur.execute(query).fetchall()
    for title in result_set:
        print(title[0])
        populate_advisory(title[0], ia, cur)
        conn.commit()
    conn.close()
