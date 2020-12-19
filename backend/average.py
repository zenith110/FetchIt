import json 
import os
import sys
def Get_Average(Term):
    Term_Files = [d for d in os.listdir("FE") if Term in d]
    total_average_score_section_I = float()
    total_average_score_section_II = float()
    total_average_score_total = float()
    total_DS_A1 = float()
    total_DS_A2 = float()
    total_DS_A3 = float()
    total_DS_B1 = float()
    total_DS_B2 = float()
    total_DS_B3 = float()
    total_AA1 = float()
    total_AA2 = float()
    total_AA3 = float()
    total_AB1 = float()
    total_AB2 = float()
    total_AB3 = float()
    for i in Term_Files:
        with open("FE/" + i) as f:
            data = json.load(f)
        total_average_score_section_I += float(data["average_score_section_I"])
        total_average_score_section_II = float(data["average_score_section_II"])
        total_average_score_total = float(data["average_score_total"])
        total_DS_A1 = float(data["DS_A1"])
        total_DS_A2 = float(data["DS_A2"])
        total_DS_A3 = float(data["DS_A3"])
        total_DS_B1 = float(data["DS_B1"])
        total_DS_B2 = float(data["DS_B2"])
        total_DS_B3 = float(data["DS_B3"])
        total_AA1 = float(data["AA1"])
        total_AA2 = float(data["AA2"])
        total_AA3 = float(data["AA3"])
        total_AB1 = float(data["AB1"])
        total_AB2 = float(data["AB2"])
        total_AB3 = float(data["AB3"])
    
    
    total_average_score_section_I /= len(Term_Files)
    total_average_score_section_II /= len(Term_Files)
    total_average_score_total /= len(Term_Files)
    total_DS_A1 /= len(Term_Files) 
    total_DS_A2 /= len(Term_Files)
    total_DS_A3 /= len(Term_Files)
    total_DS_B1 /= len(Term_Files)
    total_DS_B2 /= len(Term_Files)
    total_DS_B3 /= len(Term_Files)
    total_AA1 /= len(Term_Files)
    total_AA2 /= len(Term_Files)
    total_AA3 /= len(Term_Files)
    total_AB1 /= len(Term_Files)
    total_AB2 /= len(Term_Files)
    total_AB3 /= len(Term_Files)
    data = {}
    data[Term + "-Average"] = []
    
    # Create a default JSON structure
    data[Term + "-Average"].append(
    {
        "average_score_section_I": str(total_average_score_section_I) + "%",
        "average_score_section_II": str(total_average_score_section_II) + "%",
        "average_score_total": str(total_average_score_total) + "%",
        "DS_A1": str(total_DS_A1) + "%",
        "DS_A2": str(total_DS_A2) + "%",
        "DS_A3": str(total_DS_A3) + "%",
        "DS_B1": str(total_DS_B1) + "%",
        "DS_B2": str(total_DS_B2) + "%",
        "DS_B3": str(total_DS_B3) + "%",
        "AA1": str(total_AA1) + "%",
        "AA2": str(total_AA2) + "%",
        "AA3": str(total_AA3) + "%",
        "AB1": str(total_AB1) + "%",
        "AB2": str(total_AB2) + "%",
        "AB3": str(total_AB3) + "%"
    })
    with open("FE/" + Term + "-average.json", "w") as f:
        json.dump(data, f, indent = 2)
            
if __name__ == "__main__":
    term = sys.argv[1]
    Get_Average(term)