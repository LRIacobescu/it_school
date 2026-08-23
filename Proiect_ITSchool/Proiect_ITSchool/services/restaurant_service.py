class RestaurantService:
    def __init__(self, restaurants):
        self.restaurants = restaurants

    def get_all(self, city=None, is_open=None):
        results = self.restaurants

        if city is not None:
            results = [r for r in results if r["city"].lower() == city.lower()]

        if is_open is not None:
            results = [r for r in results if r["is_open"] == is_open]

        return results

    def find_by_id(self, restaurant_id: int):
        for r in self.restaurants:
            if r["id"] == restaurant_id:
                return r
        return None

    def get_next_id(self):
        if len(self.restaurants) == 0:
            return 1
        return max(r["id"] for r in self.restaurants) + 1

    def name_exists_in_city(self, name: str, city: str, exclude_id: int = None):
        for r in self.restaurants:
            if r["name"].lower() == name.lower() and r["city"].lower() == city.lower():
                if exclude_id is None or r["id"] != exclude_id:
                    return True
        return False

    def create(self, restaurant_data):
        new_restaurant = {
            "id": self.get_next_id(),
            "name": restaurant_data.name,
            "city": restaurant_data.city,
            "rating": restaurant_data.rating,
            "is_open": restaurant_data.is_open
        }
        self.restaurants.append(new_restaurant)
        return new_restaurant

    def update(self, restaurant, updated_data):
        restaurant["name"] = updated_data.name
        restaurant["city"] = updated_data.city
        restaurant["rating"] = updated_data.rating
        restaurant["is_open"] = updated_data.is_open
        return restaurant

    def patch(self, restaurant, updates: dict):
        for key, value in updates.items():
            restaurant[key] = value
        return restaurant

    def delete(self, restaurant):
        self.restaurants.remove(restaurant)
        return restaurant