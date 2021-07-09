import json
import math
import os
from livereload import Server
from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_books_description():
    with open('json/books_description.json', 'r', encoding='utf-8') as file:
        books_description = json.load(file)
        return books_description


def on_reload():
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books = read_books_description()
    books_per_page = 20
    pages = range(1, math.ceil(len(books) / books_per_page) + 1)
    for page_number, books_stack in enumerate(chunked(books, books_per_page), start=1):
        rendered_page = template.render(
            books=books_stack,
            pages=pages,
            current_page=page_number
        )
        page_name = os.path.join(folder, f'index{page_number}.html')
        with open(page_name, 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
