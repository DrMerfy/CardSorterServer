from bson import ObjectId
from flask import current_app, jsonify

from flaskr.db import get_db


class Participant:
    def __init__(self):
        with current_app.app_context():
            self.studies = get_db()['studies']
            self.participants = get_db()['participants']
        self.participant_id = 0

    def post_categorization(self, study_id, categories, non_sorted):
        study = list(self.studies.find({'_id': ObjectId(study_id)}))

        if len(study) == 0:
            return {'message': 'STUDY NOT FOUND'}

        # Calculate some (very) small statistics
        categories_no = len(categories)
        cards_sorted = 0
        for category in categories:
            cards_sorted += len(categories[category]['cards'])

        # Calculate percentage
        cards_sorted = int((cards_sorted / len(study[0]['cards'])) * 100)

        # Create the participant instance
        item = self.participants.insert_one({
            'categories': categories,
            'not_sorted': non_sorted,
            'cards_sorted': str(cards_sorted)+'%',
            'categories_no': categories_no,
        })

        self.participant_id = ObjectId(item.inserted_id)

        # Link participant to the study
        self.studies.update_one({'_id': ObjectId(study_id)}, {'$push': {'participants': self.participant_id}})