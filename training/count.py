import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------
# 1️⃣ Load Dataset
# -----------------------------------------------------
df = pd.read_csv("C:/Users/Joshua/Downloads/ai-spam-detection-telegram-bot/dataset/mail_data_ml.csv")

# Rename columns for consistency
df = df.rename(columns={"Category": "label", "Message": "message"})

# Normalize labels
df["label"] = df["label"].astype(str).str.lower().map({"spam": 1, "ham": 0})
df = df.dropna(subset=["label"])

# -----------------------------------------------------
# 2️⃣ Show Counts and Percentages
# -----------------------------------------------------
counts = df["label"].value_counts()
percentages = df["label"].value_counts(normalize=True) * 100

print("📊 Dataset Summary:")
print(counts)
print(df["label"].value_counts())
print("\n📈 Percentage Distribution (%):")
print(percentages.round(2))

# -----------------------------------------------------
# 3️⃣ Visualize
# -----------------------------------------------------
plt.figure(figsize=(5, 4))
ax = sns.countplot(x="label", data=df, palette="coolwarm", legend=False)
for p in ax.patches:
    ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 10,
            int(p.get_height()), ha='center')
plt.title("Spam vs Ham Distribution")
plt.xlabel("Label (0 = Ham, 1 = Spam)")
plt.ylabel("Count")
plt.show()

