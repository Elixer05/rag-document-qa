import os
from langchain_community.document_loaders import PyPDFLoader
from sympy import re

def extract_metadata(text, curr_chapter, curr_section, curr_subsec):
    chapter_pattern = r"CHAPTER\s+([IVXLCDM\d]+)\s*[:\-–]?\s*(.+)?"
    section_pattern = r"(\d+\.\d+)\s+(.+)"
    subsection_pattern = r"(\d+\.\d+\.\d+)\s+(.+)"

    curr_chapter = re.search(chapter_pattern, text, re.IGNORECASE)
    if curr_chapter:
        curr_chapter = f"Chapter {curr_chapter.group(1)}"
    curr_subsection = re.search(subsection_pattern, text)
    if curr_subsection:
        curr_subsection=f"{curr_subsection.group(1)} {curr_subsection.group(2).strip()}"
    curr_section = re.search(section_pattern, text)
    if curr_section:
        curr_section=f"{curr_section.group(1)} {curr_section.group(2).strip()}"

    return curr_chapter, curr_section, curr_subsection


def loadPages(path):
    doc=[]
    for sub in os.listdir(path):
        sub_path=os.path.join(path,sub)
        if  not os.path.isdir(sub_path):
            continue
        for file in os.listdir(sub_path):
            if file.endswith('.pdf'):
                pdf_path=os.path.join(sub_path,file)
                loader = PyPDFLoader(pdf_path)
                curr_chapter = "Unknown"
                curr_section= "Unknown"
                curr_subsec= "Unknown"
                for page in loader.lazy_load():
                    chapter=extract_metadata(page.page_content, curr_chapter, curr_title, curr_section, curr_subsec)
                    if chapter:
                        curr_chapter, curr_title, curr_section, curr_subsec = chapter
                    page.metadata['chapter'] = curr_chapter
                    page.metadata['section'] = curr_section
                    page.metadata['subsection'] = curr_subsec
                    doc.extend([page])
    return doc