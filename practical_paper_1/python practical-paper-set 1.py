# 1. Write output for the below statements, if you find any error please write the error.
# -> [] * 3 = []
# -> ('a', 'b', 'c') * 2 = ('a', 'b', 'c', 'a', 'b', 'c')
# -> (2) ** 2 = 2
# -> [{}] * 2 = [{}, {}]
# -> {3:1} * 2 = TypeError: unsupported operand type(s) for *: 'dict' and 'int'
# -> ‘123’ + 2 = TypeError: can only concatenate str (not "int") to str
# -> ['a', 'b', 'c'] + ‘rf’ = TypeError: can only concatenate list (not "str") to list
# -> (2, 4) ** 2 = TypeError: unsupported operand type(s) for ** or pow(): 'tuple' and 'int'
# -> Assume Z = ['P', 'L', ']' ] and then Z += 'SE'. What will be the output of print(Z)? = ['P', 'L', ']', 'S', 'E']

# 2 program check given number is armstrong and output will be an boolean 
def is_armstrong(num):
    return num == sum(int(digit) ** len(str(num)) for digit in str(num))

print(is_armstrong(153)) 

# a = 10
# b = 20
# print(a and b) output = 20
# print(a or b) output =  10

# if False:
#   print("It is False")
# else:
# print("It is True") output = it is true

# if [ ]:
# print("It is Blank")
# else:
# print("It is Something else") output = it is something else

# d. if [ [ ] ]:
# print("It is Blank")
# else:
# print("It is Something else") output = it is blank 

# e. if [ False ]:
# print("It is Blank")
# else:
# print("It is Something else")

# f. type(range) output = blank/nothing will display



# 4 Write a program to extract string elements from a list based on the conditions below.
# a. The first character must be lower and consonant.
# b. The string must not contain any number and also does not contain any special character.

def extract_string_ele(lst):
    return [ele for ele in lst if ele[0].islower() and ele[0]
            not in 'aeiou' and ele.isalpha() and ele.isalnum()]
lst = ['apple', 'banana', 'cherry', 'date', 'elderberry']
print(extract_string_ele(lst))


# 5 Write a program to create a list of numbers, and extract integer numbers from a list based on the
# below conditions.
# a. The number must be 4 digits long i.e (1000 to 9999)
# b. The second digit of the number must be odd and the last digit must be even.
# c. The number must be divisible by either 8 or 5.

def  extract_number(num):
      return [num for num in lst if isinstance(num, int) 
          and 1000 <= num <= 9999
          and num // 1000 % 2 != 0 and num % 2 == 0 
          and (num % 8 == 0 or num % 5 == 0)]

lst = [1001, 2002, 3003, 4004, 500]
print(extract_number(lst))



#6 program 

class Product:
    def __init__(self, name, costs):
        self.name = name
        self.costs = costs
        self.sales_prices = {}
        self.category = None

    def update_sale_price(self, month, percentage):
        if month in self.costs:
            self.sales_prices[month] = self.costs[month] * (1 + percentage/100)

    def set_category(self, category):
        self.category = category

    def get_max_min_price(self):
        if self.costs:
            max_cost = max(self.costs.values())
            min_cost = min(self.costs.values())
            max_month = [k for k, v in self.costs.items() if v == max_cost][0]
            min_month = [k for k, v in self.costs.items() if v == min_cost][0]
            return f"Product: {self.name}, Max Price: {max_cost} in {max_month}, Min Price: {min_cost} in {min_month}"
        else:
            return f"Product: {self.name}, No cost data available."


class Shelf:
    def __init__(self, name):
        self.name = name
        self.products = {}

    def add_product(self, product):
        self.products[product.name] = product

    def update_sale_price(self, month, percentage):
        for product in self.products.values():
            product.update_sale_price(month, percentage)

    def set_product_category(self, product_name, category):
        if product_name in self.products:
            self.products[product_name].set_category(category)

    def reset_cost_price(self, product_name, month):
        if product_name in self.products:
            if month in self.products[product_name].costs:
                self.products[product_name].costs[month] = 0

    def get_average_cost_sale_profit(self, month):
        if month in self.products[list(self.products.keys())[0]].costs:
            total_cost = 0
            total_sales = 0
            for product in self.products.values():
                if month in product.costs:
                    total_cost += product.costs[month]
                    if month in product.sales_prices:
                        total_sales += product.sales_prices[month]
            avg_cost = total_cost / len(self.products)
            avg_sale = total_sales / len(self.products)
            profit = total_sales - total_cost
            return f"Shelf: {self.name}, Avg Cost: {avg_cost:.2f}, Avg Sale: {avg_sale:.2f}, Profit: {profit:.2f}"
        else:
            return f"Shelf: {self.name}, No data for the specified month."


product1_shelf1 = Product("Product 1", {'January': [10, 30, 45, 50], 'February': [60, 6, 4, 68]})
product2_shelf1 = Product("Product 2", {'January': [66, 67, 81, 75], 'February': [78, 81, 85]})
product3_shelf1 = Product("Product 3", {'January': [18, 20], 'February': [21, 22], 'March': [22, 23, 24]})

product1_shelf2 = Product("Product 1", {'January': [206, 220, 225], 'March': [180, 170, 165], 'April': [160, 150, 136]})
product3_shelf2 = Product("Product 3", {})  # Empty costs for Product 3 in Shelf 2
product4_shelf2 = Product("Product 4", {'January': [300], 'February': [280], 'March': [300, 385], 'April': [360, 376]})
product6_shelf2 = Product("Product 6", {})  # Empty costs for Product 6 in Shelf 2

product2_shelf3 = Product("Product 2", {'March': [55, 59, 61], 'April': [53, 54, 55]})
product4_shelf3 = Product("Product 4", {})  # Empty costs for Product 4 in Shelf 3
product6_shelf3 = Product("Product 6", {})  # Empty costs for Product 6 in Shelf 3

# Create shelves
shelf1 = Shelf("SHELF-1")
shelf1.add_product(product1_shelf1)
shelf1.add_product(product2_shelf1)
shelf1.add_product(product3_shelf1)

shelf2 = Shelf("SHELF-2")
shelf2.add_product(product1_shelf2)
shelf2.add_product(product3_shelf2)
shelf2.add_product(product4_shelf2)
shelf2.add_product(product6_shelf2)

shelf3 = Shelf("SHELF-3")
shelf3.add_product(product2_shelf3)
shelf3.add_product(product4_shelf3)
shelf3.add_product(product6_shelf3)

# Calculate initial sale prices (example)
shelf1.update_sale_price('January', 20)  # For Product 1 and 2 in January
shelf1.update_sale_price('February', 30)  # For Product 1 and 2 in February
shelf1.update_sale_price('January', 35)  # For Product 3 in January
shelf1.update_sale_price('February', 40)  # For Product 3 in February
shelf1.update_sale_price('March', 50)  # For Product 3 in March

shelf2.update_sale_price('January', 10)  # For Product 1 and 4 in January
shelf2.update_sale_price('February', 10)  # For Product 1 and 4 in February
shelf2.update_sale_price('March', 15)  # For Product 1 and 4 in March
shelf2.update_sale_price('April', -10)  # For Product 1 in April
shelf2.update_sale_price('April', 10)  # For Product 4 in April

# Example usage
print(product1_shelf1.get_max_min_price())
print(shelf1.get_average_cost_sale_profit('January'))
print(shelf2.get_average_cost_sale_profit('March'))



