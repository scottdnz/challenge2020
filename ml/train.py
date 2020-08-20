import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *


def build_model(my_learning_rate, inputs):
	"""Create and compile a simple linear regression model."""
	# Most simple tf.keras models are sequential. 
	# A sequential model contains one or more layers.
	model = tf.keras.models.Sequential()

	# Describe the topography of the model.
	# The topography of a simple linear regression model
	# is a single node in a single layer. 

	num_c = [
		"classified_use_3",
		"classified_use_4",
		"Metal Sheet Colorsteel"
	]
	feature_columns = []
	for header in num_c:
		feature_columns.append(tf.feature_column.numeric_column(header))

	#model.add(tf.keras.layers.DenseFeatures(feature_columns))


	model.add(tf.keras.layers.Dense(units=64, activation='sigmoid', input_shape = (inputs,)))
	#model.add(tf.keras.layers.Dense(units=24, activation='relu')) #input_shape=(1,)

	model.add(tf.keras.layers.Dense(units=16, activation='sigmoid'))
	model.add(tf.keras.layers.Dense(units=4, activation='sigmoid'))
	model.add(tf.keras.layers.Dense(units=1, activation='linear'))
	#model.add(tf.keras.layers.Dense(units=5, activation='relu'))

	# Compile the model topography into code that 
	# TensorFlow can efficiently execute. Configure 
	# training to minimize the model's mean squared error. 
	model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=my_learning_rate),
					loss="mean_squared_error",
					metrics=[tf.keras.metrics.BinaryAccuracy()]) #RootMeanSquaredError
	model.summary()

	return model


def train_model(model, xin, yin, epochs, batch_size):
	"""Train the model by feeding it data."""

	# Feed the model the feature and the label.
	# The model will train for the specified number of epochs. 
	history = model.fit(x=xin,
						y=yin,
						batch_size=batch_size,
						epochs=epochs)

	# Gather the trained model's weight and bias.
	trained_weight = model.get_weights()[0]
	trained_bias = model.get_weights()[1]

	# The list of epochs is stored separately from the rest of history.
	epochs = history.epoch
  
	# Isolate the error for each epoch.
	hist = pd.DataFrame(history.history)

	# To track the progression of training, we're going to take a snapshot
	# of the model's root mean squared error at each epoch. 
	rmse = 0 #hist["root_mean_squared_error"]

	return trained_weight, trained_bias, epochs, rmse


def split_data(df, f):
	set2 = df.sample(frac=f,random_state=26394)
	set1 = df.drop(set2.index)
	return set1, set2


def prepare_data(csv_file):
	qcode = '6a3bc4d3-3cd5-11e6-8be5-000c292dee42'

	training_data_df = pd.read_csv(csv_file)
	training_data_df = training_data_df.reindex(np.random.permutation(training_data_df.index)) # shuffle the examples

	# remove unused
	training_data_df = training_data_df.drop('DB', axis=1)
	training_data_df = training_data_df.drop('ID', axis=1)
	training_data_df = training_data_df.drop('question_'+qcode+'_pass', axis=1)
	training_data_df = training_data_df.drop('question_'+qcode+'_fail', axis=1)

	training_data_df, test_data_df = split_data(training_data_df, 0.2)

	training_x = training_data_df.drop('question_'+qcode+'_na', axis=1).values
	training_y = training_data_df[['question_'+qcode+'_na']].values

	test_x = test_data_df.drop('question_'+qcode+'_na', axis=1).values
	test_y = test_data_df[['question_'+qcode+'_na']].values


	training_data_df.describe()

	# unused
	features = {name:np.array(value) for name, value in training_data_df.items()}
	label = np.array(features.pop('question_'+qcode+'_na'))

	return training_x, training_y, test_x, test_y



training_x, training_y, test_x, test_y = prepare_data("all_results.csv")


learning_rate = 0.002
epochs = 25
batch_size = 20

# Discard any pre-existing version of the model.
my_model = None

# Invoke the functions.
my_model = build_model(learning_rate, training_x.shape[1])

weight, bias, epochs, rmse = train_model(my_model, training_x, training_y, epochs, batch_size)

#print("\nThe learned weight for your model is %.4f" % weight)
#print("The learned bias for your model is %.4f\n" % bias )

# Specify the feature and the label.
#my_feature = "classified_use_0"  # the total number of rooms on a specific city block.
#my_label="question_0402249f-3830-11e6-8be5-000c292dee42_na" # 
#plot_the_model(weight, bias, my_feature, my_label)
#plot_the_loss_curve(epochs, rmse)


r = my_model.evaluate(training_x, training_y, batch_size=batch_size)
print(r)

#for i in training_x:
#	r = my_model.predict([i.tolist()])
#	print(r)

r = my_model.evaluate(test_x, test_y, batch_size=batch_size)
print(r)
