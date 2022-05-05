{\rtf1\ansi\ansicpg1252\cocoartf2576
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;\f1\fmodern\fcharset0 Courier-Bold;}
{\colortbl;\red255\green255\blue255;\red202\green202\blue202;\red23\green23\blue23;}
{\*\expandedcolortbl;;\cssrgb\c83137\c83137\c83137;\cssrgb\c11765\c11765\c11765;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\sl380\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 This notebook aims to predict the remaining useful life (RUL) of engines using operational & sensor reading data, provided by NASA via Kaggle. \cb1 \
\
\cb3 It will start by exploring the data using statistics and visualisations, before moving onto modelling the data. The aim o the Kaggle conmpetition is simply to predict if an engine has failed or not (i.e. RUL is 0). However, there are numerous ways in which this can be achieved. A range of models have been employed in this analysis.\cb1 \
\
\cb3 The data will be modelled in 2 main ways:\cb1 \
\
\pard\pardeftab720\sl380\partightenfactor0

\f1\b \cf2 \cb3 **1. Regression:**
\f0\b0 \cb1 \
\
\pard\pardeftab720\sl380\partightenfactor0
\cf2 \cb3 This will aim to predict a continuous value for RUL. Models will be assessed on their ability to closely match the RUL of engines.\cb1 \
\
\pard\pardeftab720\sl380\partightenfactor0

\f1\b \cf2 \cb3 **2. Classification:**
\f0\b0 \cb1 \
\
\pard\pardeftab720\sl380\partightenfactor0
\cf2 \cb3 For this, the data will have to be classified using the RUL feature. if the RUL is above 0, then the engines are still active (data labelled 0), otherwise, the engine has failed (data labelled 1). Due to the large disparity in class size, accuracy metrics are initially expected to be poor.\cb1 \
}