from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_books():
    with open('json/books_description.json', 'r', encoding='utf-8') as books_file:
        books_description = json.load(books_file)
        return books_description


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    books = load_books()
    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()