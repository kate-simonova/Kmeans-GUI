#!/bin/env/python 3

# importing tkinter-related packages
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# importing basic ML packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# importing warnings
from OOP.L4.kmeans_warnings import MyWarnings # please change this line to your folder

# importing other modules
import operator
from fpdf import FPDF
import tempfile
from datetime import date
import xlrd

# defining a class
class App(object):
    def __init__(self, master, **kwargs):
        self.master = master

    # Variables used for this project
    get_excel_var = 0
    get_kmeans_var = 0
    clear_charts_var = 0
    export_charts_var = 0

    # defining main functions used for this project
    def getExcel(self):
        '''
        load excel file into the program
        :return: dataframe
        '''
        global df
        global get_excel_var
        if self.get_excel_var == 0:
            try:
                import_file_path = filedialog.askopenfilename(filetypes=(("excel files", ("*.xlsx", "*.xls")), ("all files", "*.*")))
                read_file = pd.read_excel(import_file_path)
                df = pd.DataFrame(read_file, columns=['x', 'y'])
                self.get_excel_var += 1
            except xlrd.biffh.XLRDError:
                MyWarnings.warning_callback_unsupported_filetype(self)
        else:
            MyWarnings.warning_callback_load(self)

    # getting the number of clusters by Sihoulette method
    def get_k_sihouette(self):
        '''
        Calculates k based on sihouette score
        :return: optimal k
        '''
        s = {}
        K = range(2, 20)
        for k in K:
            kmeanModel = KMeans(n_clusters=k, random_state=0).fit(df)
            labels = kmeanModel.fit_predict(df)
            s[k] = silhouette_score(df, labels)
        return max(s.items(), key=operator.itemgetter(1))[0]

    # getting the number of clusters by GapStatic method
    def get_k_gap_statistic(self):
        """
        Calculates KMeans optimal K using Gap Statistic from Tibshirani, Walther, Hastie
        :return: optimal K
        """
        self.gaps = np.zeros((len(range(1, 20)),))
        self.nrefs = 3
        resultsdf = pd.DataFrame({'clusterCount': [], 'gap': []})
        for gap_index, k in enumerate(range(1, 20)):
            # Holder for reference dispersion results
            refDisps = np.zeros(self.nrefs)
            # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
            for i in range(self.nrefs):
                # Create new random reference set
                randomReference = np.random.random_sample(size=df.shape)
                # Fit to it
                km = KMeans(k)
                km.fit(randomReference)
                refDisp = km.inertia_
                refDisps[i] = refDisp
            # Fit cluster to original data and create dispersion
            km = KMeans(k)
            km.fit(df)
            origDisp = km.inertia_
            # Calculate gap statistic
            gap = np.log(np.mean(refDisps)) - np.log(origDisp)
            # Assign this loop's gap statistic to gaps
            self.gaps[gap_index] = gap
            resultsdf = resultsdf.append({'clusterCount': k, 'gap': gap}, ignore_index=True)
        return self.gaps.argmax() + 1  # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal

    # creating a function to apply Kmeans
    def getKMeans(self):
        '''
        Create visualization of your data and marks clusters with red
        :return: charts and conclusion
        '''
        global df
        global scatter1
        global scatter2
        global numberOfClusters
        global numberOfClusters2
        global figure1
        global figure2
        window.geometry("800x650")
        # with sihouette method
        if self.get_kmeans_var == 0:
            if self.get_excel_var == 1:
                try:
                    numberOfClusters = App.get_k_sihouette(self)
                    kmeans = KMeans(n_clusters=numberOfClusters).fit(df)
                    centroids = kmeans.cluster_centers_

                    figure1 = plt.Figure(figsize=(4, 3), dpi=100)
                    ax1 = figure1.add_subplot()
                    ax1.scatter(df['x'], df['y'], c=kmeans.labels_.astype(int), s=50, alpha=0.5)
                    ax1.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
                    ax1.set_title('Silhouette analysis')
                    scatter1 = FigureCanvasTkAgg(figure1, canvas2)
                    scatter1.get_tk_widget().pack(side=tk.LEFT)

                    # with Gap Statistic method
                    numberOfClusters2 = App.get_k_gap_statistic(self)\
                    kmeans = KMeans(n_clusters=numberOfClusters2).fit(df)
                    centroids = kmeans.cluster_centers_

                    figure2 = plt.Figure(figsize=(4, 3), dpi=100)
                    ax1 = figure2.add_subplot()
                    ax1.scatter(df['x'], df['y'], c=kmeans.labels_.astype(int), s=50, alpha=0.5)
                    ax1.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
                    ax1.set_title('Gap Statistic Analysis')
                    scatter2 = FigureCanvasTkAgg(figure2, canvas2)
                    scatter2.get_tk_widget().pack(side=tk.RIGHT)
                    obj = str(numberOfClusters)
                    obj2 = str(numberOfClusters2)
                    canvas3.create_text(250, 20, fill="black", font=('Arial', 12, 'bold'), text="Conclusion")
                    canvas3.create_text(250, 50, fill="black", font=('Arial', 12),
                                        text='The number of clusters determined by Sihouette Analysis is ' + obj + '.\nThe number of clusters determined by Gap Statistic Analysis is ' + obj2 + '.')
                    self.clear_charts_var = 1
                    self.export_charts_var = 1
                    self.get_kmeans_var += 1
                except ValueError:
                    window.geometry("800x300")
                    MyWarnings.warning_callback_bad_data(self)
            else:
                window.geometry("800x300")
                MyWarnings.warning_callback_no_load(self)
        else:
            MyWarnings.warning_callback_the_kmeans_finished_running(self)

    # clearing charts
    def clear_charts(self):
        if self.clear_charts_var == 0:
            MyWarnings.warning_callback_no_charts_to_clear(self)
        else:
            scatter1.get_tk_widget().pack_forget()
            scatter2.get_tk_widget().pack_forget()
            canvas1.delete()
            canvas2.delete()
            canvas3.delete('all')
            window.geometry("800x300")
            self.clear_charts_var = 0
            self.get_excel_var = 0
            self.get_kmeans_var = 0
            self.export_charts_var = 0

    # exporting data to jpg
    def export_to_jpg(self):
        if self.export_charts_var == 1:
            figure1.savefig(f'Sihouette_{date.today()}.jpg', dpi=200)
            figure2.savefig(f'GapStatistic_{date.today()}.jpg', dpi=200)
        else:
            MyWarnings.warning_callback_no_charts_to_export(self)

    # exporting data to pdf
    def export_to_pdf(self):
        if self.export_charts_var == 1:
            figure1.savefig('chart1.png', dpi=100)
            figure2.savefig('chart2.png', dpi=100)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_xy(0, 0)
            pdf.set_font('arial', 'B', 12)
            pdf.cell(60)
            pdf.cell(75, 20, "A Graphical Report of K-Means Clustering Calculator", 0, 2, 'C')
            pdf.set_font('arial', '', 11)
            pdf.cell(75, 20, 'The number of clusters determined by Sihouette Analysis is ' + str(numberOfClusters) + '.', 0,
                     2, 'C')
            pdf.cell(-30)
            pdf.image('chart1.png', x=None, y=None, w=0, h=0, type='', link='')
            pdf.cell(30)
            pdf.cell(75, 20,
                     'The number of clusters determined by Gap Statistic Analysis is ' + str(numberOfClusters2) + '.',
                     0, 2, 'C')
            pdf.cell(-30)
            pdf.image('chart2.png', x=None, y=None, w=0, h=0, type='', link='')
            pdf.output('KMeansClusterCalculatorReport.pdf', 'F')
        else:
            MyWarnings.warning_callback_no_pdf_to_export(self)

    about_text = "K-Means Clustering Calculator allows to apply different analysis " \
                 "to the data in order to determine the optimal number of clusters for k-Means analysis. " \
                 "Load your standardized data having 'x' and 'y' in A1 and B1 positions of an excel file. \n\n\n Version 0.0.1"
    about_header = 'About K-Means Clustering Calculator'

    def about(self):
        self.about = tk.Toplevel(window, padx=40, pady=40)
        self.about.title(self.about_header)
        msg = Message(self.about, anchor=CENTER, text=self.about_text)
        msg.pack()

    help_text = 'If you have some issues with a program you can contact me on Github via https://github.com/kate-simonova' \
                'or via email on simonek1@fit.cvut.cz'

    def help(self):
        self.help_menu = tk.Toplevel(window, padx=40, pady=40)
        self.help_menu.title('Help')
        msg2 = Message(self.help_menu, anchor=CENTER, text=self.help_text)
        msg2.pack()

