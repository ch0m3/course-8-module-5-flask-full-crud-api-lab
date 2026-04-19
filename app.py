# ...existing code...
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]
# ...existing code...

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()
    title = data.get("title")
    if not title or not isinstance(title, str):
        return jsonify({"error": "Field 'title' is required and must be a string"}), 400

    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, title)
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    data = request.get_json()
    title = data.get("title")
    if not title or not isinstance(title, str):
        return jsonify({"error": "Field 'title' is required and must be a string"}), 400

    for event in events:
        if event.id == event_id:
            event.title = title
            return jsonify(event.to_dict()), 200

    return jsonify({"error": "Event not found"}), 404

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for i, event in enumerate(events):
        if event.id == event_id:
            removed = events.pop(i)
            return jsonify({"message": "Event deleted", "event": removed.to_dict()}), 200

    return jsonify({"error": "Event not found"}), 404
# ...existing code...

if __name__ == "__main__":
    app.run(debug=True)