import tkinter as tk
from tkinter import ttk
import matplotlib
import requests
from datetime import datetime as dt
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('API - Cotação do dólar')

        # Criando uma figura
        self.figure = Figure(figsize=(15, 6), dpi=100)

        # Criando um objeto FigureCanvasTkAgg (Cria objeto para facilitar quando chama-lo para ser utilizado)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

        # Criando a barra de Ferramentas
        NavigationToolbar2Tk(self.figure_canvas, self)

        # Criando Gráfico
        self.chart = self.figure.add_subplot()

        self.current_value = tk.StringVar(value=10)
        self.cmdExecutar()

        # Mostrar o Gráfico
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.spinRange = ttk.Spinbox(
            self,
            from_=1,
            to=60,
            textvariable=self.current_value,
            wrap=True,
            font=("Arial 18 bold")
        )
        self.spinRange.pack(fill="x", side="left", expand=True, padx=5)

        # Botao para atualizar o gráfico
        ttk.Button(
            self, text="Atualizar",
            command=self.cmdExecutar
        ).pack(fill="x", side="left", expand=True, padx=5)

    def cmdExecutar(self):  # Criação da função do botão ATUALIZAR

        cotacoes = requests.get(f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{self.current_value.get()}")

        xData = []
        yData = []
        yVenda = []
        yMaxi = []
        yMini = []

        for x in cotacoes.json():
            ts = int(x['timestamp'])
            xEixo = dt.utcfromtimestamp(ts).strftime('%d/%m\n%Y')  # Para que a data fique 04/03/2023
            xData.insert(0, xEixo)  # Data no formato padrão adicionando no inicio posição 0
            yData.insert(0, float(x['bid']))  # Valor de Compra
            yVenda.insert(0, float(x['ask']))  # Valor de Venda
            yMaxi.insert(0, float(x['high']))  # Valor Máximo
            yMini.insert(0, float(x['low']))  # Valor Mínimo

        self.chart.clear()

        # Fazendo a label de lagenda e colocando as suas marcações
        self.chart.plot(xData, yData, marker='o', label='Compra')
        self.chart.plot(xData, yVenda, marker='*', label='Venda')
        self.chart.plot(xData, yMaxi, marker='p', label='Máximo')
        self.chart.plot(xData, yMini, marker='o', label='Mínimo')
        self.chart.set_xlabel('Datas')  # Eixo x com nome de DATAS
        self.chart.set_ylabel('BRL')
        self.chart.grid()
        self.chart.legend()

        self.figure_canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
