import csv
import os

# Filepath for the CSV file
CSV_FILE = "comments.csv"

# Fields in the CSV file
FIELDS = ["username", "postshortcode", "comment_id", "comment", "comment_likes_count", "comment_time"]

# Ensure the CSV file exists
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()

# Create or update a comment by comment_id
def create_or_update_comment(data):
    comments = read_comments()
    updated = False
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for comment in comments:
            if comment["comment_id"] == data["comment_id"]:
                comment.update(data)
                updated = True
            writer.writerow(comment)
        if not updated:
            writer.writerow(data)
            print("Comment added successfully.")
        else:
            print("Comment updated successfully.")

# Read all comments
def read_comments():
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Delete a comment by comment_id
def delete_comment(comment_id):
    comments = read_comments()
    initial_length = len(comments)
    comments = [comment for comment in comments if comment["comment_id"] != comment_id]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(comments)
    if len(comments) < initial_length:
        print("Comment deleted successfully.")
    else:
        print("Comment not found.")

# Example usage
# if __name__ == "__main__":
#     initialize_csv()

#     while True:
#         print("\nComment CRUD Operations:")
#         print("1. Create or Update Comment")
#         print("2. Read Comments")
#         print("3. Delete Comment")
#         print("4. Exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             data = {
#                 "username": input("Enter username: "),
#                 "postshortcode": input("Enter post shortcode: "),
#                 "comment_id": input("Enter comment ID: "),
#                 "comment": input("Enter comment text: "),
#                 "comment_likes_count": input("Enter comment likes count: "),
#                 "comment_time": input("Enter comment time: ")
#             }
#             create_or_update_comment(data)

#         elif choice == "2":
#             comments = read_comments()
#             for comment in comments:
#                 print(comment)

#         elif choice == "3":
#             comment_id = input("Enter comment ID to delete: ")
#             delete_comment(comment_id)

#         elif choice == "4":
#             print("Exiting...")
#             break

#         else:
#             print("Invalid choice. Please try again.")