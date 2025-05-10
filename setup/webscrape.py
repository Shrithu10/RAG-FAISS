import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
def clean_text(text):
    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "•": "*"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# arr = [169, 170, 171]  # Replace or extend with desired IPC sections
base_url = "https://devgan.in/ipc/section/{}/"
arr= [
    # General and Core Offenses
    1, 34, 120, "120B", 300, 302, 307, 375, 376, 378, 420, 499, 511,
    
    # Cyber Security (from IT Act, 2000)
    66, "66C", "66D", 67, 69,
    
    # Traffic and Road Safety (from Motor Vehicles Act, 1988)
    184, 185, 192, 194,
    
    # Special and Miscellaneous Offenses
    124, "124A", "153A", 354, "498A", 509
]


pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

for section_num in arr:
    url = base_url.format(section_num)
    print(f"Scraping Section {section_num}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", id="content")

        if not content_div:
            pdf.cell(0, 10, f"Section {section_num}: Content not found.", ln=True)
            continue

        result = {}

        # Chapter
        chapter = content_div.find("th", class_="title")
        if chapter:
            result["Chapter"] = chapter.get_text(strip=True)

        # Section Number and Title
        section_row = content_div.find("tr", class_="mys-head")
        if section_row:
            h2s = section_row.find_all("h2")
            if len(h2s) >= 2:
                result["Section Number"] = h2s[0].get_text(strip=True)
                result["Section Title"] = h2s[1].get_text(strip=True)

        # Description
        desc_row = content_div.find("tr", class_="mys-desc")
        if desc_row:
            result["Description"] = desc_row.get_text(strip=True)

        # Classification
        classification = content_div.find("table", summary="Classification of Offence under Schedule I")
        if classification:
            offense = classification.find("tr", class_="mys-sched")
            if offense:
                cells = offense.find_all("td")
                if len(cells) >= 2:
                    result["Offence"] = cells[0].get_text(strip=True)
                    result["Punishment"] = cells[1].get_text(strip=True)

            tables = classification.find_all("table", class_="sch")
            if len(tables) >= 2:
                trial_row = tables[1].find_all("tr")[1]
                trial_cells = trial_row.find_all("td")
                if len(trial_cells) == 3:
                    result["Cognizance"] = trial_cells[0].get_text(strip=True)
                    result["Bail"] = trial_cells[1].get_text(strip=True)
                    result["Triable By"] = trial_cells[2].get_text(strip=True)

        # Compoundable
        compound_info = content_div.find("table", summary="Whether Offence is Compoundable or Non-Compoundable")
        if compound_info:
            compound_text = compound_info.find("th").get_text(strip=True)
            result["Compoundable"] = "NOT Compoundable" if "NOT" in compound_text else "Compoundable"

        # Add to PDF
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Section {section_num}", ln=True)
        pdf.set_font("Arial", size=12)

        for key, value in result.items():
            cleaned_value = clean_text(value)
            pdf.multi_cell(0, 8, f"{key}: {cleaned_value}")


    except Exception as e:
        pdf.cell(0, 10, f"Error scraping section {section_num}: {e}", ln=True)

# Save PDF
pdf.output("research_paper.pdf")
print("PDF generated: research_paper.pdf")

