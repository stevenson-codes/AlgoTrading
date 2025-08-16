import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# Download options data for AAPL
chains = obb.derivatives.options.chains(
    "AAPL",
    provider="cboe"
)

# Filter the calls
calls = chains[(chains.option_type == "call")]
calls = calls[(calls.dte < 100) & (calls.strike >= 100)]
calls.drop_duplicates(subset=["strike", "dte"], keep=False, inplace=True)

# Pivot DataFrame
vol_surface = (
    calls.pivot(
        index="strike",
        columns="dte",
        values="implied_volatility"
    )
    .dropna(how="all", axis=1)
)

# Create 2D grid
strike, dte = np.meshgrid(
    vol_surface.columns, 
    vol_surface.index
)

# Plot the surface
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("Days to Expiration")
ax.set_ylabel("Strike Price")
ax.set_zlabel("Implied Volatility")
ax.plot_surface(
    strike,
    dte,
    vol_surface.values,
    cmap="viridis"
)

plt.show()