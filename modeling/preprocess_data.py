import pandas as pd
import pickle


def preprocess(data_path):
    df = pd.read_csv(data_path)
    df = df.drop_duplicates()

    # constructing data
    dataset = []
    for i in range(df.index.size):
        es1, es2, es3, es4, es9 = df['essay1'][i], df['essay2'][i], df['essay3'][i], df['essay4'][i], df['essay9'][i]
        if not pd.isnull(es1) and not pd.isnull(es2) and not pd.isnull(es3) and not pd.isnull(es4) and not pd.isnull(
                es9):

            es = f'{es1} {es2} {es3} {es4} {es9}'
            missed = 0

            premise = ''
            if not pd.isnull(df['age'][i]):
                premise += f"I am {df['age'][i]} years old. "
            else:
                missed += 1

            if not pd.isnull(df['education'][i]):
                premise += f"My education is {df['education'][i]}. "
            else:
                missed += 1

            if not pd.isnull(df['sex'][i]):
                premise += f"My sex is {'male' if df['sex'][i] == 'm' else 'female'}. "
            else:
                missed += 1

            if not pd.isnull(df['body_type'][i]):
                premise += f"My body type is {df['body_type'][i]}. "
            else:
                missed += 1

            if not pd.isnull(df['job'][i]):
                premise += f"My job is {df['job'][i]}. "
            else:
                missed += 1

            if not pd.isnull(df['height'][i]):
                premise += f"My height is {df['height'][i]}. "
            else:
                missed += 1

            if not pd.isnull(df['sign'][i]):
                premise += f"My sign is {df['sign'][i]}. "
            else:
                missed += 1

            if missed > 3:
                continue

            dataset += [f'{premise} My tinder bio => {es}']

        # filter out extremely long and extremely short descriptions
        filtered_dataset = []
        for i in range(len(dataset)):
            if len(dataset[i].split()) > 400 or len(dataset[i].split()) < 100:
                continue
            filtered_dataset += [dataset[i]]

        t = len(filtered_dataset) - 2000

        pickle.dump(filtered_dataset[:t], open('okcupid_train.pkl', 'wb'))
        pickle.dump(filtered_dataset[t:t + 1000], open('okcupid_val.pkl', 'wb'))
        pickle.dump(filtered_dataset[t + 1000:t + 2000], open('okcupid_test.pkl', 'wb'))
