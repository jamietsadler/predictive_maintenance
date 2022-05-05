This notebook aims to predict the remaining useful life (RUL) of engines using operational & sensor reading data, provided by NASA via Kaggle. 

It will start by exploring the data using statistics and visualisations, before moving onto modelling the data. The aim o the Kaggle conmpetition is simply to predict if an engine has failed or not (i.e. RUL is 0). However, there are numerous ways in which this can be achieved. A range of models have been employed in this analysis.

The data will be modelled in 2 main ways:

**1. Regression:**

This will aim to predict a continuous value for RUL. Models will be assessed on their ability to closely match the RUL of engines.

**2. Classification:**

For this, the data will have to be classified using the RUL feature. if the RUL is above 0, then the engines are still active (data labelled 0), otherwise, the engine has failed (data labelled 1). Due to the large disparity in class size, accuracy metrics are initially expected to be poor.
