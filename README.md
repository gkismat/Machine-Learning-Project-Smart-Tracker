# Smart Tracker - Machine Learning Based Workout Tracking

## Overview
Smart Tracker is an advanced workout tracking system that uses machine learning to monitor fitness activities with precision. By leveraging multiple machine learning models, Smart Tracker not only tracks workouts but also counts repetitions, identifies exercise types, and distinguishes between exercise intensities such as medium and heavy squats. It offers a comprehensive solution to fitness tracking, helping users gain deeper insights into their performance and progress.

### Features
- **Accurate Workout Classification**: Achieves a 96% accuracy rate in workout classification using the Random Forest model.
- **Repetition and Intensity Tracking**: Accurately counts repetitions and differentiates exercise intensity for workouts like squats.
- **Data Cleaning and Preprocessing**: Handles missing values, detects and removes outliers, and applies feature engineering techniques like PCA to improve model performance.
- **Multi-Sensor Integration**: Combines data from accelerometers and gyroscopes for a detailed view of exercises.
- **Visualization**: Generates clear, insightful visualizations to compare participants, show exercise patterns, and analyze sensor data.

### Models Used
The system utilizes five machine learning models to classify workouts and perform other tasks:
- **Neural Networks (NN)**
- **K-Nearest Neighbors (KNN)**
- **Naive Bayes (NB)**
- **Random Forest (RF)** - Achieved 96% accuracy.
- **Decision Tree (DT)**

### Key Features and Contributions
1. **Enhanced Repetition Tracking**: Developed a system to count repetitions and classify the intensity of exercises.
2. **Comprehensive Data Analysis**: Designed a workflow for analyzing, visualizing, and comparing exercise patterns.
3. **Advanced Data Preprocessing**: Implemented techniques to clean and preprocess sensor data effectively.
4. **Workflow Automation**: Automated data merging, resampling, and exporting tasks.
5. **Participant-Specific Insights**: Enabled personalized insights by identifying trends in workout patterns.
6. **Multi-Sensor Data Integration**: Integrated accelerometer and gyroscope data for more accurate results.
7. **Customized Metrics**: Introduced unique metrics like set durations and intensity comparisons to offer actionable insights.

### Accuracy and Results
- **Model Accuracy**:
  - **Random Forest**: 96%
  - **Decision Tree**: 91-92%
  - **Neural Networks**: 90-91%
  - **K-Nearest Neighbors**: 81-83%
  - **Naive Bayes**: 76-77%
  
- **Exercise Classification Accuracy**:
  - **Squats**: 90%
  - **Bench Press**: 95%
  - **Overhead Press**: 93%
  - **Deadlifts**: 96%
  - **Rows**: 89%

### Challenges
- **Data Preprocessing**: Dealing with missing values and noisy sensor data.
- **Feature Engineering**: Reducing the dataset's dimensionality while retaining essential features.
- **Model Selection**: Choosing and fine-tuning the best model based on accuracy and performance.
- **Visualization**: Creating meaningful plots to represent complex data in an easy-to-understand manner.
- **Integration**: Combining data from multiple sensors and ensuring consistent workflows.

### Results and Insights
- **PCA Explained Variance**: The first three principal components capture over 90% of the variance in the dataset.
- **Optimal Clustering**: The elbow method suggests four clusters for optimal data grouping.
- **Heavy vs. Medium Squats**: Heavy squats exhibit larger peaks in accelerometer data, indicating higher intensity.
### Acknowledgments
**MiLift Paper:** Inspired by the paper "MiLift: Efficient Smartwatch-Based Workout Tracking Using Automatic Segmentation," IEEE Transactions on Mobile Computing.
Libraries Used: scikit-learn, matplotlib, pandas, numpy, and more.

