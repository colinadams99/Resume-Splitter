# Package import
import os
import re
import csv
from PyPDF2 import PdfReader, PdfWriter

# Grabs the bookmarks (table of contents values) from PDF
def get_bookmarks(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        outlines = reader.get_outlines()
        return parse_outlines(outlines)

# Parses the bookmark values and returns them
def parse_outlines(outlines, level=0):
    bookmarks = []
    for outline in outlines:
        if isinstance(outline, list):
            bookmarks.extend(parse_outlines(outline, level + 1))
        else:
            bookmarks.append(outline.title)
    return bookmarks

# Extracts the text from the pdf
def extract_text_from_page(pdf_path, page_number):
    reader = PdfReader(pdf_path)
    page = reader.pages[page_number]
    text = page.extract_text()
    return text

# Function to save the used bookmarks as a CSV
def save_bookmarks_to_csv(bookmarks, csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Bookmark Name', 'File Name'])
        writer.writerows(bookmarks)
    print(f"CSV file saved at {csv_path}")

# Cleans the file name 
def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '', name).replace('\n', '').replace('\r', '')

# Removes dulicated names in instance of wrongly inputted bookmark values
def remove_first_instance_of_duplicates(bookmarks):
    seen = set()
    to_remove = set()
    for bookmark in bookmarks:
        bookmark_lower = bookmark.lower()
        if bookmark_lower in seen:
            to_remove.add(bookmark_lower)
        seen.add(bookmark_lower)
    
    processed_bookmarks = []
    seen = set()
    for bookmark in bookmarks:
        bookmark_lower = bookmark.lower()
        if bookmark_lower in to_remove:
            if bookmark_lower not in seen:
                seen.add(bookmark_lower)
                continue
        processed_bookmarks.append(bookmark)
    
    return processed_bookmarks

'''# Regex to find if a bookmark is missing
def find_missing_bookmarks(bookmarks, total_pages):
    bookmark_pages = [int(re.search(r'(\d+)', bm).group()) for bm in bookmarks if re.search(r'(\d+)', bm)]
    missing_pages = []

    for i in range(1, total_pages + 1):
        if i not in bookmark_pages:
            missing_pages.append(i)
    
    return missing_pages'''

# Function to manually move another bookmark to another location if misplaced
def realign_bookmarks(bookmarks, adjustments):
    for incorrect_index, correct_index in adjustments.items():
        bookmarks.insert(correct_index, bookmarks.pop(incorrect_index))
    return bookmarks

# Fxn to manually add any missing bookmarks
def add_missing_bookmark(bookmarks, missing_bookmark_name, insert_index):
    bookmarks.insert(insert_index, missing_bookmark_name)
    return bookmarks
  
