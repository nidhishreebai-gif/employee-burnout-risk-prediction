from flask import Flask, request, render_template_string, send_from_directory
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

app = Flask(__name__)

DATA_PATH = 'employee_data.csv'
FEATURES = [
    'age',
    'years_experience',
    'weekly_work_hours',
    'meetings_per_week',
    'emails_sent_per_day',
    'projects_handled',
    'remote_days_per_month',
    'sleep_hours',
    'stress_level',
    'exercise_hours_week',
    'sick_leaves_year',
    'productivity_score'
]
IMAGE_FILES = [
    ('Correlation Heatmap', '01_correlation_heatmap.png'),
    ('Feature Distributions', '02_feature_distributions.png'),
    ('Outlier Boxplots', '03_outlier_boxplots.png'),
    ('Scatter Plots', '04_scatter_plots_top_features.png'),
    ('Evaluation Charts', '05_model_evaluation.png'),
    ('Scenario Analysis', '06_scenario_analysis.png'),
]


def load_data_and_train():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df['burnout_risk_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metrics = {
        'mae': mean_absolute_error(y_test, y_pred),
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2': r2_score(y_test, y_pred),
        'train_size': X_train.shape[0],
        'test_size': X_test.shape[0],
    }
    coefficients = pd.Series(model.coef_, index=FEATURES).sort_values(ascending=False)
    defaults = X.mean().round(2).to_dict()
    return df, model, metrics, coefficients, defaults


df, model, metrics, coefficients, defaults = load_data_and_train()

TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Burnout Risk Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f7fb; color: #1f2937; }
    .container { width: 92%; max-width: 1100px; margin: 24px auto; }
    .header { padding: 24px 0; text-align: center; }
    .card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
    .grid { display: grid; gap: 18px; }
    .grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
    th { background: #f8fafc; }
    input[type=number] { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; }
    button { background: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 8px; cursor: pointer; }
    button:hover { background: #1d4ed8; }
    .small { font-size: 0.95rem; color: #6b7280; }
    .img-grid { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
    img { width: 100%; border-radius: 10px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Burnout Risk Prediction Dashboard</h1>
      <p class="small">Enter employee feature values and see the predicted burnout risk score.</p>
    </div>

    <div class="card">
      <h2>Prediction Form</h2>
      <form method="post">
        <div class="grid grid-3">
          {% for feature in features %}
          <div>
            <label><strong>{{ feature.replace('_', ' ').title() }}</strong></label>
            <input type="number" step="0.01" name="{{ feature }}" value="{{ form_values[feature] }}" required>
          </div>
          {% endfor %}
        </div>
        <div style="margin-top: 20px;"><button type="submit">Predict Burnout Risk</button></div>
      </form>
      {% if prediction is not none %}
      <div style="margin-top: 20px; padding: 18px; background: #ecfdf5; border: 1px solid #d1fae5; border-radius: 10px;">
        <h3>Predicted Burnout Risk Score</h3>
        <p style="font-size: 1.8rem; font-weight: bold; margin: 0;">{{ prediction | round(3) }}</p>
      </div>
      {% endif %}
    </div>

    <div class="card">
      <h2>Model Summary</h2>
      <div class="grid grid-2">
        <div><strong>Training set size:</strong> {{ metrics.train_size }}</div>
        <div><strong>Test set size:</strong> {{ metrics.test_size }}</div>
        <div><strong>MAE:</strong> {{ metrics.mae | round(3) }}</div>
        <div><strong>MSE:</strong> {{ metrics.mse | round(3) }}</div>
        <div><strong>RMSE:</strong> {{ metrics.rmse | round(3) }}</div>
        <div><strong>R² Score:</strong> {{ metrics.r2 | round(3) }}</div>
      </div>
    </div>

    <div class="card">
      <h2>Top Feature Coefficients</h2>
      <table>
        <thead><tr><th>Feature</th><th>Coefficient</th></tr></thead>
        <tbody>
          {% for feature, coef in coefficients.items() %}
          <tr><td>{{ feature.replace('_', ' ').title() }}</td><td>{{ coef | round(4) }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <div class="card">
      <h2>Generated Charts</h2>
      <div class="img-grid">
        {% for title, filename in images %}
        <div class="explain-card" data-title="{{ title }}">
          <h4 style="margin-bottom: 10px;">{{ title }}</h4>
          <img src="{{ url_for('serve_image', filename=filename) }}" alt="{{ title }}">
        </div>
        {% endfor %}
      </div>
      <div id="explanation-box" style="margin-top: 24px; padding: 18px; border-radius: 12px; background: #f9fafb; border: 1px solid #e5e7eb; min-height: 120px;">
        <h3 style="margin-top:0;">Scroll to learn more</h3>
        <p id="explanation-text" style="margin:0; color: #374151; line-height: 1.7;">As you move through the charts, I’ll explain what each one means and why it matters for burnout risk.</p>
      </div>
    </div>
  </div>
  <script>
    const explanations = {
      'Correlation Heatmap': 'This heatmap shows how each feature relates to the burnout risk score. Stronger colors tell us which factors are most closely linked to burnout, so we can target the right levers.',
      'Feature Distributions': 'These distribution plots show how the employee data is spread across each metric. It helps us see if values are clustered, skewed, or if there are extreme values that deserve attention.',
      'Outlier Boxplots': 'The boxplots identify unusual values in the dataset. I use these to see whether any employees have extreme values that might affect the model or signal special cases.',
      'Scatter Plots': 'These scatter plots compare top features against burnout score. They help me judge whether the relationships look linear and which features move together with higher burnout.',
      'Evaluation Charts': 'Here I compare actual versus predicted values and look at residuals. This tells us how well the model is performing and whether the predictions are consistently close to the real scores.',
      'Scenario Analysis': 'This chart illustrates what happens when we change a few workplace conditions. It helps show practical actions, like reducing work hours, that can lower burnout risk.'
    };

    const explanationText = document.getElementById('explanation-text');
    const cards = document.querySelectorAll('.explain-card');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const title = entry.target.getAttribute('data-title');
          explanationText.textContent = explanations[title] || 'Scroll through the charts and I will explain each one.';
        }
      });
    }, { threshold: 0.4 });

    cards.forEach(card => observer.observe(card));
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        TEMPLATE,
        features=FEATURES,
        prediction=None,
        metrics=metrics,
        coefficients=coefficients,
        images=IMAGE_FILES,
        form_values=defaults,
    )

@app.route('/', methods=['POST'])
def predict():
    values = {}
    for feature in FEATURES:
        raw_value = request.form.get(feature, '')
        try:
            values[feature] = float(raw_value)
        except ValueError:
            values[feature] = defaults[feature]

    x = np.array([values[feature] for feature in FEATURES]).reshape(1, -1)
    prediction = float(model.predict(x)[0])

    return render_template_string(
        TEMPLATE,
        features=FEATURES,
        prediction=prediction,
        metrics=metrics,
        coefficients=coefficients,
        images=IMAGE_FILES,
        form_values={**defaults, **values},
    )

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
