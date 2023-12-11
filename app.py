from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

knn = pickle.load(open('models/knn.pkl', 'rb'))
tree = pickle.load(open('models/tree.pkl', 'rb'))
forest = pickle.load(open('models/forest.pkl', 'rb'))
adaboost = pickle.load(open('models/adaboost.pkl', 'rb'))


@app.route('/predict')
def hello_world(values: str):  # put application's code here
    return values


class NetworkConnection:
    def __init__(self, *args):
        # Assuming the order of values corresponds to the order of attributes in the class
        self.duration, self.protocol_type, self.service, self.flag, self.src_bytes, self.dst_bytes, \
        self.land, self.wrong_fragment, self.urgent, self.hot, self.num_failed_logins, self.logged_in, \
        self.num_compromised, self.root_shell, self.su_attempted, self.num_root, self.num_file_creations, \
        self.num_shells, self.num_access_files, self.num_outbound_cmds, self.is_host_login, \
        self.is_guest_login, self.count, self.srv_count, self.serror_rate, self.srv_serror_rate, \
        self.rerror_rate, self.srv_rerror_rate, self.same_srv_rate, self.diff_srv_rate, \
        self.srv_diff_host_rate, self.dst_host_count, self.dst_host_srv_count, self.dst_host_same_srv_rate, \
        self.dst_host_diff_srv_rate, self.dst_host_same_src_port_rate, self.dst_host_srv_diff_host_rate, \
        self.dst_host_serror_rate, self.dst_host_srv_serror_rate, self.dst_host_rerror_rate, \
        self.dst_host_srv_rerror_rate = args


@app.route('/test/<values>')
def test(values):  # put application's code here
    values_list = values.split(',')
    columns = (
        ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
         'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted'
            , 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
         'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
         'same_srv_rate', 'diff_srv_rate'
            , 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
         'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
         'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'])
    data = pd.DataFrame([values_list], columns=columns)
    data.drop(columns=["num_outbound_cmds"], inplace=True)
    for col in ['protocol_type', 'service', 'flag']:
        data[col] = data[col].astype('category')
    label_encoder = LabelEncoder()

    for col in data.select_dtypes(include="category").columns:
        data[col] = label_encoder.fit_transform(data[col])

    predictions = [forest.predict(data.iloc[:, :12]),knn.predict(data.iloc[:, :12]), adaboost.predict(data.iloc[:, :12])]
    results = []
    for pred in predictions:
        print(pred[0])
        if pred[0] == 0:
            results.append("Normal")
        if pred[0] == 1:
            print("test")
            results.append("DoS")
        if pred[0] == 2:
            results.append("U2R")
        if pred[0] == 3:
            results.append("R2L")
        if pred[0] == 4:
            results.append("Probe")
    print(results[0])
    return render_template("result.html", forest=results[0], knn=results[1],adaboost=results[2])


if __name__ == '__main__':
    app.run()
