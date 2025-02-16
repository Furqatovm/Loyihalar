import os
from slugify import slugify

class Article:
    def __init__(self, title):
        self.title =title
        self.content = ""
    @property
    def slug(self):
        return slugify(self.title)
    

    def load_content(self):
        with open(f"articles/{self.title}.md", "r") as file:
            self.content = file.read()
    @classmethod
    def all(cls):
        titles = os.listdir("articles")
        slug_articles = {}
        for title in titles:
            title = title.replace(".md", "")
            slug =slugify(title)
            Article =cls(title)
            Article.load_content()
            slug_articles[slug] =Article
        return slug_articles


