import pandas as pd

df = pd.read_csv('./2022_spring.csv')

# We want only undergraduate courses
df = df[df['Number'] < 4900]
df.to_csv('dataset.csv', index=False)

# Note: gcloud SQL imports don't like column titles in the CSV, they just assume it follows the schema

# User not populated here
# Calendar not populated here

# Note that this data does not include department descriptions, but our DB supports adding them
departments = df[['Mnemonic']].drop_duplicates()
departments.to_csv('department.csv', header=None, index=False)

courses = df[['Title', 'Description', 'Units', 'Mnemonic', 'Number']]
courses = courses[courses['Units'] != '0'].drop_duplicates()
courses = courses.reset_index(drop=True)
courses.to_csv('course.csv', header=None)

sections = []
section_index = 0
section_times = []
section_days = []
section_instructors = []
for index, section in df.iterrows():
    # section ID handled implicitly by index
    section_type = section['Type']
    matching_indices = courses.index[
        (courses['Mnemonic'] == section['Mnemonic']) & (courses['Number'] == section['Number'])]
    if len(matching_indices) != 1:
        print(
            f'WARNING: {section["Mnemonic"]} {section["Number"]} is being skipped (creditless class?)')
        continue
    sections.append([section_type, matching_indices[0]])

    if section['Days1'] != 'TBA':
        datetime = section['Days1']
        days = datetime[:datetime.find(' ')]
        time = datetime[datetime.find(' ') + 1:]

        section_times.append([section_index, time])
        for i in range(int(len(days) / 2)):
            section_days.append([section_index, days[2 * i:2 * i + 2]])

    instructors = section['Instructor1']
    for name in instructors.split(','):
        section_instructors.append([section_index, name])
    section_index += 1
sections = pd.DataFrame(sections)
sections.to_csv('section.csv', header=None)

section_times = pd.DataFrame(section_times)
section_times.to_csv('section_times.csv', index=False, header=None)

section_days = pd.DataFrame(section_days)
section_days.to_csv('section_days.csv', index=False, header=None)

section_instructors = pd.DataFrame(section_instructors)
section_instructors.to_csv('section_instructors.csv', index=False, header=None)

# Contains is not populated here
# Enrolls_In is not populated