# starting point
window = tk.Tk()
window.geometry("800x350")
window.title('K-Means Clustering Calculator')
app = App(window)

# making Tkinter icon invisible
ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

window.iconbitmap(default=ICON_PATH)

# creating a GUI screen where I can place all items
canvas1 = tk.Canvas(window, width = 800, height = 250)
canvas1.pack()

canvas2 = tk.Canvas(window, width = 800, height = 200)
canvas2.pack()

canvas3 = tk.Canvas(window, width = 800, height = 100)
canvas3.pack()

# creating a label of the program
label1 = tk.Label(window, text='K-Means Clustering Calculator')
label1.config(font=('Arial', 20, 'bold'))
canvas1.create_window(370, 30, window=label1)

# creating a button to load an excel file
button1 = tk.Button(window, text='Load Excel File',command=app.getExcel, bg='palegreen2', font=('Arial', 11, 'bold'))
canvas1.create_window(650, 100, window=button1)

# creating a button to start K-means
button2 = tk.Button(window, text=' Run  k-Means ',command=app.getKMeans, bg='brown', fg='white', font=('Arial', 11, 'bold'))
canvas1.create_window(650, 150, window=button2)

# creating a button to clear created charts
button3 = tk.Button(window, text=' Clear  Charts ', command=app.clear_charts, bg='black', fg='white', font=('Arial', 11, 'bold'))
canvas1.create_window(650, 200, window=button3)

