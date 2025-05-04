import csv
from BTrees.OOBTree import OOBTree
import timeit


def load_data(file_path):
    items = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append({
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            })
    return items


# Додавання товару до OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = item


# Додавання товару до словника
def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item


# Діапазонний запит для OOBTree
def range_query_tree(tree, min_price, max_price):
    return [item for _, item in tree.items() if min_price <= item["Price"] <= max_price]


# Діапазонний запит для словника
def range_query_dict(dictionary, min_price, max_price):
    # Лінійний пошук по значеннях словника
    return [item for item in dictionary.values() if min_price <= item["Price"] <= max_price]


def main():
    file_path = "generated_items_data.csv"
    items = load_data(file_path)

    tree = OOBTree()
    dictionary = {}

    # Додавання товарів до обох структур
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначення діапазону цін для запитів
    min_price = 50
    max_price = 150

    # Вимірювання часу для OOBTree
    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price),
        number=100
    )

    # Вимірювання часу для словника
    dict_time = timeit.timeit(
        lambda: range_query_dict(dictionary, min_price, max_price),
        number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")


if __name__ == "__main__":
    main()
