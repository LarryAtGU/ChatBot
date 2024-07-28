Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. Here's a step-by-step tutorial to get you started with Streamlit.

### Step 1: Install Streamlit

First, you need to install Streamlit. You can do this using pip:

```bash
pip install streamlit
```

### Step 2: Create a Simple Streamlit App

Create a new Python file, for example, `app.py`, and add the following code:

```python
import streamlit as st

st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
```

### Step 3: Run the Streamlit App

To run your app, open a terminal and navigate to the directory containing `app.py`, then run:

```bash
streamlit run app.py
```

This will start a local web server and open a new tab in your default web browser showing your Streamlit app.

### Step 4: Adding More Features

#### Displaying Data

Streamlit can easily display data frames:

```python
import streamlit as st
import pandas as pd

st.title("Data Display Example")

data = {
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40]
}
df = pd.DataFrame(data)

st.write("Here is a simple data frame:")
st.write(df)
```

#### Plotting

Streamlit integrates with various plotting libraries like Matplotlib, Seaborn, and Plotly:

```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Plotting Example")

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

st.pyplot(fig)
```

#### Interactive Widgets

Streamlit provides various interactive widgets like sliders, buttons, and text inputs:

```python
import streamlit as st

st.title("Interactive Widgets Example")

name = st.text_input("Enter your name")
st.write(f"Hello, {name}!")

age = st.slider("Select your age", 0, 100, 25)
st.write(f"Your age is: {age}")
```

### Step 5: Combining Everything

Here's an example that combines data display, plotting, and interactive widgets:

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Streamlit Tutorial")

# Interactive widget
st.sidebar.title("Controls")
name = st.sidebar.text_input("Enter your name")
age = st.sidebar.slider("Select your age", 0, 100, 25)

# Display data
data = {
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40]
}
df = pd.DataFrame(data)
st.write("Here is a simple data frame:")
st.write(df)

# Plotting
x = np.linspace(0, 10, 100)
y = np.sin(x) * (age / 100)

fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)

# Display input
st.write(f"Hello, {name}!")
st.write(f"Your age is: {age}")
```

### Step 6: Deploying Your Streamlit App

Streamlit provides an easy way to deploy your apps using Streamlit Cloud. You can also deploy your app on other platforms like Heroku, AWS, or Google Cloud.

To deploy on Streamlit Cloud:
1. Push your code to a GitHub repository.
2. Sign in to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repository and deploy your app.

This is a basic overview to get you started with Streamlit. The official [Streamlit documentation](https://docs.streamlit.io/) has more detailed information and examples for creating advanced applications.