import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from data_loader import load_data

# dcc --> dash core components --> drop down, sliders, graphs
# Input , Output --> Used to connect interactivity between input and output components
# html -> components of html

# Load data
df = load_data()
available_countries = sorted(df['Country'].unique())

# Start Dash app
app = dash.Dash(__name__)
app.title = "Retail Dashboard"

# Layout
app.layout = html.Div([

    html.H1("Online Retail Dashboard"),

    html.Label("Select a Country"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in available_countries],
        value='United Kingdom',
        # value=None,
        style={'width': '300px'}
    ),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='bar-chart'),
])

# Callbacks
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('country-dropdown', 'value')]
)

# Plot 1 and Plot 2, should be based on selected country
# plot 1 --> line chart -- monthly revenue
# plot 2 --> bar chart -- Top 5 revenue months

def update_chart(selected_country):
    filtered_df = df[df['Country'] == selected_country]


    # Line Chart - Monthly Revenue
    monthly_rev = filtered_df.groupby('Month')['Revenue'].sum().reset_index()
    line_fig = px.line(monthly_rev, x='Month', y='Revenue',
                       title=f'Monthly Revenue in {selected_country}',
                       markers=True)
    line_fig.update_layout(xaxis_tickangle=45)
    
    # Bar Chart - Top 5 Revenue Months
    top_months = monthly_rev.sort_values('Revenue', ascending=False).head(5)
    bar_fig = px.bar(top_months, x='Month', y='Revenue',
                     title=f'Top 5 Revenue Months in {selected_country}',
                     text='Revenue')
    bar_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    return line_fig, bar_fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)