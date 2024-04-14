from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd

# Load the dataset (replace the URL with the actual data URL)
df = pd.read_csv('data/fire.csv', dtype={'date': str})  # Read the date as string

print(df.head())
# Check the columns to ensure 'date' is present
print(df.columns)

# Assuming 'date' is correct and now present in df.columns, parse it
df['date'] = pd.to_datetime(df['date'], format='%m-%d-%y')

# Extract year and month for filtering
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Start the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='incident-type-dropdown',
            options=[{'label': i, 'value': i}
                     for i in df['incident'].unique()],
            value=df['incident'].unique()[0]
        )
    ]),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        min=df['month'].min(),
        max=df['month'].max(),
        step=1,
        value=df['month'].min(),
        marks={str(month): f"{month:02d}" for month in range(
            1, 13)},  # Ensure months are shown as two digits
        id='month-slider'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('month-slider', 'value'),
     Input('incident-type-dropdown', 'value')])
def update_figure(selected_month, selected_incident):
    filtered_df = df[(df.month == selected_month) &
                     (df.incident == selected_incident)]
    filtered_df = filtered_df.groupby(
        ['date', 'incident']).size().reset_index(name='count')

    # Creating a line plot for the number of incidents over time
    fig = px.line(
        filtered_df,
        x='date',
        y='count',
        title='Incidents Over Time',
        color='incident')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
