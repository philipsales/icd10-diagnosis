import pandas as pd


def main():
    pages = pd.read_csv('links.csv')
    all_pages = pages.drop_duplicates(subset=['pages','text'], keep='last')
    page_links = all_pages
    page_links.to_csv('new_links.csv', index=False, header=True)

if __name__ == "__main__":
    main()
