class ProductService:
    def __init__(self, products, categories):
        self.products = products
        self.categories = categories

    def get_all(self, category = None, available = None, min_price = None, max_price = None, name = None):
        filtered_products = []

        for product in self.products:
            if category is not None:
                if product["category"].lower() != category.lwoer():
                    continue
            if available is not None:
                if product["available"] != available:
                    continue
            if min_price is not None:
                if product["price"] < min_price:
                    continue
            if max_price is not None:
                if product["price"] > max_price:
                    continue
            if name is not None:
                if name.lower() not in product["name"].lower():
                    continue
            filtered_products.append(product)
        return filtered_products

    def find_by_id(self, product_id):
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    def get_next_id(self):
        max_id = 0

        for product in self.products:
            if product["id"] > max_id:
                max_id = product["id"]
        return max_id + 1

    def category_exists(self, category_name):
        for category in self.categories:
            if(category["name"].lower() == category_name.lower()):
                return True
        return False

    def name_exists(self, product_name, excluded_id=None):
        for product in self.products:
            if product["name"].lower() == product_name.lower():
                if excluded_id is None:
                    return True
                if product["id"] != excluded_id:
                    return True
        return False

    def create(self, product_data):
        new_product = {
            "id": self.get_next_id(),
            "name": product_data.name,
            "description": product_data.description,
            "price": product_data.price,
            "category": product_data.category,
            "available": product_data.available
        }

        self.products.append(new_product)

        return new_product

    def update(self, product, product_data):
        product["name"] = product_data.name
        product["description"] = product_data.description
        product["price"] = product_data.price
        product["category"] = product_data.category.lower()
        product["available"] = product_data.available

        return product

    def patch(self, product, updates):
        for key in updates:
            product[key] = updates[key]
        return product

    def delete(self, product):
        self.products.remove(product)
        return product