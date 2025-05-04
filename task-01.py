import networkx as nx
import pandas as pd

# Побудова орієнтованого графа
G = nx.DiGraph()

# Вхідні дані: ребра та пропускні здатності
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо ребра до графу
for u, v, capacity in edges:
    G.add_edge(u, v, capacity=capacity)

# Додаємо джерело і стік
G.add_edge("Джерело", "Термінал 1", capacity=float("inf"))
G.add_edge("Джерело", "Термінал 2", capacity=float("inf"))

for i in range(1, 15):
    G.add_edge(f"Магазин {i}", "Стік", capacity=float("inf"))

# Обчислення максимального потоку
flow_value, flow_dict = nx.maximum_flow(G, "Джерело", "Стік", flow_func=nx.algorithms.flow.edmonds_karp)

# Побудова таблиці потоків
records = []
terminals = ["Термінал 1", "Термінал 2"]

for terminal in terminals:
    for warehouse, flow_to_warehouse in flow_dict[terminal].items():
        if flow_to_warehouse > 0:
            for shop, flow_to_shop in flow_dict[warehouse].items():
                if flow_to_shop > 0:
                    records.append({
                        "Термінал": terminal,
                        "Магазин": shop,
                        "Фактичний Потік (одиниць)": flow_to_shop
                    })

flow_table = pd.DataFrame(records)

# Зведення
terminal_totals = flow_table.groupby("Термінал")["Фактичний Потік (одиниць)"].sum().reset_index(name="Загальний потік")
shop_totals = flow_table.groupby("Магазин")["Фактичний Потік (одиниць)"].sum().reset_index(name="Отримано товару")

# Вивід результатів
print(f"Максимальний потік: {flow_value}")
print("\nТаблиця потоків:")
print(flow_table.to_string(index=False))
print("\nПотік за терміналами:")
print(terminal_totals.to_string(index=False))
print("\nПоставка за магазинами:")
print(shop_totals.to_string(index=False))
