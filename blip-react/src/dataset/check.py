import pandas as pd

df = pd.read_csv("dataset.csv")

# Step 1: Lowercase all labels
df['label'] = df['label'].str.lower()

# Step 2: Remove extra spaces
df['label'] = df['label'].str.strip()

df['label'] = df['label'].str.replace('-', '')

df['label'].replace({
    "user experience & entertainment": "user experience",
    "social norms & relationships": "social norms & relationship",
    "power": "power dynamics",
    "information, discourse & governance": "access to information & discourse",
    "answer: privacy": "security & privacy",
    "children's growth and wellbeing.": "health & wellbeing",
    "(if you have questions, feel free to ask)": "user experience"
}, inplace=True)

# label_mapping = {
#     # 'voice assistant': 'Voice Assistant',
#     # 'voice assistants': 'Voice Assistant',
#     # 'augmented/virtual reality': 'Augmented/Virtual Reality',
#     # 'virtual reality': 'Augmented/Virtual Reality',
#     # 'mobile technology': 'Mobile Technology',
#     "computer vision", "Computer Vision"
# }

# Lowercase the labels before replacing to make the process case-insensitive
# df['sector'] = df['sector'].str.lower()

# # Replace the labels
# df['sector'].replace(label_mapping, inplace=True)

# # Capitalize the first letter of each word in the labels
# df['sector'] = df['sector'].str.title()

print(df['sector'].value_counts())

df["label"] = df["label"].apply(lambda x: "environment & sustainability" if "environment & sustainability" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "access to information & discourse" if "access to information & discourse" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "politics" if "leading to wrongful convictions or acquittals" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "power dynamics" if "business culture" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "economy" if "economy" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "politics" if "politics" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "equality & justice" if "equality & justice" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "security & privacy" if "security & privacy" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "power dynamics" if "efficiency" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "user experience" if "technical" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "user experience" if "performance" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "social norms & relationship" if "education" in str(x).lower() else x)
df["label"] = df["label"].apply(lambda x: "social norms & relationship" if "art" in str(x).lower() else x)
df = df[~df['label'].isin(["thank you for taking the time to answer this question. your input is valuable to me. if you have any questions or concerns, please don't hesitate to reach out. i'm here to help.\n\nbest regards,\n[your name]",
                            '''please select one aspect of life that the consequence affects the most. for example, if the consequence is about health, select "health & wellbeing". if the consequence is about privacy, select "privacy & security".\n\nnote: you can select only one option.''', 
                            "1. unrealistic expectations\n2. misuse of ai\n3. inadequate regulation\n4. lack of investment in human capabilities\n5. unintended consequences\n\nplease select one of the options from the list above.",
                            ""
                            ])] 

df = df[~df['title'].isin(["TechCrunch+ roundup: Tested TAM tips, no-code tech survey, writing crypto white papers"])] 

# print(df["label"].value_counts())
# magazine_label_mapping = {
#     "computer vision techcrunch final": "TechCrunch",
#     "computer vision the verge": "The Verge",
#     "computer vision mit tech review": "MIT Tech Review",
#     "computer vision wired": "Wired"
# }
# df["sector"] = df["magazine"].apply(lambda x: "Computer Vision" if "computer vision" in x else x)
# df['magazine'].replace(magazine_label_mapping, inplace=True)

print(df)
print(df["label"].value_counts())
# print(len(df))
with open("dataset.csv", "w") as f:
    df.to_csv(f, index=False)
