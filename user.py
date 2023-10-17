class User:
    def __init__(self):
        self.username = ''
        self.city = ''
        self.name = ''
        self.order = {}
        self.order['desc'] = ''
        self.order['cat'] = ''
        self.order['dur'] = ''
        self.order['loc'] = ''
        self.order['createdAt'] = ''
        self.order['id'] = ''
        self.order['comment'] = ''
        self.orders = []
        self.role = ''
        self.currOrderIndex = 0
