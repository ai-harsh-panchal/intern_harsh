#1 program extract repeated word from text#
from collections import Counter

def extract_repeated_words(sentence):
  words = sentence.lower().split()
  word_counts = Counter(words)
  repeated_words = [word for word, count in word_counts.items() if count > 1]
  return '#'.join(repeated_words) if repeated_words else ""

if __name__ == "__main__":
  sample_sentence = "This is a test sentence with test This words that are repeated words."
  result = extract_repeated_words(sample_sentence)
  print("Repeated words:", result)


  #2 program extract string element form list 
  # a. The first character must capitalize and consonant.
  #b. The string must not contain any number.#

def extract_string(lst):
  return [s for s in lst if s and s[0].isupper() and s[0] not in 'AEIOU' and not any(c.isdigit() for c in s)]

my_list = ["Apple", "123Banana", "Cat", "Dog", "eEl", "Fish", "Goat", "Horse", "123"]
result = extract_string(my_list)
print(result)

# 3 Write a program to create a list of numbers, and extract integer numbers from a list
# based on the below conditions.
# a. The number must be 4 digits long i.e (1000 to 9999)
# b. The first digit of the number must be odd and the last digit must be even.
# c. The number must be divisible by either 3 or 7.

def extract_numbers(lst):
  return [num for num in lst if isinstance(num, int) 
          and 1000 <= num <= 9999 
          and num // 1000 % 2 != 0 and num % 2 == 0 
          and (num % 3 == 0 or num % 7 == 0)]

my_list = [1234, 5678, 9012, 3456, 7890, 1111, 4444, 8888, 2222, 3333]
result = extract_numbers(my_list)
print(result)

# 4 program

company = {
    "Project Managers": {
        "Robert Downey": {
            "Team Leads": {
                "Mark": {
                    "Role": "Team Lead",
                    "Experience": 8,
                    "Junior Developers": {
                        "Leonardo": {"Experience": 1, "Role": "Junior Developer"},
                        "Alexandra": {"Experience": 1, "Role": "Junior Developer"}
                    }
                },
                "Samuel": {"Role": "Team Lead", "Experience": 8},
                "Paul": {
                    "Role": "Team Lead",
                    "Experience": 8,
                    "Senior Developers": {
                        "Fergal": {"Experience": 4.5, "Role": "Senior Developer"}
                    }
                },
                "Tom": {
                    "Role": "Team Lead",
                    "Experience": 8,
                    "Junior Developers": {
                        "Jerry": {"Experience": 1.5, "Role": "Junior Developer"},
                        "John": {"Experience": 1.6, "Role": "Junior Developer"}
                    }
                }
            }
        },
        "Anne Hathaway": {
            "Team Leads": {
                "Chris": {
                    "Role": "Team Lead",
                    "Experience": 5,
                    "Senior Developers": {
                        "James": {
                            "Experience": None,
                            "Role": "Team Lead",
                            "Senior Developers": {
                                "Jennifer": {"Experience": 3.8, "Role": "Senior Developer"},
                                "Scott": {"Experience": 3.8, "Role": "Senior Developer"},
                                "Sophie": {"Experience": 3.8, "Role": "Senior Developer"}
                            }
                        }
                    }
                },
                "Pratt": {"Role": "Team Lead", "Experience": 5},

                "Emma": {"Role": "Team Lead", "Experience": 5},

                "Will": {
                    "Role": "Team Lead",
                    "Experience": 5,
                    "Senior Developers": {
                        "Edge": {"Experience": 3, "Role": "Senior Developer"},
                        "Ryan": {"Experience": 3.5, "Role": "Senior Developer"}
                    }
                },
                "Smith": {
                    "Role": "Team Lead",
                    "Experience": 5,
                    "Senior Developers": {
                        "Walker": {"Experience": 2.7, "Role": "Senior Developer"},
                        "Diana": {"Experience": 2.7, "Role": "Senior Developer"}
                    }
                }
            }
        }
    }
}


