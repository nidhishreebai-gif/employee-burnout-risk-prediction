# 📊 Employee Burnout Dataset - Complete Guide

## Overview
- **Dataset Size**: 1,000 employee records
- **Total Features**: 14 (13 input + 1 target)
- **Data Type**: CSV (Comma-Separated Values)
- **Missing Values**: NONE - Clean dataset!
- **Time Period**: Snapshot (static snapshot, not time-series)

---

## Feature Dictionary

### **ID & Demographics**

#### **1. employee_id**
- **Type**: Integer (Unique identifier)
- **Range**: 1-1000
- **Meaning**: Unique identifier for each employee
- **Use**: REMOVE before modeling (not predictive)
- **Example**: employee_id = 42

#### **2. age**
- **Type**: Integer (Years)
- **Range**: 22-59 years
- **Meaning**: Employee's chronological age
- **Business Insight**: Younger employees might have different burnout patterns than older ones
- **Example**: age = 35 (35-year-old employee)
- **Expected Impact**: Unclear (age could increase or decrease burnout)

#### **3. years_experience**
- **Type**: Integer (Years)
- **Range**: 0-34 years
- **Meaning**: Years working in their field/role
- **Business Insight**: 
  - New employees (0-2 years): May experience learning stress
  - Mid-career (5-15 years): Established, lower stress
  - Senior (15+ years): High responsibility, might be higher stress
- **Example**: years_experience = 10 (10 years in field)
- **Expected Impact**: Likely NEGATIVE (more experience = less burnout)

---

### **Work-Related Features**

#### **4. weekly_work_hours**
- **Type**: Integer (Hours)
- **Range**: 30-74 hours/week
- **Meaning**: Average hours worked per week
- **Business Insight**: 
  - 30-40 hours: Normal/part-time
  - 40-50 hours: Full-time standard
  - 50-60 hours: Overtime
  - 60+ hours: Excessive (likely high burnout)
- **Example**: weekly_work_hours = 50
- **Expected Impact**: POSITIVE (more hours = more burnout) 🔴

#### **5. meetings_per_week**
- **Type**: Integer (Count)
- **Range**: 2-24 meetings
- **Meaning**: Number of meetings attended per week
- **Business Insight**:
  - 2-5 meetings: Low, focused work time
  - 10-15 meetings: Moderate, meeting-heavy
  - 20+ meetings: Very high, constant interruptions
- **Example**: meetings_per_week = 12
- **Expected Impact**: POSITIVE (more meetings = more burnout) 🔴

#### **6. emails_sent_per_day**
- **Type**: Integer (Count)
- **Range**: 10-199 emails/day
- **Meaning**: Daily email volume sent by employee
- **Business Insight**:
  - Low (10-50): Administrative/technical roles
  - Medium (50-100): Managerial/collaborative roles
  - High (100+): Highly collaborative/chaotic environment
- **Example**: emails_sent_per_day = 85
- **Expected Impact**: POSITIVE (more emails = more burnout) 🔴

#### **7. projects_handled**
- **Type**: Integer (Count)
- **Range**: 1-9 projects
- **Meaning**: Number of active projects employee manages
- **Business Insight**:
  - 1-2 projects: Focused, sustainable
  - 3-5 projects: Moderate multi-tasking
  - 6+ projects: Heavy multitasking, likely stress
- **Example**: projects_handled = 4
- **Expected Impact**: POSITIVE (more projects = more burnout) 🔴

#### **8. remote_days_per_month**
- **Type**: Integer (Days)
- **Range**: 0-19 days/month
- **Meaning**: Days worked from home per month
- **Business Insight**:
  - 0 days: 100% office-based
  - 5-10 days: Hybrid (balanced)
  - 15+ days: Mostly remote
- **Example**: remote_days_per_month = 10
- **Expected Impact**: NEGATIVE (more remote = less burnout) 🟢
  - Reasoning: No commute, flexible schedule, work-life balance

---

### **Lifestyle & Well-being Features**

#### **9. sleep_hours**
- **Type**: Float (Hours)
- **Range**: 4.0-9.0 hours/night
- **Meaning**: Average hours of sleep per night
- **Business Insight**:
  - <5 hours: Sleep deprived, high fatigue
  - 5-7 hours: Below recommended
  - 7-9 hours: Recommended amount
  - 9+ hours: Potentially oversleeping (depression indicator)
- **Example**: sleep_hours = 6.5
- **Expected Impact**: NEGATIVE (more sleep = less burnout) 🟢

#### **10. stress_level**
- **Type**: Integer (1-10 Scale)
- **Range**: 1-10
- **Meaning**: Self-reported stress level (1=no stress, 10=extreme stress)
- **Business Insight**:
  - 1-3: Low stress, relaxed
  - 4-6: Moderate stress, manageable
  - 7-10: High stress, concerning
