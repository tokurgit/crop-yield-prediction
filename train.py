
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction import DictVectorizer

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import mean_squared_error, normalized_mutual_info_score


df = pd.read_csv("data/yield_df.csv")


df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("/","_")
categorical = ["area", "item"]

for col in categorical:
    df[col] = df[col].str.lower().str.replace(" ", "_")

# Remove `Unnamed: 0` column as it seems to not serve any purpose, duplicates index value.
df = df.drop("unnamed:_0", axis=1)

# %%
random_seed = 1
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=random_seed)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=random_seed)

df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)

y_train = np.log1p(df_train.hg_ha_yield.values)
y_val = np.log1p(df_val.hg_ha_yield.values)
y_test = np.log1p(df_test.hg_ha_yield.values)

del df_train["hg_ha_yield"]
del df_val["hg_ha_yield"]
del df_test["hg_ha_yield"]

# %%
dv = DictVectorizer(sparse=False)

train_dicts = df_train.to_dict(orient="records")
val_dicts = df_val.to_dict(orient="records")

X_train = dv.fit_transform(train_dicts)
X_val = dv.transform(val_dicts)

# %% [markdown]
# # Evaluate results from:
# - Linear regression
# - Ridge, Lasso
# - DecisionTreeRegressor
# - RandomForestRegressor
# - GradientBoostingRegressor

# %%
model_names = []
results = []
for _class in [LinearRegression, Ridge, Lasso, DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor]:
    print(_class.__name__)
    model_names.append(_class.__name__)
    kwargs = {}
    if _class in [DecisionTreeRegressor, RandomForestRegressor, GradientBoostingRegressor]:
        kwargs["max_depth"] = 5
    if _class in [RandomForestRegressor, GradientBoostingRegressor]:
        kwargs["n_estimators"] = 200
        kwargs["min_samples_leaf"] = 3

    # Initiate model
    model = _class(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)
    
    # Measure predictive performance 
    mse = mean_squared_error(y_val, y_pred)
    rmse = np.sqrt(mse)
    results.append((y_pred, rmse))

# %%
df_results = pd.DataFrame(results, columns=["PRED", "RMSE"], index=model_names)
df_results

# %%
for model_name in model_names:
    pred = df_results.loc[model_name]["PRED"]
    print(f"Histogram of Y_pred(red) VS Y_true(blue) for {model_name}")
    sns.histplot(pred, color="red", alpha=0.5, bins=50)
    sns.histplot(y_val, color="blue", alpha=0.5, bins=50)
    plt.show()


# %% [markdown]
# #### GradientBoostingRegressor - chosen model
# Best RMSE without parameter tuning - 0.272639
# 
# ### Parameter tuning
# I will use GridSearchCV.  
# It is a hyperparameter tuning technique that exhaustively searches through a specified hyperparameter grid and  
# finds the best combination of hyperparameters.

# %%
# This took 20 minutes to complete

param_grid = {
    'n_estimators': [10, 20, 30, 40, 50],
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [1, 3, 4, 6, 10],
    'min_samples_leaf': [1, 3, 5, 10, 50],
}
# model_two = GradientBoostingRegressor()

# grid_search_two = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='neg_root_mean_squared_error')
# grid_search_two.fit(X_train, y_train)
# This took 20 minutes to complete

# %% [markdown]
# Results from Grid Search 
# 
# The best estimator across ALL searched params:
# GradientBoostingRegressor(learning_rate=0.3, max_depth=10, n_estimators=50)
# 
# The best parameters across ALL searched params:
# {'learning_rate': 0.3, 'max_depth': 10, 'min_samples_leaf': 1, 'n_estimators': 50}
# 
# The best RMSE across all searched params is 0.18673196751275872, which is significant improvement from 0.272639 (without parameter tuning)

# %%
best_params = {'learning_rate': 0.3, 'max_depth': 10, 'min_samples_leaf': 1, 'n_estimators': 50}
model = GradientBoostingRegressor(**best_params, random_state=random_seed)
model.fit(X_train, y_train)

# %%
y_pred = model.predict(X_val)
# Measure predictive performance 
mse = mean_squared_error(y_val, y_pred)
model_rmse = np.sqrt(mse)
print(model_rmse)
# Training best model with best params gives RMSE~0.2


# %% [markdown]
# ## Final model
# 
# Get the final model with best params and full training data

# %%
df_full_train.reset_index(drop=True)
y_full_train = np.log1p(df_full_train.hg_ha_yield.values)

del df_full_train["hg_ha_yield"]

print("Training final model")
# %%
dicts_full_train = df_full_train.to_dict(orient="records")
dv = DictVectorizer(sparse=False)
X_full_train = dv.fit_transform(dicts_full_train)

dicts_test = df_test.to_dict(orient="records")
X_test = dv.transform(dicts_test)

# %%
best_params = {'learning_rate': 0.3, 'max_depth': 10, 'min_samples_leaf': 1, 'n_estimators': 50}
best_model = GradientBoostingRegressor(**best_params, random_state=random_seed)
best_model.fit(X_full_train, y_full_train)

# %%
y_pred = model.predict(X_test)
# Measure predictive performance 
mse = mean_squared_error(y_test, y_pred)
best_model_rmse = np.sqrt(mse)
print(f"Best model RMSE is {best_model_rmse}")
# Training best model with best params gives RMSE~0.19


# %% [markdown]
# ### Testing model performance for individual cases

# %%
import random

idx = random.randint(1, len(df_test))
random_yield_data = df_test.iloc[idx].to_dict()
actual_yield = np.expm1(y_test[idx])

X_random_yield = dv.transform([random_yield_data])
predicted_log1p_yield = best_model.predict(X_random_yield)
predicted_yield = np.expm1(predicted_log1p_yield)[0]

print("Actual yield", actual_yield)
print("Predicted yield", predicted_yield)
print("Difference in between predicted and actual yield, Absolute numbers", abs(actual_yield - predicted_yield))
print("Difference in between predicted and actual yield, as Percentage", abs(actual_yield - predicted_yield)/ actual_yield * 100)



# %% [markdown]
# # Saving the model

# %%
import pickle

output_file_name = "model.bin"
# Open file and instruct that we will "wb" = Write Bytes (not text)
with open(output_file_name, "wb") as f_out:
    # Need also DictVectorizer, otherwise won't be able to translate a customer to feature matrix
    pickle.dump((dv, best_model), f_out)

print(f"The model is saved to {output_file_name}")
