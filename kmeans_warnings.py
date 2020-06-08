#!/bin/python 3

# importing necessary modules
from tkinter import messagebox

# defining warnings used in the main script
class MyWarnings(object):
    def __init__(self, master, **kwargs):
        self.master = master

    def warning_callback_load(self):
        messagebox.showwarning("Warning", "The data have been already loaded.")

    def warning_callback_clear(self):
        messagebox.showwarning("Warning", "The charts have been already cleared.")

    def warning_callback_no_load(self):
        messagebox.showwarning("Warning", "The data are not loaded.")

    def warning_callback_no_charts_to_clear(self):
        messagebox.showwarning("Warning", "There are no charts to clear.")

    def warning_callback_the_kmeans_finished_running(self):
        messagebox.showwarning("Warning",
                               "K-means have already finished running on this data. If you want to have a new run, please"
                               " clear charts, load new data and run it again.")

    def warning_callback_no_charts_to_export(self):
        messagebox.showwarning("Warning", "There are no charts to export. Load data and run K-means first.")

    def warning_callback_no_pdf_to_export(self):
        messagebox.showwarning("Warning", "There are no pdf to export. Load data and run K-means first.")

    def warning_callback_bad_data(self):
        messagebox.showwarning("Warning", "Make sure that your data do not contain NaN values and check if all x values are in x"
                                          " column and all y values are in y column. Open SampleData.xlsx to compare your input with a required input.")

    def warning_callback_unsupported_filetype(self):
        messagebox.showwarning("Warning", "Unsupported format. Only *.xlsx, *.xls file are supported for loading.")

