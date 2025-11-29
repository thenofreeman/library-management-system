import csv

def read_borrowers():
    borrowers_data = [['Card_id', 'Ssn', 'Bname', 'Address', 'Phone']]

    with open('data/borrower.csv', 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file))
        header = rows[0]

        for row in rows[1:]:
            [idn, ssn, fname, lname, email, addr, city, state, phone] = row
            full_name = f'{fname} {lname}'
            address = f'{addr}, {city}, {state}'

            new_borrower = [int(idn[2:]), ssn, full_name, address, phone]
            borrowers_data.append(new_borrower)

    return borrowers_data

def read_books():
    books_data = [['Isbn', 'Title']]
    authors_data = [['Author_id', 'Name']]
    book_authors_data = [['Author_id', 'Isbn']]

    with open('data/book.csv', 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file, delimiter='\t'))
        header = rows[0]

        author_id_incr = 0
        author_set = dict()

        for row in rows[1:]:
            [isbn10, isbn13, title, authors, cover, pub, pages] = row

            new_book = [isbn10, title]
            books_data.append(new_book)

            for author in authors.split(','):
                author = author.strip()

                if author == '':
                    author = 'Unknown Author'

                if author not in author_set:
                    author_set[author] = author_id_incr
                    author_id_incr += 1

                new_book_author = [author_set[author], isbn10]
                book_authors_data.append(new_book_author)

        for (name, author_id) in author_set.items():
            new_author = [author_id, name]
            authors_data.append(new_author)

    return (books_data, book_authors_data, authors_data)

def write_to_csv(list_of_lists, filename):
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter='|')

        writer.writerows(list_of_lists)

    # previous usage:
    # write_to_csv(borrowers, 'borrower.csv')
    # write_to_csv(books, 'book.csv')
    # write_to_csv(book_authors, 'book_authors.csv')
    # write_to_csv(authors, 'authors.csv')
