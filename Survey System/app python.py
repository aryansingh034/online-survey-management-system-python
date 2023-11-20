import tkinter as tk
from tkinter import messagebox
import mysql.connector

class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey App")
        self.root.geometry("800x500")

        # Initialize the database connection and prepared statements
        self.initialize_database()

        main_panel = tk.Frame(root)
        main_panel.pack(expand=True, fill="both")

        text_panel = tk.Frame(main_panel)
        text_panel.pack(side="top")
        top_label = tk.Label(text_panel, text="Welcome to the Survey App", font=("Arial", 18, "bold"))
        top_label.pack()

        form_panel = tk.Frame(main_panel)
        form_panel.pack(expand=True, fill="both")

        # Configure row and column weights for centering
        for i in range(6):
            form_panel.grid_rowconfigure(i, weight=1)
            form_panel.grid_columnconfigure(i, weight=1)

        # Labels and Entries
        self.name_label = tk.Label(form_panel, text="Name:")
        self.name_label.grid(row=0, column=0, sticky='e')
        self.name_entry = tk.Entry(form_panel, width=30)
        self.name_entry.grid(row=0, column=1)

        self.email_label = tk.Label(form_panel, text="Email:")
        self.email_label.grid(row=1, column=0, sticky='e')
        self.email_entry = tk.Entry(form_panel, width=30)
        self.email_entry.grid(row=1, column=1)

        self.additional_label = tk.Label(form_panel, text="Where do you invest your Money?")
        self.additional_label.grid(row=2, column=0, sticky='e')
        self.additional_entry = tk.Entry(form_panel, width=30)
        self.additional_entry.grid(row=2, column=1)

        self.feedback_label = tk.Label(form_panel, text="Share your Experience with us:")
        self.feedback_label.grid(row=3, column=0, sticky='e')
        self.feedback_text = tk.Text(form_panel, height=10, width=30, wrap="word")
        self.feedback_text.grid(row=3, column=1)

        # Buttons
        self.submit_button = tk.Button(form_panel, text="Submit", command=self.submit_feedback)
        self.submit_button.grid(row=4, column=0, columnspan=2)

        self.update_button = tk.Button(form_panel, text="Update", command=self.update_feedback)
        self.update_button.grid(row=5, column=0, columnspan=2)

        self.exit_button = tk.Button(form_panel, text="Exit", command=root.quit)
        self.exit_button.grid(row=6, column=0, columnspan=2)

    def initialize_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Aryan@htc03",
                database="survey_db"
            )
            self.insert_query = "INSERT INTO feedback (name, email, additional_field, feedback) VALUES (%s, %s, %s, %s)"
            self.update_query = "UPDATE feedback SET additional_field = %s, feedback = %s WHERE name = %s AND email = %s"
        except mysql.connector.Error as err:
            print(f"Failed to connect to the database: {err}")
            messagebox.showerror("Error", "Failed to connect to the database.")

    def submit_feedback(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        additional_value = self.additional_entry.get()
        feedback = self.feedback_text.get("1.0", "end-1c")

        if not (name and email and additional_value and feedback):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(self.insert_query, (name, email, additional_value, feedback))
            self.connection.commit()
            messagebox.showinfo("Success", "Thank you for your feedback!")

            self.display_survey_details(name, email, additional_value, feedback)

            self.name_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.additional_entry.delete(0, "end")
            self.feedback_text.delete("1.0", "end")
        except mysql.connector.Error as err:
            print(f"Failed to submit feedback: {err}")
            messagebox.showerror("Error", "Failed to submit feedback.")
        finally:
            cursor.close()

    def update_feedback(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        additional_value = self.additional_entry.get()
        feedback = self.feedback_text.get("1.0", "end-1c")

        if not (name and email):
            messagebox.showerror("Error", "Name and Email are required for updating.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(self.update_query, (additional_value, feedback, name, email))
            self.connection.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Feedback updated successfully!")

                self.display_survey_details(name, email, additional_value, feedback)

                self.name_entry.delete(0, "end")
                self.email_entry.delete(0, "end")
                self.additional_entry.delete(0, "end")
                self.feedback_text.delete("1.0", "end")
            else:
                messagebox.showerror("Error", "No records updated. Please check the Name and Email.")
        except mysql.connector.Error as err:
            print(f"Failed to update feedback: {err}")
            messagebox.showerror("Error", "Failed to update feedback.")
        finally:
            cursor.close()

    def display_survey_details(self, name, email, additional_value, feedback):
        details_window = tk.Toplevel(self.root)
        details_window.title("Survey Details")
        details_window.geometry("400x300")

        details_panel = tk.Frame(details_window)
        details_panel.pack(expand=True, fill="both")

        details_text = tk.Text(details_panel, height=10, width=30, wrap="word")
        details_text.pack(expand=True, fill="both")
        details_text.insert("1.0", f"Name: {name}\n")
        details_text.insert("end-1c", f"Email: {email}\n")
        details_text.insert("end-1c", f"Where do you invest your Money? {additional_value}\n")
        details_text.insert("end-1c", f"Experience: {feedback}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()
