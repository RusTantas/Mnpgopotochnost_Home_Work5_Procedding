"""Моделирование программы для управления данными о движении товаров на складе и эффективной обработки запросов на обновление информации в многопользовательской среде.

Представим, что у вас есть система управления складом, где каждую минуту поступают запросы на обновление информации о поступлении товаров и отгрузке товаров.
Наша задача заключается в разработке программы, которая будет эффективно обрабатывать эти запросы в многопользовательской среде, с использованием механизма мультипроцессорности для обеспечения быстрой реакции на поступающие данные.

Создайте класс WarehouseManager - менеджера склада, который будет обладать следующими свойствами:
Атрибут data - словарь, где ключ - название продукта, а значение - его кол-во. (изначально пустой)
Метод process_request - реализует запрос (действие с товаром), принимая request - кортеж.
Есть 2 действия: receipt - получение, shipment - отгрузка.
а) В случае получения данные должны поступить в data (добавить пару, если её не было и изменить значение ключа, если позиция уже была в словаре)
б) В случае отгрузки данные товара должны уменьшаться (если товар есть в data и если товара больше чем 0).

3.Метод run - принимает запросы и создаёт для каждого свой параллельный процесс, запускает его(start) и замораживает(join).
"""

from multiprocessing import Process, Manager


class WarehouseManager:

    def __init__(self):
        # super().__init__(*args, **kwargs)
        self.product = Manager().dict()

    def process_request(self, request):
        product1, action, amuont = request
        if action == 'receipt':
            if product1 in self.product:
                self.product[product1] += amuont
            else:
                self.product[product1] = amuont
        elif action == 'shipment':
            if product1 in self.product and self.product[product1] >= amuont:
                self.product[product1] -= amuont

    def run(self, request):
        processes = []
        for i in request:
            process = Process(target=self.process_request, args=(i, ))
            processes.append(process)
            process.start()
        for j in processes:
            j.join()
if __name__ == '__main__':
    ff = WarehouseManager()
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    ff.run(requests)
    print(dict(ff.product))