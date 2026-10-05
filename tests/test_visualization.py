import pandas as pd

from visualization.chart_generator import generate_chart


# Test data
data = {
    "city": [
        "Bhopal",
        "Indore",
        "Delhi",
        "Mumbai",
        "Pune"
    ],
    "total_sales": [
        50000,
        75000,
        60000,
        90000,
        45000
    ]
}


df = pd.DataFrame(data)


# Generate chart
chart = generate_chart(df)


# Check result
if chart is not None:

    print("Chart generated successfully!")
    print("Chart type:", type(chart).__name__)

else:

    print("No suitable chart could be generated.")