import tkinter as tk
from tkinter import messagebox

class WebsiteBlockerGUI:
    def __init__(self):
        self.site_block = []
        self.host_path = "C:/Windows/System32/drivers/etc/hosts"
        self.redirect = "127.0.0.1"

        self.root = tk.Tk()
        self.root.title("Website Blocker")
        self.root.geometry("400x300")

        self.entry_label = tk.Label(self.root, text="Enter website:", font=("Helvetica", 12))
        self.entry_label.pack(pady=(15, 5))

        self.website_entry = tk.Entry(self.root, width=30, font=("Helvetica", 10))
        self.website_entry.pack(pady=(0, 15))

        self.block_button = tk.Button(self.root, text="Block Website", command=self.block_website, font=("Helvetica", 10), bg="#4CAF50", fg="white")
        self.block_button.pack(pady=(0, 15))

        self.website_listbox_label = tk.Label(self.root, text="Blocked Websites:", font=("Helvetica", 12))
        self.website_listbox_label.pack(pady=(15, 5))

        self.website_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, font=("Helvetica", 10))
        self.website_listbox.pack(pady=(0, 15))

        self.unblock_button = tk.Button(self.root, text="Unblock Selected", command=self.unblock_website, font=("Helvetica", 10), bg="#FF6347", fg="white")
        self.unblock_button.pack(pady=(0, 15))

        # Populate initial blocked websites
        self.update_website_listbox()

    def block_website(self):
        website = self.website_entry.get().strip()
        if website:
            if website not in self.site_block:
                self.site_block.append(website)
                with open(self.host_path, "r+") as host_file:
                    content = host_file.read()
                    if website not in content:
                        host_file.write(self.redirect + " " + website + "\n")
                self.update_website_listbox()
            else:
                messagebox.showinfo("Info", f"{website} is already blocked.")
        else:
            messagebox.showwarning("Warning", "Please enter a website.")

    def unblock_website(self):
        selected_index = self.website_listbox.curselection()
        if selected_index:
            selected_website = self.site_block[selected_index[0]]
            with open(self.host_path, "r+") as host_file:
                content = host_file.readlines()
                host_file.seek(0)
                for line in content:
                    if not any(selected_website in line for website in self.site_block):
                        host_file.write(line)
                host_file.truncate()
            self.site_block.remove(selected_website)
            self.update_website_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a website to unblock.")

    def update_website_listbox(self):
        self.website_listbox.delete(0, tk.END)
        self.site_block = []  # Clear the list before updating
        with open(self.host_path, "r") as host_file:
            for line in host_file:
                if line.startswith(self.redirect):
                    website = line.split()[1]
                    self.site_block.append(website)
                    self.website_listbox.insert(tk.END, website)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    website_blocker = WebsiteBlockerGUI()
    website_blocker.run()
