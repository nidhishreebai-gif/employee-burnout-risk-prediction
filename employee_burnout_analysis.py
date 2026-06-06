# Employee Burnout Risk Prediction System
# Machine Learning Internship Assignment
# Author: ML Intern
# Date: 2026

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# ============================================================================
# PHASE 1: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================

def load_and_explore_data(file_path):
    """Load dataset and perform initial exploration"""
    print("="*80)
    print("PHASE 1: EXPLORATORY DATA ANALYSIS")
    print("="*80)
    
    # Load data
    df = pd.read_csv(file_path)
    print(f"\n✓ Dataset loaded successfully!")
    print(f"  Shape: {df.shape} (Rows, Columns)")
    
    # Display basic info
    print("\n" + "="*80)
    print("1. DATASET OVERVIEW")
    print("="*80)
    print(f"\nDataset Dimensions: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    
    # Data types
    print("\n" + "="*80)
    print("2. DATA TYPES")
    print("="*80)
    print(f"\n{df.dtypes}")
    
    # Missing values
    print("\n" + "="*80)
    print("3. MISSING VALUES ANALYSIS")
    print("="*80)
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("\n✓ No missing values found in the dataset!")
    else:
        print(f"\nMissing Values:\n{missing[missing > 0]}")
    
    # Statistical summary
    print("\n" + "="*80)
    print("4. STATISTICAL SUMMARY")
    print("="*80)
    print(f"\n{df.describe().round(2)}")
    
    return df

def perform_correlation_analysis(df):
    """Analyze correlations with target variable"""
    print("\n" + "="*80)
    print("5. CORRELATION ANALYSIS")
    print("="*80)
    
    # Correlation with target
    correlation_with_target = df.corr()['burnout_risk_score'].sort_values(ascending=False)
    print(f"\nFeature Correlation with Burnout Risk Score:\n{correlation_with_target.round(3)}")
    
    # Create correlation heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap - All Features', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('01_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("\n✓ Correlation heatmap saved as '01_correlation_heatmap.png'")
    plt.close()
    
    return correlation_with_target

def visualize_distributions(df):
    """Create distribution visualizations"""
    print("\n" + "="*80)
    print("6. DISTRIBUTION ANALYSIS")
    print("="*80)
    
    # Histograms for all features including target
    num_plots = len(df.columns)
    cols = 3
    rows = int(np.ceil(num_plots / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
    axes = axes.ravel()
    
    for idx, col in enumerate(df.columns):
        axes[idx].hist(df[col], bins=30, color='skyblue' if col != 'burnout_risk_score' else 'salmon', edgecolor='black')
        axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
        axes[idx].set_xlabel('Value')
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(alpha=0.3)
    
    for idx in range(num_plots, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('02_feature_distributions.png', dpi=300, bbox_inches='tight')
    print("✓ Distribution plots saved as '02_feature_distributions.png'")
    plt.close()

def identify_outliers(df):
    """Identify outliers using IQR method"""
    print("\n" + "="*80)
    print("7. OUTLIER DETECTION")
    print("="*80)
    
    feature_cols = list(df.columns)
    num_plots = len(feature_cols)
    cols = 3
    rows = int(np.ceil(num_plots / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
    axes = axes.ravel()
    
    outlier_counts = {}
    
    for idx, col in enumerate(feature_cols):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_counts[col] = len(outliers)
        
        axes[idx].boxplot(df[col])
        axes[idx].set_title(f'Box Plot: {col}', fontweight='bold')
        axes[idx].set_ylabel('Value')
        axes[idx].grid(alpha=0.3)
    
    for idx in range(num_plots, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('03_outlier_boxplots.png', dpi=300, bbox_inches='tight')
    print("✓ Outlier detection plots saved as '03_outlier_boxplots.png'")
    
    print(f"\nOutlier Count by Feature:")
    for col, count in outlier_counts.items():
        if count > 0:
            print(f"  {col}: {count} outliers")
    plt.close()

def create_scatter_plots(df):
    """Create scatter plots for top features vs target"""
    print("\n" + "="*80)
    print("8. SCATTER PLOT ANALYSIS")
    print("="*80)
    
    correlation_with_target = df.corr()['burnout_risk_score'].drop('burnout_risk_score').abs().sort_values(ascending=False)
    top_features = correlation_with_target.head(6).index.tolist()
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(top_features):
        axes[idx].scatter(df[feature], df['burnout_risk_score'], alpha=0.5, color='steelblue')
        axes[idx].set_xlabel(feature, fontweight='bold')
        axes[idx].set_ylabel('Burnout Risk Score', fontweight='bold')
        axes[idx].set_title(f'{feature} vs Burnout Risk', fontweight='bold')
        axes[idx].grid(alpha=0.3)
        
        # Add trend line
        z = np.polyfit(df[feature], df['burnout_risk_score'], 1)
        p = np.poly1d(z)
        axes[idx].plot(df[feature].sort_values(), p(df[feature].sort_values()), 
                      "r--", linewidth=2, label='Trend')
        axes[idx].legend()
    
    plt.tight_layout()
    plt.savefig('04_scatter_plots_top_features.png', dpi=300, bbox_inches='tight')
    print("✓ Scatter plots saved as '04_scatter_plots_top_features.png'")
    plt.close()

# ============================================================================
# PHASE 2: DATA PREPROCESSING
# ============================================================================

def preprocess_data(df):
    """Prepare data for model training"""
    print("\n" + "="*80)
    print("PHASE 2: DATA PREPROCESSING")
    print("="*80)
    
    # Create a copy
    df_processed = df.copy()
    
    # Remove employee_id (not needed for prediction)
    print("\n1. Removing unnecessary columns...")
    df_processed = df_processed.drop('employee_id', axis=1)
    print("   ✓ Removed 'employee_id' column")
    
    # Feature selection - use all remaining features
    print("\n2. Feature Selection...")
    feature_cols = [col for col in df_processed.columns if col != 'burnout_risk_score']
    target_col = 'burnout_risk_score'
    
    X = df_processed[feature_cols]
    y = df_processed[target_col]
    
    print(f"   ✓ Selected {len(feature_cols)} features for prediction")
    print(f"   Features: {feature_cols}")
    
    return X, y, feature_cols

def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets"""
    print("\n3. Train-Test Split...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"   ✓ Training set size: {X_train.shape[0]} samples ({(1-test_size)*100:.1f}%)")
    print(f"   ✓ Testing set size: {X_test.shape[0]} samples ({test_size*100:.1f}%)")
    
    return X_train, X_test, y_train, y_test

# ============================================================================
# PHASE 3: MODEL DEVELOPMENT
# ============================================================================

def build_linear_regression_model(X_train, y_train):
    """Build and train Linear Regression model"""
    print("\n" + "="*80)
    print("PHASE 3: MODEL DEVELOPMENT - LINEAR REGRESSION")
    print("="*80)
    
    print("\n1. Model Training...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("   ✓ Model trained successfully!")
    
    return model

def display_model_coefficients(model, feature_cols):
    """Display and interpret model coefficients"""
    print("\n2. Model Coefficients and Interpretation")
    print("-" * 80)
    
    coefficients = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', ascending=False)
    
    print(f"\nIntercept: {model.intercept_:.4f}")
    print("\nFeature Coefficients (Sorted by Impact):")
    print(coefficients.to_string(index=False))
    
    print("\n" + "-" * 80)
    print("INTERPRETATION:")
    print("-" * 80)
    
    for idx, row in coefficients.iterrows():
        feature = row['Feature']
        coef = row['Coefficient']
        direction = "INCREASES" if coef > 0 else "DECREASES"
        magnitude = abs(coef)
        
        print(f"• {feature}: {direction} burnout by {magnitude:.4f} per unit increase")
    
    return coefficients

# ============================================================================
# PHASE 4: MODEL EVALUATION
# ============================================================================

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance using standard metrics"""
    print("\n" + "="*80)
    print("PHASE 4: MODEL EVALUATION")
    print("="*80)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Display results
    print("\n" + "="*80)
    print("EVALUATION METRICS")
    print("="*80)
    print(f"\n1. Mean Absolute Error (MAE): {mae:.4f}")
    print(f"   → On average, predictions are off by {mae:.2f} burnout points")
    
    print(f"\n2. Mean Squared Error (MSE): {mse:.4f}")
    print(f"   → Average squared error in predictions")
    
    print(f"\n3. Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"   → Square root of MSE, in same units as target variable")
    
    print(f"\n4. R² Score: {r2:.4f}")
    print(f"   → Model explains {r2*100:.2f}% of the variance in burnout risk")
    
    # Model interpretation
    print("\n" + "="*80)
    print("MODEL INTERPRETATION")
    print("="*80)
    if r2 > 0.8:
        quality = "EXCELLENT"
    elif r2 > 0.6:
        quality = "GOOD"
    elif r2 > 0.4:
        quality = "MODERATE"
    else:
        quality = "WEAK"
    
    print(f"\nModel Quality: {quality}")
    print(f"• The model's predictive power is {quality.lower()}")
    print(f"• For every 1-point error in predictions, employees face ~{rmse:.2f} burnout units")
    
    # Visualize predictions vs actual
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scatter plot
    axes[0].scatter(y_test, y_pred, alpha=0.5, color='steelblue')
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0].set_xlabel('Actual Burnout Risk Score', fontweight='bold')
    axes[0].set_ylabel('Predicted Burnout Risk Score', fontweight='bold')
    axes[0].set_title('Actual vs Predicted Values', fontweight='bold')
    axes[0].grid(alpha=0.3)
    
    # Residuals
    residuals = y_test - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.5, color='coral')
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Predicted Burnout Risk Score', fontweight='bold')
    axes[1].set_ylabel('Residuals', fontweight='bold')
    axes[1].set_title('Residual Plot', fontweight='bold')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('05_model_evaluation.png', dpi=300, bbox_inches='tight')
    print("\n✓ Evaluation plots saved as '05_model_evaluation.png'")
    plt.close()
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'predictions': y_pred,
        'residuals': residuals
    }

# ============================================================================
# PHASE 5: BUSINESS INSIGHTS
# ============================================================================

def extract_business_insights(df, model, feature_cols, coefficients):
    """Generate actionable business insights"""
    print("\n" + "="*80)
    print("PHASE 5: BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("="*80)
    
    print("\n1. TOP FACTORS AFFECTING BURNOUT")
    print("-" * 80)
    
    top_positive = coefficients[coefficients['Coefficient'] > 0].head(3)
    top_negative = coefficients[coefficients['Coefficient'] < 0].head(3)
    
    print("\n✗ FACTORS THAT INCREASE BURNOUT RISK:")
    for idx, row in top_positive.iterrows():
        print(f"   • {row['Feature']}: +{row['Coefficient']:.4f} per unit")
    
    print("\n✓ FACTORS THAT DECREASE BURNOUT RISK:")
    for idx, row in top_negative.iterrows():
        print(f"   • {row['Feature']}: {row['Coefficient']:.4f} per unit")
    
    print("\n2. VULNERABLE EMPLOYEE SEGMENTS")
    print("-" * 80)
    
    # Predict on full dataset
    X_full = df[feature_cols]
    burnout_predictions = model.predict(X_full)
    
    # Add predictions to dataframe
    df_analysis = df.copy()
    df_analysis['predicted_burnout'] = burnout_predictions
    
    # High risk employees
    high_risk = df_analysis[df_analysis['predicted_burnout'] > df_analysis['predicted_burnout'].quantile(0.75)]
    print(f"\nHigh-Risk Employees (>75th percentile):")
    print(f"   • Count: {len(high_risk)}")
    print(f"   • Average Predicted Burnout: {high_risk['predicted_burnout'].mean():.2f}")
    print(f"   • Average Work Hours: {high_risk['weekly_work_hours'].mean():.2f}")
    print(f"   • Average Sleep Hours: {high_risk['sleep_hours'].mean():.2f}")
    print(f"   • Average Stress Level: {high_risk['stress_level'].mean():.2f}")
    
    print("\n3. STATISTICAL INSIGHTS")
    print("-" * 80)
    
    # Correlation analysis
    corr_with_burnout = df.corr()['burnout_risk_score'].sort_values(ascending=False)
    print(f"\nStrongest Positive Correlations with Burnout:")
    for feature, corr in corr_with_burnout.head(4).items():
        if feature != 'burnout_risk_score':
            print(f"   • {feature}: {corr:.4f}")
    
    print(f"\nStrongest Negative Correlations with Burnout:")
    for feature, corr in corr_with_burnout.tail(3).items():
        print(f"   • {feature}: {corr:.4f}")
    
    return df_analysis, high_risk

def generate_recommendations(high_risk, df):
    """Generate HR recommendations based on analysis"""
    print("\n4. ACTIONABLE HR RECOMMENDATIONS")
    print("-" * 80)
    
    print("\n✓ IMMEDIATE ACTIONS:")
    print(f"   1. Identify and monitor {len(high_risk)} high-risk employees")
    print(f"      - Schedule one-on-one meetings with them")
    print(f"      - Assess their current workload and well-being")
    
    avg_work_hours = df['weekly_work_hours'].mean()
    high_risk_work_hours = high_risk['weekly_work_hours'].mean()
    if high_risk_work_hours > avg_work_hours:
        print(f"\n   2. Reduce Work Hours")
        print(f"      - High-risk employees average {high_risk_work_hours:.1f} hours/week")
        print(f"      - Organizational average: {avg_work_hours:.1f} hours/week")
        print(f"      - Recommend workload reduction by 10-15%")
    
    avg_sleep = df['sleep_hours'].mean()
    high_risk_sleep = high_risk['sleep_hours'].mean()
    if high_risk_sleep < avg_sleep:
        print(f"\n   3. Promote Better Sleep Habits")
        print(f"      - High-risk employees average {high_risk_sleep:.1f} hours sleep/night")
        print(f"      - Organizational average: {avg_sleep:.1f} hours/night")
        print(f"      - Recommend flexible work schedules to improve sleep")
    
    avg_exercise = df['exercise_hours_week'].mean()
    high_risk_exercise = high_risk['exercise_hours_week'].mean()
    if high_risk_exercise < avg_exercise:
        print(f"\n   4. Encourage Physical Activity")
        print(f"      - High-risk employees exercise {high_risk_exercise:.1f} hours/week")
        print(f"      - Organizational average: {avg_exercise:.1f} hours/week")
        print(f"      - Sponsor gym memberships or wellness programs")
    
    avg_stress = df['stress_level'].mean()
    high_risk_stress = high_risk['stress_level'].mean()
    if high_risk_stress > avg_stress:
        print(f"\n   5. Stress Management Programs")
        print(f"      - High-risk employees report {high_risk_stress:.1f} stress level")
        print(f"      - Organizational average: {avg_stress:.1f}")
        print(f"      - Offer meditation, counseling, or mental health support")
    
    print(f"\n✓ PREVENTIVE MEASURES:")
    print(f"   • Implement wellness programs for all employees")
    print(f"   • Regular check-ins on workload and well-being")
    print(f"   • Promote work-life balance through policies")
    print(f"   • Monitor burnout metrics monthly")

# ============================================================================
# BONUS: SCENARIO ANALYSIS
# ============================================================================

def scenario_analysis(model, df, feature_cols, original_coef):
    """Perform scenario simulations"""
    print("\n" + "="*80)
    print("BONUS: SCENARIO ANALYSIS")
    print("="*80)
    
    X = df[feature_cols]
    baseline_prediction = model.predict(X).mean()
    
    print(f"\nBaseline Average Burnout Risk: {baseline_prediction:.4f}")
    print("-" * 80)
    
    # Scenario 1: Reduce work hours by 10%
    print("\nSCENARIO 1: Reduce Weekly Work Hours by 10%")
    X_scenario1 = X.copy()
    X_scenario1['weekly_work_hours'] = X_scenario1['weekly_work_hours'] * 0.9
    scenario1_prediction = model.predict(X_scenario1).mean()
    scenario1_change = ((scenario1_prediction - baseline_prediction) / baseline_prediction) * 100
    
    print(f"   Original avg work hours: {X['weekly_work_hours'].mean():.2f}")
    print(f"   New avg work hours: {X_scenario1['weekly_work_hours'].mean():.2f}")
    print(f"   New avg burnout risk: {scenario1_prediction:.4f}")
    print(f"   Change: {scenario1_change:+.2f}%")
    print(f"   Impact: Reduces burnout by {baseline_prediction - scenario1_prediction:.4f} points")
    
    # Scenario 2: Increase sleep by 1 hour
    print("\nSCENARIO 2: Increase Daily Sleep by 1 Hour")
    X_scenario2 = X.copy()
    X_scenario2['sleep_hours'] = X_scenario2['sleep_hours'] + 1
    scenario2_prediction = model.predict(X_scenario2).mean()
    scenario2_change = ((scenario2_prediction - baseline_prediction) / baseline_prediction) * 100
    
    print(f"   Original avg sleep: {X['sleep_hours'].mean():.2f} hours/night")
    print(f"   New avg sleep: {X_scenario2['sleep_hours'].mean():.2f} hours/night")
    print(f"   New avg burnout risk: {scenario2_prediction:.4f}")
    print(f"   Change: {scenario2_change:+.2f}%")
    print(f"   Impact: Reduces burnout by {baseline_prediction - scenario2_prediction:.4f} points")
    
    # Scenario 3: Increase exercise by 3 hours/week
    print("\nSCENARIO 3: Increase Weekly Exercise by 3 Hours")
    X_scenario3 = X.copy()
    X_scenario3['exercise_hours_week'] = X_scenario3['exercise_hours_week'] + 3
    scenario3_prediction = model.predict(X_scenario3).mean()
    scenario3_change = ((scenario3_prediction - baseline_prediction) / baseline_prediction) * 100
    
    print(f"   Original avg exercise: {X['exercise_hours_week'].mean():.2f} hours/week")
    print(f"   New avg exercise: {X_scenario3['exercise_hours_week'].mean():.2f} hours/week")
    print(f"   New avg burnout risk: {scenario3_prediction:.4f}")
    print(f"   Change: {scenario3_change:+.2f}%")
    print(f"   Impact: Reduces burnout by {baseline_prediction - scenario3_prediction:.4f} points")
    
    # Visualize scenarios
    scenarios = ['Baseline', 'Reduce Work\nHours 10%', 'Increase Sleep\n1 Hour', 'Increase\nExercise 3hrs']
    predictions = [baseline_prediction, scenario1_prediction, scenario2_prediction, scenario3_prediction]
    colors = ['gray', 'green', 'blue', 'orange']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scenarios, predictions, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, pred in zip(bars, predictions):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{pred:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.ylabel('Average Burnout Risk Score', fontweight='bold', fontsize=12)
    plt.title('Scenario Analysis: Impact on Burnout Risk', fontweight='bold', fontsize=14)
    plt.ylim(0, max(predictions) * 1.15)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('06_scenario_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Scenario analysis plot saved as '06_scenario_analysis.png'")
    plt.close()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    # Load and explore data
    df = load_and_explore_data('employee_data.csv')
    
    # Correlation analysis
    correlation = perform_correlation_analysis(df)
    
    # Visualizations
    visualize_distributions(df)
    identify_outliers(df)
    create_scatter_plots(df)
    
    # Data preprocessing
    X, y, feature_cols = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Model development
    model = build_linear_regression_model(X_train, y_train)
    coefficients = display_model_coefficients(model, feature_cols)
    
    # Model evaluation
    metrics = evaluate_model(model, X_test, y_test)
    
    # Business insights
    df_analysis, high_risk = extract_business_insights(df, model, feature_cols, coefficients)
    generate_recommendations(high_risk, df)
    
    # Scenario analysis
    scenario_analysis(model, df, feature_cols, model.coef_)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated Outputs:")
    print("  ✓ 01_correlation_heatmap.png")
    print("  ✓ 02_feature_distributions.png")
    print("  ✓ 03_outlier_boxplots.png")
    print("  ✓ 04_scatter_plots_top_features.png")
    print("  ✓ 05_model_evaluation.png")
    print("  ✓ 06_scenario_analysis.png")

if __name__ == "__main__":
    main()
