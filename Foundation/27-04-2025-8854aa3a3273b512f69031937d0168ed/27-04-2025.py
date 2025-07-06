# We are builders and we are selling home located in "abc-123-werr-234"

class Home():
    def __init__(self):
        self.property_size = "1200sqft"
        self.location = "abc-123-werr-234"
        self.house_left = 100

    def buy_house(self, customer_name):
        print("Congraturations ", customer_name, "You have secured a house of size ", self.property_size, "at location ", self.location)
        self.house_left-=1
        self.house_left = self.house_left-1
        print("House left : ", self.house_left)


builder_manager = Home()
builder_manager.buy_house("Monal")
builder_manager.buy_house("Alekhya")
builder_manager.buy_house("Ashar")
builder_manager.buy_house("Yusuf")
builder_manager.buy_house("Rohit")
builder_manager.buy_house("Riyan")