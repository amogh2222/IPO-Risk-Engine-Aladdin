import pandas as pd
import numpy as np

# Seed for consistency
np.random.seed(42)

# Generate 120 IPO Names
names = [f"IPO_{i}" for i in range(1, 121)]
sectors = ['Tech', 'FinTech', 'Energy', 'Consumer', 'Health', 'SME']

data = {
    'IPO Name': names,
    'Sector': np.random.choice(sectors, 120),
    'Subscription (x)': np.random.uniform(1, 150, 120),
    'GMP': np.random.uniform(5, 80, 120),  # Grey Market Premium %
    'Hype Score': np.random.randint(1, 11, 120)
}

df = pd.DataFrame(data)

# Create Listing Gain based on a formula (Hype + Subscription + Random Noise)
# This mimics real market behavior for your model to find patterns
df['Listing Gain %'] = (df['GMP'] * 0.6) + (df['Subscription (x)'] * 0.2) + np.random.normal(0, 5, 120)

# Save it
df.to_csv("ipo_data.csv", index=False)
print("Success: 'ipo_data.csv' created with 120 entries.")