def CalculateTotal(orders):
    sum = 0
    for i in orders:
        sum += i["value"]
    return sum

class userManager:
    def __init__(self):
        self.users = []
    
    def addUser(self, name, id):
        new_user = {"name": name, "id": id}
        self.users.append(new_user)
    
    def findUser(self, id):
        for user in self.users:
            if user["id"] == id:
                return user
        return None