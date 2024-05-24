import json
import tkinter as tk

from dao.tools import tools


class DiscussionForumLogic:
    def __init__(self):
        """
        初始化话题
        """
        self.topics = []

    def post(self, **kwargs):
        """
        发布话题
        :param kwargs: 参数
        :return:
        """
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
        """
        加载话题
        :param path: 路径
        :param topic_listbox: 列表框
        :return:
        """
        self.path = path
        self.topic_listbox = topic_listbox
        self.topic_listbox.delete(0, tk.END)

        with open(self.path, "r") as file:
            self.topics = json.load(file)

            for topic_data in self.topics:
                topic = topic_data["topic"]
                self.topic_listbox.insert(tk.END, topic)

    def check_file(self, path):
        """
        检查文件是否存在,不存在则创建
        :param path: 路径
        :return:
        """
        tools().check_file(path)