# creating a menu
menubar = tk.Menu(window)

menu_file = tk.Menu(menubar, tearoff = 0)
menu_file.add_command(label="Load Excel File", command = app.getExcel)
menu_file.add_command(label="Run k-Means", command = app.getKMeans)
menu_file.add_command(label="Clear charts", command = app.clear_charts)
menu_file.add_command(label="Export graphs to pdf", command = app.export_to_pdf)
menu_file.add_command(label="Export graphs to jpg", command = app.export_to_jpg)
menu_file.add_command(label="Exit", command = window.destroy)

menubar.add_cascade(label = "File", menu = menu_file)

# creating radiobuttons
menu_help = tk.Menu(menubar, tearoff = 0)
menuRadioVar1 = tk.IntVar()
menu_help.add_radiobutton(label="Help", val=1, variable = menuRadioVar1, command = app.help)
menu_help.add_radiobutton(label="About", val=2, variable = menuRadioVar1, command = app.about)
menubar.add_cascade(label = "Options", menu = menu_help)

# creating a text with the description of the program
canvas1.create_text(260,100, fill="black",font=('Arial', 12, 'bold'), text= 'About the program')
canvas1.create_text(260,170, fill="black",font=('Arial', 12),
                        text="Welcome to the K-Means Clustering Calculator! \nThis programs allows to apply different analysis "
                             "to \n the data in order to determine the optimal number \n of clusters for k-Means analysis. "
                             "Load your \n standardized data having 'x' and 'y' in A1 and B1 \n positions of an excel file. ")

# creating a rectangle around text
rect = canvas1.create_rectangle(465, 250, 50, 80, outline='black', fill="" )

window.config(menu = menubar)
window.mainloop()
