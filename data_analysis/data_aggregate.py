from pymongo import MongoClient
from datetime import datetime


class AggregationUpdateDate:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['haktan_ozer']
        self.collection = self.db['news']
        self.documents = list(self.collection.find())
        self.datetime_formatter()

    def datetime_formatter(self):
        """
        This method converts string type update_date to datetime type
        :return:
        """
        for document in self.documents:
            if 'update_date' in document and isinstance(document['update_date'], str):
                try:
                    document['update_date'] = datetime.strptime(document['update_date'], '%Y-%m-%d')
                    self.collection.update_one({'_id': document['_id']},
                                               {'$set': {'update_date': document['update_date']}})
                except ValueError:
                    print(f"Error: Date conversion failed - Document: {document}")

    def aggregation(self):
        """
        This method groups documents by update_date
        :param self:
        :return: Date, Count, Documents
        """
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$update_date'},
                        'month': {'$month': '$update_date'},
                        'day': {'$dayOfMonth': '$update_date'},
                    },
                    'count': {'$sum': 1},
                    'documents': {'$push': '$$ROOT'}
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))

        for group in result:
            print(f"Date: {group['_id']['year']}-{group['_id']['month']}-{group['_id']['day']}")
            print(f"Count: {group['count']}")
            print("Documents:")
            for document in group['documents']:
                print(document)
        self.client.close()


if __name__ == "__main__":
    aggregation = AggregationUpdateDate()
    aggregation.aggregation()
