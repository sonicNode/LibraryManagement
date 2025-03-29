import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to process the Excel file
def process_xls(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.fillna("Unknown", inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

# Function to analyze and generate recommendations
def recommend_books(df, user_id):
    user_books = df.groupby('card_number')['title'].apply(set).to_dict()
    if user_id not in user_books:
        return [], df['title'].value_counts().head(5).index.tolist()
    
    books = user_books[user_id]
    recommendations = set()
    for u, bks in user_books.items():
        if u != user_id and books & bks:
            recommendations.update(bks - books)
    
    return sorted(recommendations)[:5], df['title'].value_counts().head(5).index.tolist()

# Function to visualize data
def show_graph(user_recommendations, popular_books):
    labels = ['User Recommendations', 'Most Popular Books']
    sizes = [len(user_recommendations), len(popular_books)]
    colors = ['#ff9999','#66b3ff']
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.axis('equal')  
    plt.title("Book Recommendation Analysis")
    plt.show()

# GUI for file selection and user input
def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xls;*.xlsx")])
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return
    
    df = process_xls(file_path)
    user_id = tk.simpledialog.askstring("Input", "Enter your user ID (card number):")
    
    if not user_id:
        messagebox.showerror("Error", "No user ID entered.")
        return
    
    user_recommendations, popular_books = recommend_books(df, user_id)
    
    messagebox.showinfo("Recommendations", f"User-Based Recommendations:\n" + "\n".join(user_recommendations) + "\n\nMost Popular Books:\n" + "\n".join(popular_books))
    show_graph(user_recommendations, popular_books)

if __name__ == "__main__":
    main()
