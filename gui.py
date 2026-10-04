import tkinter as tk
from tkinter import ttk, messagebox
import scraper

print("SCRAPER FILE:", scraper.__file__)

import inspect
print("FUNCTION:", inspect.signature(scraper.scrape_products))


# Main window
root = tk.Tk()
root.title("E-Commerce Product Scraper")
root.geometry("900x600")
root.minsize(750, 500)


# Heading
title = tk.Label(
    root,
    text="🛒 E-Commerce Product Scraper",
    font=("Segoe UI", 22, "bold")
)

title.pack(pady=(20, 5))


subtitle = tk.Label(
    root,
    text="Extract product name, price and rating from an online store",
    font=("Segoe UI", 11)
)

subtitle.pack(pady=(0, 15))

# Website URL
url_frame = tk.Frame(root)
url_frame.pack(fill="x", padx=25, pady=5)

url_label = tk.Label(
    url_frame,
    text="Website URL:",
    font=("Segoe UI", 10, "bold")
)

url_label.pack(side="left", padx=(0, 10))

url_entry = tk.Entry(
    url_frame,
    font=("Segoe UI", 10)
)

url_entry.pack(
    side="left",
    fill="x",
    expand=True
)

url_entry.insert(
    0,
    "https://books.toscrape.com/"
)


# Status message
status = tk.Label(
    root,
    text="Ready to scrape products.",
    font=("Segoe UI", 10)
)

status.pack(pady=5)


# Table
columns = ("name", "price", "rating")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

table.heading("name", text="Product Name")
table.heading("price", text="Price")
table.heading("rating", text="Rating")

table.column("name", width=500)
table.column("price", width=150, anchor="center")
table.column("rating", width=150, anchor="center")

table.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


# Scrollbar
scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

scrollbar.place(
    relx=0.97,
    rely=0.17,
    relheight=0.65
)


# Scrape button
def scrape_data():

    try:

        status.config(text="🔄 Scraping products...")

        root.update()

        url = url_entry.get().strip()

        if not url:
            messagebox.showwarning(
                "Missing URL",
                "Please enter a website URL."
            )
            return

        products = scraper.scrape_products(url)

        # Clear old data
        for item in table.get_children():
            table.delete(item)

        # Add new data
        for product in products:

            table.insert(
                "",
                "end",
                values=(
                    product["name"],
                    product["price"],
                    product["rating"]
                )
            )

        scraper.save_to_csv(products)

        status.config(
            text=f"✅ Successfully extracted {len(products)} products."
        )

        messagebox.showinfo(
            "Success",
            f"{len(products)} products extracted successfully!\n\n"
            "Data has been saved to products.csv"
        )

    except Exception as error:

        status.config(
            text="❌ Failed to scrape products."
        )

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{error}"
        )


scrape_button = tk.Button(
    root,
    text="🔍 Scrape Products",
    command=scrape_data,
    font=("Segoe UI", 11, "bold"),
    padx=25,
    pady=10,
    cursor="hand2"
)

scrape_button.pack(pady=(5, 20))


# Start application
root.mainloop()