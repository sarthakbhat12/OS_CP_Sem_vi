# ml/model.py

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from ml.dataset import generate_dataset


class MLModel:

    def __init__(self):
        self.model = None
        self.encoder = LabelEncoder()
        self.metrics = {}

    def train(self):
        X, y = generate_dataset()

        y_encoded = self.encoder.fit_transform(y)

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded,
                test_size=0.2,
                random_state=42,
                stratify=y_encoded
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded,
                test_size=0.2,
                random_state=42
            )

        dt = DecisionTreeClassifier(max_depth=5, random_state=42)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)

        dt.fit(X_train, y_train)
        rf.fit(X_train, y_train)

        dt_pred = dt.predict(X_test)
        rf_pred = rf.predict(X_test)

        dt_acc = accuracy_score(y_test, dt_pred)
        rf_acc = accuracy_score(y_test, rf_pred)

        best_model = rf if rf_acc >= dt_acc else dt
        best_pred = rf_pred if rf_acc >= dt_acc else dt_pred
        
        report = classification_report(
            y_test,
            best_pred,
            target_names=self.encoder.classes_,
            zero_division=1,
            output_dict=True
        )

        self.model = best_model
        self.metrics = {
            "decision_tree_accuracy": dt_acc,
            "random_forest_accuracy": rf_acc,
            "selected_model": type(self.model).__name__,
            "report": report
        }
        
        return self.metrics

    def predict(self, processes):
        import numpy as np

        bursts = [p.burst for p in processes]
        arrivals = [p.arrival for p in processes]

        features = [[
            len(processes),
            float(np.mean(bursts)),
            float(np.std(bursts)),
            max(bursts),
            min(bursts),
            max(arrivals) - min(arrivals),
            sum(bursts),
            len([b for b in bursts if b > np.mean(bursts)])
        ]]

        pred = self.model.predict(features)[0]
        return self.encoder.inverse_transform([pred])[0]