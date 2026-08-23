class CategoryService:
    def __init__(self, categories, products):
        self.categories = categories
        self.products = products

    def get_all(self):
        return self.categories

    def find_by_id(self, category_id):
        for category in self.categories:
            if category["id"] == category_id:
                return category
        return None

    def get_next_id(self):
        max_id = 0

        for category in self.categories:
            if category["id"] > max_id:
                max_id = category["id"]
        return max_id + 1

    def name_exists(self, category_name):
        for category in self.categories:
            if category["name"].lower() == category_name.lower():
                return True
        return False

    def create(self, category_data):
        new_category = {
            "id": self.get_next_id(),
            "name": category_data.name
        }

        self.categories.append(new_category)

        return new_category

    def delete(self, category):
        self.categories.remove(category)
        return category

    def is_used(self, category_name):
        for product in self.products:
            if product["category"].lower() == category_name.lower():
                return True
        return False