import os
import re
from langchain_community.document_loaders import PyPDFLoader

def extract_metadata(text, curr_chapter, curr_title, curr_section, curr_subsec):
    chapter_pattern = r"CHAPTER\s+([IVXLCDM\d]+)\s*[:\-–]?\s*(.+)?"
    section_pattern = r"(\d+\.\d+)\s+(.+)"
    subsection_pattern = r"(\d+\.\d+\.\d+)\s+(.+)"

    chapter_match = re.search(chapter_pattern, text, re.IGNORECASE)
    if chapter_match:
        curr_chapter = f"Chapter {chapter_match.group(1)}"
        curr_title = chapter_match.group(2) if chapter_match.group(2) else "Unknown"
    curr_subsection = re.search(subsection_pattern, text)
    if curr_subsection:
        curr_subsection=f"{curr_subsection.group(1)} {curr_subsection.group(2).strip()}"
    curr_section = re.search(section_pattern, text)
    if curr_section:
        curr_section=f"{curr_section.group(1)} {curr_section.group(2).strip()}"

    return curr_chapter, curr_title, curr_section, curr_subsection


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
                curr_title = "Unknown"
                curr_section= "Unknown"
                curr_subsec= "Unknown"
                for page in loader.lazy_load():
                    result=extract_metadata(page.page_content, curr_chapter, curr_title, curr_section, curr_subsec)
                    if result:
                        curr_chapter, curr_title, curr_section, curr_subsec = result
                    page.metadata['chapter'] = curr_chapter
                    page.metadata['section'] = curr_section
                    page.metadata['subsection'] = curr_subsec
                    doc.extend([page])
    return doc