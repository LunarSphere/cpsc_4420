import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("annotations_eval.csv")   # change filename if needed

# Compute accuracy per question type
accuracy_by_type = df.groupby("question_type")["correct"].mean()

#drop navigation veer and turn under question column question_type
accuracy_by_type = accuracy_by_type.drop(index=["Navigation Veer", "Navigation Turn"], errors='ignore')


print("Accuracy by question type:")
print(accuracy_by_type)

# Plot
plt.figure(figsize=(9, 9))
accuracy_by_type.plot(kind="bar")

plt.title("Accuracy by Question Type")
plt.xlabel("Question Type")
plt.ylabel("Accuracy")
plt.ylim(0, 1)            # accuracy is between 0 and 1
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