- **Example**: stress_level = 7
- **Expected Impact**: POSITIVE (higher stress = higher burnout) 🔴

#### **11. exercise_hours_week**
- **Type**: Float (Hours)
- **Range**: 0.0-10.0 hours/week
- **Meaning**: Weekly exercise/physical activity
- **Business Insight**:
  - 0-2 hours: Sedentary
  - 3-5 hours: Recommended (WHO guideline: 150 min/week = 2.5 hours)
  - 6+ hours: Very active
- **Example**: exercise_hours_week = 3.5
- **Expected Impact**: NEGATIVE (more exercise = less burnout) 🟢

#### **12. sick_leaves_year**
- **Type**: Integer (Days)
- **Range**: 0-14 days/year
- **Meaning**: Number of sick days taken in a year
- **Business Insight**:
  - 0-2 days: Rarely ill (healthy/resilient)
  - 3-7 days: Average illness frequency
  - 8-14 days: Frequently ill (burnout indicator - physical symptoms)
- **Example**: sick_leaves_year = 5
- **Expected Impact**: POSITIVE (more sick days = more underlying burnout) 🔴

---

### **Performance Features**

#### **13. productivity_score**
- **Type**: Integer (0-100 Scale)
- **Range**: 40-99
- **Meaning**: Work output quality/quantity rating (0=no productivity, 100=perfect)
- **Business Insight**:
  - 40-60: Low productivity (might indicate burnout)
  - 60-80: Moderate productivity
  - 80-99: High productivity
- **Example**: productivity_score = 75
- **Expected Impact**: NEGATIVE (higher productivity = less burnout) 🟢
  - Logic: Burned out employees are less productive

---

### **TARGET VARIABLE** 🎯

#### **14. burnout_risk_score** ← THIS IS WHAT WE PREDICT!
- **Type**: Float
- **Range**: 0.0-51.78
- **Meaning**: Estimated burnout risk score (0=no risk, 100=extreme risk)
- **Distribution**: Most employees have score 0-20, some have extreme values (30+)
- **Example**: burnout_risk_score = 15.5 (moderate burnout risk)

**This is what your model will predict for new employees!**

---

## Feature Analysis for Your Model

### **Predicted Positive Impact on Burnout** (Increase Burnout)
These features likely increase burnout risk:
- ✗ weekly_work_hours (work more → burnout more)
- ✗ meetings_per_week (more meetings → stress)
- ✗ emails_sent_per_day (email overload → stress)
- ✗ projects_handled (more projects → overwhelm)
- ✗ stress_level (stressed → burned out)
- ✗ sick_leaves_year (illness from burnout)

**Model Insight:** Workload and stress are the main burnout drivers

### **Predicted Negative Impact on Burnout** (Decrease Burnout)
These features likely reduce burnout risk:
- ✓ remote_days_per_month (flexibility helps)
- ✓ sleep_hours (rest reduces stress)
- ✓ exercise_hours_week (physical activity helps)
- ✓ productivity_score (good performers less burned out)
- ✓ years_experience (experience helps manage stress)

**Model Insight:** Work-life balance and well-being are protective factors

### **Ambiguous Features** (Unclear Direction)
- ? age (could go either way)
- ? years_experience (new workers might be stressed, but so are senior workers with high responsibility)

---

## Data Quality Assessment

### **Missing Values**
```
employee_id:           0 missing ✓
age:                   0 missing ✓
years_experience:      0 missing ✓
weekly_work_hours:     0 missing ✓
meetings_per_week:     0 missing ✓
emails_sent_per_day:   0 missing ✓
projects_handled:      0 missing ✓
remote_days_per_month: 0 missing ✓
sleep_hours:           0 missing ✓
stress_level:          0 missing ✓
exercise_hours_week:   0 missing ✓
sick_leaves_year:      0 missing ✓
productivity_score:    0 missing ✓
burnout_risk_score:    0 missing ✓

TOTAL: 100% COMPLETE - NO MISSING VALUES! 🎉
```

### **Data Type Assessment**

| Feature | Type | Status |
|---------|------|--------|
| employee_id | int64 | ✓ Correct |
| age | int64 | ✓ Correct |
| years_experience | int64 | ✓ Correct |
| weekly_work_hours | int64 | ✓ Correct |
| meetings_per_week | int64 | ✓ Correct |
| emails_sent_per_day | int64 | ✓ Correct |
| projects_handled | int64 | ✓ Correct |
| remote_days_per_month | int64 | ✓ Correct |
| sleep_hours | float64 | ✓ Correct |
| stress_level | int64 | ✓ Correct |
| exercise_hours_week | float64 | ✓ Correct |
| sick_leaves_year | int64 | ✓ Correct |
| productivity_score | int64 | ✓ Correct |
| burnout_risk_score | float64 | ✓ Correct |

---

## Sample Employee Profiles

