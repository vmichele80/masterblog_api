from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# deaktiviert die sortierung se elementen in der Json
app.config["JSON_SORT_KEYS"] = False
app.json.sort_keys = False

CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():

    if request.method == 'POST':
        # Get the new post data from the client
        new_post = request.get_json()
        # this validates the data is in the correct format
        if not validate_post_data(new_post):
            return jsonify({"error": "Title and/or Content of the post are missing"}), 400

        # Generate a new ID for the book
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        saved_post = {
            "id": new_post["id"],
            "title": new_post["title"],
            "content": new_post["content"]
        }

        # Add the new book to our list
        POSTS.append(saved_post)

        # Return the new book data to the client
        return jsonify(saved_post), 201


    else:
        # it means it is a GET request
        return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
