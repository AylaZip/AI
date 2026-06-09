import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.feature_selection import SelectKBest, chi2
from matplotlib import pyplot as plt
from sklearn.preprocessing import OrdinalEncoder

np.set_printoptions(suppress=True)

### Exercise 1 — Social Network Ads ###
print("=" * 60)
print("Exercise 1: Social Network Ads")
print("=" * 60)

dataset = pd.read_csv('./social_network_ads.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
for val, color, label in [(0, 'blue', 'Not Purchased'), (1, 'red', 'Purchased')]:
    subset = dataset[dataset['Purchased'] == val]
    plt.hist(subset['Age'], bins=15, alpha=0.6, color=color, label=label)
plt.title('Age Distribution by Purchased')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.legend()

plt.subplot(1, 2, 2)
for val, color, label in [(0, 'blue', 'Not Purchased'), (1, 'red', 'Purchased')]:
    subset = dataset[dataset['Purchased'] == val]
    plt.hist(subset['EstimatedSalary'], bins=15, alpha=0.6, color=color, label=label)
plt.title('EstimatedSalary Distribution by Purchased')
plt.xlabel('EstimatedSalary')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.savefig('social_network_histograms.png')
print("Saved social_network_histograms.png")

plt.figure(figsize=(8, 6))
colors = dataset['Purchased'].map({0: 'blue', 1: 'red'})
plt.scatter(dataset['Age'], dataset['EstimatedSalary'], c=colors, alpha=0.6, edgecolors='k')
plt.title('Age vs EstimatedSalary (red=purchased, blue=not)')
plt.xlabel('Age')
plt.ylabel('EstimatedSalary')
plt.savefig('social_network_scatter.png')
print("Saved social_network_scatter.png")
plt.close('all')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(f"\nBaseline Confusion Matrix:\n{cm}")
acc = accuracy_score(y_test, y_pred)
print(f"Baseline Test Accuracy: {acc}")

plt.figure(figsize=(25, 20))
tree.plot_tree(classifier, feature_names=['Age', 'EstimatedSalary'],
               class_names=['no', 'yes'], filled=True, rounded=True)
plt.savefig('social_network_tree_baseline.png')
print("Saved social_network_tree_baseline.png")

new_data = [[30, 87000]]
prediction = classifier.predict(new_data)
print(f"Prediction for [30, 87000]: {'yes' if prediction[0] else 'no'}")

train_acc = classifier.score(X_train, y_train)
print(f"\n--- Overfitting Check ---")
print(f"Train Accuracy: {train_acc:.4f}")
print(f"Test Accuracy:  {acc:.4f}")
print(f"Gap:           {train_acc - acc:.4f}")

if train_acc > acc + 0.05:
    print("\nOverfitting detected! Applying pruning...")
    classifier_pruned = DecisionTreeClassifier(
        criterion='entropy', random_state=0,
        max_depth=4, min_samples_leaf=5
    )
    classifier_pruned.fit(X_train, y_train)
    y_pred_pruned = classifier_pruned.predict(X_test)
    cm_pruned = confusion_matrix(y_test, y_pred_pruned)
    acc_pruned = accuracy_score(y_test, y_pred_pruned)
    train_acc_pruned = classifier_pruned.score(X_train, y_train)
    print(f"\nAfter pruning (max_depth=4, min_samples_leaf=5):")
    print(f"Confusion Matrix:\n{cm_pruned}")
    print(f"Train Accuracy: {train_acc_pruned:.4f}")
    print(f"Test Accuracy:  {acc_pruned:.4f}")
    print(f"Gap:           {train_acc_pruned - acc_pruned:.4f}")

    plt.figure(figsize=(25, 20))
    tree.plot_tree(classifier_pruned, feature_names=['Age', 'EstimatedSalary'],
                   class_names=['no', 'yes'], filled=True, rounded=True)
    plt.savefig('social_network_tree_pruned.png')
    print("Saved social_network_tree_pruned.png")
    classifier = classifier_pruned
else:
    print("\nNo significant overfitting detected.")


### Exercise 2 — Adult Income ###
print("\n" + "=" * 60)
print("Exercise 2: Adult Income Classification")
print("=" * 60)

dataset2 = pd.read_csv('./adult_income.csv')

plt.close('all')
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
numeric_cols = ['age', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week']
for idx, col in enumerate(numeric_cols):
    ax = axes[idx // 3][idx % 3]
    for val, color, label in [('No', 'blue', 'Low'), ('Yes', 'red', 'High')]:
        subset = dataset2[dataset2['income_high'] == val]
        ax.hist(subset[col], bins=20, alpha=0.6, color=color, label=label)
    ax.set_title(f'{col} by income_high')
    ax.legend()
axes[1][2].axis('off')
plt.tight_layout()
plt.savefig('adult_income_histograms.png')
print("Saved adult_income_histograms.png")

X2 = dataset2.drop(columns=['income_high'])
y2 = dataset2['income_high'].values
X2 = X2.drop(columns=['ID'])
cat_cols = X2.select_dtypes(include='str').columns.tolist()
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
X2[cat_cols] = encoder.fit_transform(X2[cat_cols])
X2 = X2.values

X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.20, random_state=0
)

print("\n--- Task 2: Baseline Model ---")
clf2 = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf2.fit(X2_train, y2_train)
y2_pred = clf2.predict(X2_test)
cm2 = confusion_matrix(y2_test, y2_pred)
acc2 = accuracy_score(y2_test, y2_pred)
train_acc2 = clf2.score(X2_train, y2_train)
print(f"Baseline Confusion Matrix:\n{cm2}")
print(f"Train Accuracy: {train_acc2:.4f}")
print(f"Test Accuracy:  {acc2:.4f}")
print(f"Gap:           {train_acc2 - acc2:.4f}")

print("\n--- Task 3: Feature Selection ---")
feature_names = dataset2.drop(columns=['income_high', 'ID']).columns.tolist()
print(f"All features ({len(feature_names)}): {feature_names}")

def prepare_data(drop_cols=None):
    df = dataset2.drop(columns=['income_high'])
    if drop_cols:
        df = df.drop(columns=drop_cols)
    cat = df.select_dtypes(include='str').columns.tolist()
    enc = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    df[cat] = enc.fit_transform(df[cat])
    Xb = df.values
    Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(
        Xb, y2, test_size=0.20, random_state=0
    )
    return Xb_tr, Xb_te, yb_tr, yb_te, list(df.columns)

X3_tr, X3_te, y3_tr, y3_te, cols3 = prepare_data(drop_cols=['ID', 'native_country'])
clf3 = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf3.fit(X3_tr, y3_tr)
acc3 = accuracy_score(y3_te, clf3.predict(X3_te))
print(f"\nWithout native_country ({len(cols3)} features): Accuracy = {acc3:.4f}")

Xb_tr, Xb_te, yb_tr, yb_te, full_cols = prepare_data(drop_cols=['ID'])
selector = SelectKBest(chi2, k=5)
Xb_tr_selected = selector.fit_transform(Xb_tr, yb_tr)
Xb_te_selected = selector.transform(Xb_te)
selected_indices = selector.get_support(indices=True)
selected_names = [full_cols[i] for i in selected_indices]
print(f"\nSelectKBest top 5 features: {selected_names}")

clf3b = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf3b.fit(Xb_tr_selected, yb_tr)
acc3b = accuracy_score(yb_te, clf3b.predict(Xb_te_selected))
print(f"Top 5 features Accuracy: {acc3b:.4f}")

df4 = dataset2.drop(columns=['income_high', 'ID', 'native_country', 'workclass', 'race', 'sex'])
cat4 = df4.select_dtypes(include='str').columns.tolist()
enc4 = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
df4[cat4] = enc4.fit_transform(df4[cat4])
X4_tr, X4_te, y4_tr, y4_te = train_test_split(
    df4.values, y2, test_size=0.20, random_state=0
)
clf4 = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf4.fit(X4_tr, y4_tr)
acc4 = accuracy_score(y4_te, clf4.predict(X4_te))
print(f"\nManual select ({list(df4.columns)}): Accuracy = {acc4:.4f}")

best_acc = max(acc2, acc3, acc3b, acc4)
print(f"\nBest accuracy among feature sets: {best_acc:.4f}")

if best_acc == acc4:
    X2_best_tr, X2_best_te, y2_best_tr, y2_best_te = X4_tr, X4_te, y4_tr, y4_te
    best_feature_names = list(df4.columns)
elif best_acc == acc3b:
    X2_best_tr, X2_best_te = Xb_tr_selected, Xb_te_selected
    y2_best_tr, y2_best_te = yb_tr, yb_te
    best_feature_names = selected_names
elif best_acc == acc3:
    X2_best_tr, X2_best_te, y2_best_tr, y2_best_te = X3_tr, X3_te, y3_tr, y3_te
    best_feature_names = cols3
else:
    X2_best_tr, X2_best_te, y2_best_tr, y2_best_te = X2_train, X2_test, y2_train, y2_test
    best_feature_names = feature_names

print("\n--- Task 4: Addressing Overfitting ---")
clf_best = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf_best.fit(X2_best_tr, y2_best_tr)
train_acc_best = clf_best.score(X2_best_tr, y2_best_tr)
test_acc_best = accuracy_score(y2_best_te, clf_best.predict(X2_best_te))
print(f"Before pruning — Train: {train_acc_best:.4f}, Test: {test_acc_best:.4f}, Gap: {train_acc_best - test_acc_best:.4f}")

param_grid = {
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_leaf': [1, 5, 10, 20],
    'min_samples_split': [2, 5, 10],
}
grid = GridSearchCV(
    DecisionTreeClassifier(criterion='entropy', random_state=0),
    param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
grid.fit(X2_best_tr, y2_best_tr)

best_clf = grid.best_estimator_
y2_best_pred = best_clf.predict(X2_best_te)
cm_best = confusion_matrix(y2_best_te, y2_best_pred)
best_test_acc = accuracy_score(y2_best_te, y2_best_pred)
best_train_acc = best_clf.score(X2_best_tr, y2_best_tr)

print(f"\nBest params: {grid.best_params_}")
print(f"Confusion Matrix (best):\n{cm_best}")
print(f"After pruning — Train: {best_train_acc:.4f}, Test: {best_test_acc:.4f}, Gap: {best_train_acc - best_test_acc:.4f}")

plt.close('all')
plt.figure(figsize=(25, 20))
tree.plot_tree(best_clf, feature_names=best_feature_names,
               class_names=['Low', 'High'], filled=True, rounded=True)
plt.savefig('adult_income_tree_best.png')
print("Saved adult_income_tree_best.png")

print("\nDone!")
