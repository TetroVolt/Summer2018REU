#!/usr/bin/env python3

def pre_process_data(
   file_name, pickled=True, feature_cols=[], label_col=-1, one_hot=False):

   if pickled:
      df = pd.read_pickle(file_name)
   else:
      df = pd.read_csv(file_name)

   if isinstance(label_col, int):
      label_col = df.columns[label_col]

   assert(isinstance(feature_cols, (list, tuple)))

   if not feature_cols:
      feature_cols =[f for f in df.columns if f != label_col]
   elif all(isinstance(f, int) for f in feature_cols):
      feature_cols =[f for i, f in enumerate(df.columns) if i in feature_cols and f != label_col]
   else:
      assert(all(isinstance(f, str), for f in feature_cols))
      feature_cols =[f for f in df.columns if f in feature_cols]

   features = df[feature_cols].values
   labels = df[label_col].values

   if one_hot:
      labels = np.eye(np.unique(labels).shape[0])[labels]

   return features, labels

if __name__=='__main__'
   print('THIS FILE IS A LIBARY FOR TOTI MACHINE LEARNING, not meant to be run as a script')

