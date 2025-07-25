import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from LearningAlgorithms import ClassificationAlgorithms
import seaborn as sns
import itertools
from sklearn.metrics import accuracy_score, confusion_matrix

# Plot settings
plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (20, 5)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["lines.linewidth"] = 2

# Load dataset
df = pd.read_pickle("../../ML project/data/interim/03_data_features.pkl")

# Create a training and test set
df_train = df.drop(["participant", "category", "set"], axis=1)
X = df_train.drop("label", axis=1)
y = df_train["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Visualize label distribution
fig, ax = plt.subplots(figsize=(10, 5))
df_train["label"].value_counts().plot(
    kind="bar", ax=ax, color="lightblue", label="Total"
)
y_train.value_counts().plot(kind="bar", ax=ax, color="dodgerblue", label="Train")
y_test.value_counts().plot(kind="bar", ax=ax, color="royalblue", label="Test")
plt.legend()
plt.show()

# Feature subsets

basic_features = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z"]
square_features = []
cluster_features = ["cluster"]

feature_set_1 = list(set(basic_features))
feature_set_2 = list(set(basic_features + square_features + cluster_features))



# Summary of features
print("Basic features:", len(basic_features))
print("Square features:", len(square_features))
print("Cluster features:", len(cluster_features))


# Perform forward feature selection
learner = ClassificationAlgorithms()
max_features = 10

# Forward feature selection
selected_features, ordered_features, ordered_scores = learner.forward_selection(
    max_features, X_train[feature_set_1], y_train
)

# Plot feature selection scores
plt.figure(figsize=(10, 5))
plt.plot(np.arange(1, max_features + 1, 1), ordered_scores)
plt.xlabel("Number of features")
plt.ylabel("Accuracy")
plt.xticks(np.arange(1, max_features + 1, 1))
plt.show()

# Grid search for best feature set and model
possible_feature_sets = [feature_set_1, feature_set_2]
feature_names = ["Feature Set 1", "Feature Set 2"]



iterations = 1
score_df = pd.DataFrame()




print(df_train.columns)


for i, f in zip(range(len(possible_feature_sets)), feature_names):
    print("Feature set:", i)
    selected_train_X = X_train[possible_feature_sets[i]]
    selected_test_X = X_test[possible_feature_sets[i]]

    # Initialize performance metrics
    performance_test_nn = 0
    performance_test_rf = 0

    for it in range(0, iterations):
        print("\tTraining neural network,", it)
        (
            class_train_y,
            class_test_y,
            class_train_prob_y,
            class_test_prob_y,
        ) = learner.feedforward_neural_network(
            selected_train_X, y_train, selected_test_X, gridsearch=False
        )
        performance_test_nn += accuracy_score(y_test, class_test_y)

        print("\tTraining random forest,", it)
        (
            class_train_y,
            class_test_y,
            class_train_prob_y,
            class_test_prob_y,
        ) = learner.random_forest(
            selected_train_X, y_train, selected_test_X, gridsearch=True
        )
        performance_test_rf += accuracy_score(y_test, class_test_y)

    # Average non-deterministic classifier performance
    performance_test_nn /= iterations
    performance_test_rf /= iterations

    # Deterministic classifiers
    print("\tTraining KNN")
    (
        class_train_y,
        class_test_y,
        class_train_prob_y,
        class_test_prob_y,
    ) = learner.k_nearest_neighbor(selected_train_X, y_train, selected_test_X, gridsearch=True)
    performance_test_knn = accuracy_score(y_test, class_test_y)

    print("\tTraining decision tree")
    (
        class_train_y,
        class_test_y,
        class_train_prob_y,
        class_test_prob_y,
    ) = learner.decision_tree(selected_train_X, y_train, selected_test_X, gridsearch=True)
    performance_test_dt = accuracy_score(y_test, class_test_y)

    print("\tTraining naive bayes")
    (
        class_train_y,
        class_test_y,
        class_train_prob_y,
        class_test_prob_y,
    ) = learner.naive_bayes(selected_train_X, y_train, selected_test_X)
    performance_test_nb = accuracy_score(y_test, class_test_y)

    # Store results
    models = ["NN", "RF", "KNN", "DT", "NB"]
    new_scores = pd.DataFrame(
        {
            "model": models,
            "feature_set": f,
            "accuracy": [
                performance_test_nn,
                performance_test_rf,
                performance_test_knn,
                performance_test_dt,
                performance_test_nb,
            ],
        }
    )
    score_df = pd.concat([score_df, new_scores])

# Compare results in a bar plot
score_df.sort_values(by="accuracy", ascending=False, inplace=True)
plt.figure(figsize=(10, 10))
sns.barplot(x="model", y="accuracy", hue="feature_set", data=score_df)
plt.xlabel("Model")
plt.ylabel("Accuracy")
plt.ylim(0.7, 1)
plt.legend(loc="lower right")
plt.show()

# Final model evaluation with confusion matrix
(
    class_train_y,
    class_test_y,
    class_train_prob_y,
    class_test_prob_y,
) = learner.random_forest(X_train[feature_set_2], y_train, X_test[feature_set_2], gridsearch=True)

accuracy = accuracy_score(y_test, class_test_y)

# Confusion matrix
cm = confusion_matrix(y_test, class_test_y)
plt.figure(figsize=(10, 10))
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.title("Confusion matrix")
plt.colorbar()
tick_marks = np.arange(len(y_test.unique()))
plt.xticks(tick_marks, y_test.unique(), rotation=45)
plt.yticks(tick_marks, y_test.unique())

thresh = cm.max() / 2.0
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(
        j,
        i,
        format(cm[i, j]),
        horizontalalignment="center",
        color="white" if cm[i, j] > thresh else "black",
    )
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.grid(False)
plt.show()




#select train and test data based on participant

participant_df=df.drop(["set","category"],axis=1)

X_train=participant_df[participant_df["participant"]!="A"].drop("label",axis=1)

y_train=participant_df[participant_df["participant"]!="A"]["label"]


X_test=participant_df[participant_df["participant"]=="A"].drop("label",axis=1)

y_test=participant_df[participant_df["participant"]=="A"]["label"]


X_train=X_train.drop(["participant"],axis=1)

X_test=X_test.drop(["participant"],axis=1)




fig,ax=plt.subplots(figsize=(10,5))
df_train["label"].value_counts().plot(
    kind="bar",ax=ax,color="lightblue",label="Total"
)
y_train.value_counts().plot(kind="bar",ax=ax,color="dodgerblue",label="Train")
y_test.value_counts().plot(kind="bar",ax=ax,color="royalblue",label="Test")
plt.legend()
plt.show()


# use best model again and evaluate results
(
    class_train_y,
    class_test_y,
    class_train_prob_y,
    class_test_prob_y,
) = learner.random_forest(X_train[feature_set_2], y_train, X_test[feature_set_2], gridsearch=True)

accuracy = accuracy_score(y_test, class_test_y)

# Confusion matrix
cm = confusion_matrix(y_test, class_test_y)
plt.figure(figsize=(10, 10))
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.title("Confusion matrix")
plt.colorbar()
tick_marks = np.arange(len(y_test.unique()))
plt.xticks(tick_marks, y_test.unique(), rotation=45)
plt.yticks(tick_marks, y_test.unique())

thresh = cm.max() / 2.0
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(
        j,
        i,
        format(cm[i, j]),
        horizontalalignment="center",
        color="white" if cm[i, j] > thresh else "black",
    )
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.grid(False)
plt.show()


#try a simpler model with the selected features


(
    class_train_y,
    class_test_y,
    class_train_prob_y,
    class_test_prob_y,
) = learner.random_forest(X_train[selected_features], y_train, X_test[selected_features], gridsearch=False)

accuracy = accuracy_score(y_test, class_test_y)

# Confusion matrix
cm = confusion_matrix(y_test, class_test_y)
plt.figure(figsize=(10, 10))
plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
plt.title("Confusion matrix")
plt.colorbar()
tick_marks = np.arange(len(y_test.unique()))
plt.xticks(tick_marks, y_test.unique(), rotation=45)
plt.yticks(tick_marks, y_test.unique())

thresh = cm.max() / 2.0
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(
        j,
        i,
        format(cm[i, j]),
        horizontalalignment="center",
        color="white" if cm[i, j] > thresh else "black",
    )
plt.ylabel("True label")
plt.xlabel("Predicted label")
plt.grid(False)
plt.show()