#retrieve all employee names under a given project manager
def get_employees_by_pm(pm_name):
    employees = []
    pm_data = company["Project Managers"].get(pm_name, None)
    if not pm_data:
        return f"Project Manager {pm_name} not found."

    for tl, tl_data in pm_data["Team Leads"].items():
        employees.append(tl)
        if "Senior Developers" in tl_data:
            employees.extend(tl_data["Senior Developers"])
        if "Junior Developers" in tl_data:
            employees.extend(tl_data["Junior Developers"])

    return employees
pm_name = "Anne Hathaway"
employees_under_pm = get_employees_by_pm(pm_name)
print(f"Employees under Project Manager {pm_name}: {employees_under_pm}")

# Display names of only those employees whose experience is more than 4 years.
def get_employees_exp_more_than_4_years():
    employees = []
    for emp, pm_data in company["Project Managers"].items():
        for tl, tl_data in pm_data["Team Leads"].items():
            if tl_data["Experience"] > 4:
                employees.append(tl)
                if "Senior Developers" in tl_data:
                    employees.extend(tl_data["Senior Developers"])
    print(f'employee list > 4yrs exp :{employees}')
    print('') 
get_employees_exp_more_than_4_years()

#Update years of experience with 4.6 whose experience is greater than 3.5 and
#less than 4.5 years.#
def update_experience():
    for emp, pm_data in company["Project Managers"].items():
        for tl, tl_data in pm_data["Team Leads"].items():
                if 3.5 < tl_data["Experience"] < 4.5:
                    tl_data["Experience"] = 4.6
    print(f'Experience updated for {tl}: {tl_data["Experience"]}')
    print('') 
update_experience()

#Display TL with their year of experience
# if has no experience then display N/A.
def display_tl_experience():
    for emp, pm_data in company["Project Managers"].items():
        for tl, tl_data in pm_data["Team Leads"].items():
            if tl_data["Experience"] == 0:
                print(f'N/A.')
            else:
                print(f'Team Lead {tl} has {tl_data["Experience"]} years of experience.')
                print('') 
display_tl_experience()

# Smith left the company and all his members were assigned to Ryan.
def transfer_members(old_team_lead, new_team_lead):
    if new_team_lead in company["Project Managers"]["Anne Hathaway"]["Team Leads"]:
        members = company["Project Managers"]["Anne Hathaway"]["Team Leads"][old_team_lead]["Senior Developers"]
        company["Project Managers"]["Anne Hathaway"]["Team Leads"][new_team_lead]["Senior Developers"].extend(members)
        del company["Project Managers"]["Anne Hathaway"]["Team Leads"][old_team_lead]
        print(f'Members of {old_team_lead} were assigned to {new_team_lead}.')
    else:
        print(f'{new_team_lead} is not a valid team lead to assign members to another .')
        print('')                       
transfer_members("Smith", "Ryan")

# Check company has any employee who has less than 2 years of experience.
# Check whether Edge is TL or not if not make him TL.

def check_experience_and_promote():
    for pm, pm_data in company["Project Managers"].items():
        for tl, tl_data in pm_data["Team Leads"].items():
            if tl_data.get("Junior Developers"):
                for junior, junior_data in tl_data["Junior Developers"].items():
                    if junior_data["Experience"] < 2:
                        print(f'{junior} has less than 2 years of experience.')

    for pm, pm_data in company["Project Managers"].items():
        for tl, tl_data in pm_data["Team Leads"].items():
            if tl == "Edge":
                print(f'Edge is already a Team Lead.')
                return
    company["Project Managers"]["Anne Hathaway"]["Team Leads"]["Edge"] = {
        "Role": "Team Lead",
        "Experience": 0,  
        "Senior Developers": {}
    }
    print('')
    print('Edge has been promoted to Team Lead.')
 
check_experience_and_promote()