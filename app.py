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

@app.route("/events", methods=["POST"])
def create_event():
   
    data = request.get_json()
    new_event = Event(id=len(events) + 1, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event.id == event_id:
            event.title = data["title"]
            return jsonify(event.to_dict()), 200
    return jsonify({"error": "Event not found"}), 404


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    
    event_exists = any(event.id == event_id for event in events)
    if not event_exists:
        return jsonify ({"error": "Event not found"}),404
    events = [event for event in events if event.id != event_id]
    return "", 204


#get an event by id
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    for event in events:
        if event.id == event_id:
            return jsonify(event.to_dict())
    return jsonify({"error": "Event not found"}), 404


#get all events
@app.route("/events", methods=["GET"])
def get_all_events():
    return jsonify([event.to_dict() for event in events])

if __name__ == "__main__":
    app.run(debug=True)


