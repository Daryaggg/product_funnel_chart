import numpy as np

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import colorlover as cl
plotly.offline.init_notebook_mode()

from product_funnel_chart.chart.config import tableau20_colors

def funnel_chart(values, phases, chart_title, labels=None, colors=tableau20_colors
                 shuffle_colors=False, title_size=20, font_size=14):
    '''
    Tool to create a nice funnel chart.

    values - numbers (of users)
    phases - name of the step
    labels - values displayed on chart
    colors - colors of your chart, by default - tableu chart colors
    shuffle_colors - if you want to see random colors
    title_size - set title size
    font_size - set labels font size

    --
    code source = https://plot.ly/python/funnel-charts/

    '''
    if labels is None:
        first_value = values[0]
        labels = [str(value) + ' / '
                  + str(round(value/values[0]*100, 1)) + '%'
                  for value in values]

    # color of each funnel section
    n_phase = len(phases)
    if shuffle_colors:
        colors = np.random.choice(colors, size=n_phase, replace=False)
    else:
        colors = colors[:n_phase]

    plot_width = 500

    # height of a section and difference between sections
    section_h = 70
    section_d = 10

    # multiplication factor to calculate the width of other sections
    values = [int(x.split(' /')[0]) for x in labels]
    unit_width = plot_width / max(values)

    # width of each funnel section relative to the plot width
    phase_w = [int(value * unit_width) for value in values]

    # plot height based on the number of sections and the gap in between them
    height = section_h * n_phase + section_d * (n_phase - 1)

    # list containing all the plot shapes
    shapes = []

    # list containing the Y-axis location for each section's name and value text
    label_y = []

    for i in range(n_phase):
            if (i == n_phase-1):
                    points = [phase_w[i] / 2, height, phase_w[i] / 2, height - section_h]
            else:
                    points = [phase_w[i] / 2, height, phase_w[i+1] / 2, height - section_h]

            path = 'M {0} {1} L {2} {3} L -{2} {3} L -{0} {1} Z'.format(*points)

            shape = {
                    'type': 'path',
                    'path': path,
                    'fillcolor': colors[i],
                    'line': {
                        'width': 1,
                        'color': colors[i]
                    }
            }
            shapes.append(shape)

            # Y-axis location for this section's details (text)
            label_y.append(height - (section_h / 2))

            height = height - (section_h + section_d)

    # For phase names
    label_trace = go.Scatter(
        x=[-450]*n_phase,
        y=label_y,
        mode='text',
        text=phases,
        textposition="middle right",
        textfont=dict(
            family='Arial',
            color='rgba(44,58,71,1)',
            size=font_size
        )
    )

    # For phase values
    value_trace = go.Scatter(
        x=[450]*n_phase,
        y=label_y,
        mode='text',
        text=labels,
        textposition="middle left",
        textfont=dict(
            family='Arial',
            color='rgba(44,58,71,1)',
            size=font_size
        )
    )

    data = [label_trace, value_trace]

    layout = go.Layout(
        title="<b>{}</b>".format(chart_title),
        titlefont=dict(
            size=title_size,
            color='rgb(203,203,203)'
        ),
        shapes=shapes,
        height=560,
        width=800,
        showlegend=False,
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(255,255,255)',
        xaxis=dict(
            showticklabels=False,
            zeroline=False,
            showgrid=False
        ),
        yaxis=dict(
            showticklabels=False,
            zeroline=False,
            showgrid=False
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, image='png')
