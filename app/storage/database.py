from app import client_mongo


class Storage(object):
    def __init__(self, db: str = None, collection: str = None):
        self.db = client_mongo[db]
        self.collection = collection

    def update(self, name: dict = None, data: dict = None):
        """

        :param name:
        :param data:
        :return:
        """
        return self.db[self.collection].update(name, {"$set": data})

    def upsert(self, name: dict = None, data: dict = None):
        """

        :param name:
        :param data:
        :return:
        """
        return self.db[self.collection].update(name, {"$set": data}, upsert=True)

    def delete(self, name: dict = None):
        """

        :param name:
        :return:
        """
        return self.db[self.collection].delete_one(name)

    def get(self):
        return self.db[self.collection].find()

    def get_id(self):
        pass

    def delete_all(self):
        pass