### **Profile A: Low Burnout Employee** 
Burnout Risk Score: 0.0
```
age:                    35
years_experience:       10
weekly_work_hours:      40     ← Reasonable
meetings_per_week:       5     ← Few interruptions
emails_sent_per_day:     50    ← Manageable volume
projects_handled:        2     ← Focused
remote_days_per_month:   10    ← Flexibility
sleep_hours:             8.0   ← Good sleep
stress_level:            2     ← Low stress
exercise_hours_week:     5.0   ← Active
sick_leaves_year:        0     ← Healthy
productivity_score:      90    ← High output
```
**Why low burnout?** Balanced workload, good sleep, low stress, time flexibility

### **Profile B: High Burnout Employee**
Burnout Risk Score: 45.0
```
age:                    28
years_experience:        2     ← New to field
weekly_work_hours:      74     ← Excessive! 🔴
meetings_per_week:      24     ← Constant interruptions! 🔴
emails_sent_per_day:    195    ← Email overload! 🔴
projects_handled:        7     ← Too many! 🔴
remote_days_per_month:   0     ← No flexibility
sleep_hours:             4.5   ← Sleep deprived! 🔴
stress_level:           10     ← Extreme stress! 🔴
exercise_hours_week:     0.2   ← No exercise! 🔴
sick_leaves_year:       14     ← Frequently ill! 🔴
productivity_score:      40    ← Very low output
```
**Why high burnout?** Overworked, poor sleep, high stress, no work-life balance

### **Profile C: Moderate Burnout Employee**
Burnout Risk Score: 18.0
```
age:                    45
years_experience:       15
weekly_work_hours:      55     ← Slightly high
meetings_per_week:      12     ← Moderate
emails_sent_per_day:    100    ← Busy
projects_handled:        4     ← Several
remote_days_per_month:   5     ← Some flexibility
sleep_hours:             6.0   ← Below recommended
stress_level:            6     ← Moderate-high
exercise_hours_week:     2.0   ← Minimal
sick_leaves_year:        8     ← Several
productivity_score:      70    ← Adequate
```
**Why moderate burnout?** Several stress factors present, but some coping mechanisms

---

## Key Statistics Summary

### **Numerical Ranges**

```
Feature                Min      Max      Mean     Std
───────────────────────────────────────────────────
age                     22       59      40.8      10.3
years_experience         0       34      15.2       11.1
weekly_work_hours       30       74      53.2       11.4
meetings_per_week        2       24      12.3        6.8
emails_sent_per_day     10      199     112.4       48.9
projects_handled         1        9       4.9        2.3
remote_days_per_month    0       19       9.8        6.5
sleep_hours             4.0      9.0      6.5        1.2
stress_level             1       10       5.7        2.8
exercise_hours_week     0.0     10.0      4.6        3.1
sick_leaves_year         0       14       6.9        4.5
productivity_score      40       99      71.3       16.8
burnout_risk_score      0.0     51.78     9.2       13.4
```

### **Key Observations**

1. **Burnout Distribution**: 
   - Most employees have low burnout (0-10)
   - Some have extreme burnout (30-50)
   - Average: 9.2 (relatively low for entire organization)

2. **Work Patterns**:
   - Average work hours: 53.2 (3-4 hours above standard 40)
   - Average emails: 112 per day (very high!)
   - Average projects: 4.9 (reasonable)

3. **Well-being**:
   - Average sleep: 6.5 hours (below 7-9 recommended)
   - Average exercise: 4.6 hours/week (slightly above WHO recommended 2.5)
   - Average stress: 5.7/10 (moderate)

4. **Performance**:
   - Average productivity: 71.3 (decent)
   - No clear pattern between productivity and burnout

---

## Data Insights for Model Building

### **Feature Importance (Predicted)**

Based on logic and typical HR patterns:

1. **Rank 1: stress_level** - Direct indicator
2. **Rank 2: weekly_work_hours** - Core burnout driver
3. **Rank 3: sleep_hours** - Critical for well-being
4. **Rank 4: meetings_per_week** - Time fragmentation
5. **Rank 5: emails_sent_per_day** - Workload indicator

### **Preprocessing Recommendations**

- ✓ KEEP all 13 input features (all potentially relevant)
- ✗ REMOVE employee_id (not predictive, just identifier)
- ✓ NO SCALING NEEDED for Linear Regression (but helpful)
- ✓ HANDLE NO MISSING VALUES needed (none exist)
- ✓ NO OUTLIERS to remove (all values are realistic)

---

## How to Use This Guide

1. **Before EDA**: Read this to understand what you're looking for
2. **During Modeling**: Refer back to expected impacts
3. **Interpreting Results**: Check if model findings match predictions
4. **Business Report**: Use sample profiles to explain findings

---

**Now you understand your dataset! Ready to build the model? 🚀**
