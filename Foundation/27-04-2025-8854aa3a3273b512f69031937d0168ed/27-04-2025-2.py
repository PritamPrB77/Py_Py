# We are create this for builders

class Home():
    def __init__(self, size, location, total_house, builder_name):
        self.property_size = size
        self.location = location
        self.house_left = int(total_house)
        self.builder_name = builder_name

    def buy_house(self, customer_name):
        print("Congraturations ", customer_name, "You have secured a house of size ", self.property_size, "at location ", self.location, " from builder ", self.builder_name)
        self.house_left-=1
        print("House left : ", self.house_left)


builder_manager_1 = Home("2000sqft", "bengaluru", "2000", "brigade")
builder_manager_2 = Home("700sqft", "delhi", "200", "embassy")
builder_manager_3 = Home("4000sqft", "US", "5400", "cessina")

builder_manager_1.buy_house("Monal")
print(builder_manager_1.house_left)

builder_manager_1.buy_house("Alekhya")
print(builder_manager_1.house_left)

builder_manager_1.buy_house("Ashar")
print(builder_manager_1.house_left)

builder_manager_2.buy_house("Yusuf")
builder_manager_2.buy_house("Rohit")

builder_manager_3.buy_house("Riyan")