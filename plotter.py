import matplotlib.pyplot as plt
from io import BytesIO

class PlotManager:
    def __init__(self, db):
        self.db = db

    def generate_price_graph(self, item_id):
        price_history = self.db.get_price_history(item_id)
        plt.plot(price_history)
        plt.xlabel('Время')
        plt.ylabel('Цена')
        plt.title(f'Динамика цен для товара ID {item_id}')

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        return image_stream