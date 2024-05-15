import json
import tkinter as tk

from dao.tools import tools


class DiscussionForumLogic:
    def __init__(self):
        self.topics = []

    def post(self, **kwargs):
        self.poster = kwargs.get("poster")
        self.topic_entry = kwargs.get("topic_entry")
        self.write_content_text = kwargs.get("write_content_text")
        self.path = kwargs.get("path")
        topic = self.topic_entry.get()
        content = self.write_content_text.get("1.0", tk.END)

        self.topics.append({"topic": self.poster + "发布了 " + topic, "content": content})

        with open(self.path, "w") as file:
            json.dump(self.topics, file)

        self.load_topics(path=self.path, topic_listbox=self.topic_listbox)

    def load_topics(self, path, topic_listbox):
        self.path = path
        self.topic_listbox = topic_listbox
        self.topic_listbox.delete(0, tk.END)

        with open(self.path, "r") as file:
            self.topics = json.load(file)

            for topic_data in self.topics:
                topic = topic_data["topic"]
                self.topic_listbox.insert(tk.END, topic)

    def check_file(self, path):
        tools().check_file(path)