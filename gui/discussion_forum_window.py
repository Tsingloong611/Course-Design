import tkinter as tk
from forum import DiscussionForumLogic
from tools import *
import json


class DiscussionForumWindow:
    def __init__(self, root, course_id="3", name="student1", type="student"):
        self.name = name
        self.type = type
        self.forum_logic = DiscussionForumLogic()
        self.window = root
        self.window.title("讨论区")
        self.window.geometry("1000x1000")
        self.window.resizable(0, 0)

        self.path = f"./data/materials_data/{course_id}/topics.json"
        tools().check_file(self.path)

        self.topic_label = tk.Label(self.window, text="主题:")
        self.topic_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.topic_entry = tk.Entry(self.window, width=50)
        self.topic_entry.grid(row=0, column=1, padx=10, pady=10)

        self.content_label = tk.Label(self.window, text="内容:")
        self.content_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.write_content_text = tk.Text(self.window, width=60, height=20)
        self.write_content_text.grid(row=0, column=3, padx=10, pady=10)

        self.post_button = tk.Button(self.window, text="发布",
                                     command=lambda: self.forum_logic.post(path=self.path,
                                                                           poster=f"[{self.type}]{self.name} ",
                                                                           topic_entry=self.topic_entry,
                                                                           write_content_text=self.write_content_text))

        self.post_button.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.content_label = tk.Label(self.window, text="主题列表:")
        self.content_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.topic_listbox = tk.Listbox(self.window, width=100, height=20)
        self.topic_listbox.grid(row=2, column=1, columnspan=4, padx=10, pady=10)
        self.topic_listbox.bind("<<ListboxSelect>>", self.show_selected_topic)

        self.content_label = tk.Label(self.window, text="选中主题的内容:")
        self.content_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.content_text = tk.Text(self.window, width=60, height=20)
        self.content_text.grid(row=3, column=1, padx=10, pady=10)

        self.forum_logic.load_topics(path=self.path, topic_listbox=self.topic_listbox)

    def show_selected_topic(self, event):
        index = self.topic_listbox.curselection()[0]

        with open(self.path, "r") as file:
            topics = json.load(file)
            selected_topic = topics[index]

            content = selected_topic.get("content", "")

            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, content)


if __name__ == "__main__":
    root = tk.Tk()
    app = DiscussionForumWindow(root)
    root.mainloop()
