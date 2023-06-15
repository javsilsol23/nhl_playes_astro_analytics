import streamlit as st
import pandas as pd
import plotly.express as px


def plot_bar_chart(df, title, order, gb, colors):

    grouped = df.groupby(gb).size().reset_index(name='count')

    fig = px.bar(grouped, x=gb, y='count', title=title,
                 color=gb, color_discrete_sequence=colors,
                 category_orders={gb: order}
    )

    fig.update_layout(
        plot_bgcolor='#ccffe6',
        showlegend=False,
        width=1000,
        height=600
    )

    return fig


def plot_pie_chart(df, title, names, color_map):

    fig = px.pie(df,
                 names=names, title=title,
                 color=names, color_discrete_map=color_map
                 )
    fig.update_layout(
        # Set to 'rgba(0,0,0,0)' for transparent background
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#ccffe6'  # Set the desired background color
    )

    return fig


def classify_sign(s):
    signs = ['ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO',
             'LIBRA', 'SCORPIO', 'SAGITTARIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES']
    
    element = modality = ''

    if (signs.index(s) + 1) % 3 == 0:
        modality = 'cardinal'
    elif (signs.index(s) + 1) % 3 == 1:
        modality = 'fixed'
    else:
        modality = 'mutable'

    if (signs.index(s) + 1) % 4 == 0:
        element = 'fire'
    elif (signs.index(s) + 1) % 4 == 1:
        element = 'earth'
    elif (signs.index(s) + 1) % 4 == 2:
        element = 'air'
    else:
        element = 'water'

    return element, modality


@st.cache_data
def load_data():
    data = pd.read_csv('players4.csv')
    data = data.drop(['lat', 'lon'], axis=1)
    return data


#################################################################
#       MAIN        MAIN        MAIN        MAIN        MAIN    #
#################################################################


st.set_page_config(layout="wide")

tab1, tab2 = st.tabs(['Venus Cycle', 'Horoscope'])


with tab1:
    st.markdown('# Venus Cycle')

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write('')

    with col2:

        st.markdown(
            '<h1 style="text-align: center">NHL Players by Venus Cycle</h1>', unsafe_allow_html=True)
        data = load_data()
        data = data.drop(['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter',
                         'saturn', 'uranus', 'neptune', 'pluto', 'nn'], axis=1)

        data['color'] = data['venus_cycle'].str[:-2]

        position = st.selectbox(
            'Which position players you want to display?',
            ('All', 'Goalie', 'Defensman', 'Wing', 'Center', 'Forward'), key='position_v')

        if position == 'All':
            filtered_data = data
        elif position == 'Goalie':
            filtered_data = data[data['position'].str.contains('G')]
        elif position == 'Defensman':
            filtered_data = data[data['position'].str.contains('D')]
        elif position == 'Wing':
            filtered_data = data[data['position'].str.contains('W')]
        elif position == 'Center':
            filtered_data = data[data['position'].str.contains('C')]
        elif position == 'Forward':
            filtered_data = data[data['position'].str.contains('F')]

        if position == 'Goalie':
            s1 = 'Games Played'
            s2 = 'Wins'
            s3 = 'Losses'
            s4 = 'Ties'
            s5 = 'Shutouts'
            s6 = 'Point Shares'
            s7 = 'Minutes'
            s8 = 'Goals Against Average'
            s9 = 'Save Percentage'
        else:
            s1 = 'Games Played'
            s2 = 'Goals'
            s3 = 'Assists'
            s4 = 'Points'
            s5 = 'Plus/Minus'
            s6 = 'Point Shares'
            s7 = 'Penalties in Minutes'
            s8 = 'Shots on Goal'
            s9 = 'Game Winning Goals'

        with st.expander('Display filters'):
            max_s1 = int(data['s1'].max())
            s1x = st.slider(s1, 0, max_s1, 0, key='s1x_v')

            max_s2 = int(data['s2'].max())
            s2x = st.slider(s2, 0, max_s2, 0, key='s2x_v')

            max_s3 = int(data['s3'].max())
            s3x = st.slider(s3, 0, max_s3, 0, key='s3x_v')

            max_s4 = int(data['s4'].max())
            s4x = st.slider(s4, 0, max_s4, 0, key='s4x_v')

            max_s5 = int(data['s5'].max())
            s5x = st.slider(s5, 0, max_s5, 0, key='s5x_v')

            max_s6 = int(data['s6'].max())
            s6x = st.slider(s6, 0, max_s6, 0, key='s6x_v')

            max_s7 = int(data['s7'].max())
            s7x = st.slider(s7, 0, max_s7, 0, key='s7x_v')

            max_s8 = int(data['s8'].max())
            s8x = st.slider(s8, 0, max_s8, 0, key='s8x_v')

            max_s9 = int(data['s9'].max())
            s9x = st.slider(s9, 0, max_s9, 0, key='s9x_v')

        filtered_data = filtered_data[(filtered_data['s1'] > s1x) & (filtered_data['s2'] > s2x) & 
                                      (filtered_data['s3'] > s3x) & (filtered_data['s4'] > s4x) & 
                                      (filtered_data['s5'] > s5x) & (filtered_data['s6'] > s6x) & 
                                      (filtered_data['s7'] > s7x) & (filtered_data['s8'] > s8x) & 
                                      (filtered_data['s9'] > s9x)
                        ]

        gb = 'venus_cycle'

        order = ['White_1', 'Blue_5', 'Black_4', 'Red_3', 'White_2', 'Blue_1', 'Black_5', 'Red_4', 'White_3', 'Blue_2',
                 'Black_1', 'Red_5', 'White_4', 'Blue_3', 'Black_2', 'Red_1', 'White_5', 'Blue_4', 'Black_3', 'Red_2']
        
        colors = ['white', 'blue', 'black', 'red', 'white', 'blue', 'black', 'red', 'white',
                  'blue', 'black', 'red', 'white', 'blue', 'black', 'red', 'white', 'blue', 'black', 'red']
        
        title = 'Total Player Count by Venus Interval'

        fig1 = plot_bar_chart(
            filtered_data, title, order, gb, colors)
        
        st.plotly_chart(fig1)

        color_map = {
            'White': 'white',
            'Red': 'red',
            'Blue': 'blue',
            'Black': 'black'
        }

        fig2 = plot_pie_chart(
            filtered_data, 'Players by element', 'color', color_map)

        st.plotly_chart(fig2)

    with col3:
        st.write('')


with tab2:
    st.markdown('# Horoscope')

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write('')

    with col2:

        st.markdown(
            '<h1 style="text-align: center">NHL Players by Horoscopic Signs</h1>', unsafe_allow_html=True)
        data = load_data()
        data = data.drop(['venus_cycle'], axis=1)

        position = st.selectbox(
            'Which position players you want to display?',
            ('All', 'Goalie', 'Defensman', 'Wing', 'Center', 'Forward'), key='position_h')

        if position == 'All':
            filtered_data = data
        elif position == 'Goalie':
            filtered_data = data[data['position'].str.contains('G')]
        elif position == 'Defensman':
            filtered_data = data[data['position'].str.contains('D')]
        elif position == 'Wing':
            filtered_data = data[data['position'].str.contains('W')]
        elif position == 'Center':
            filtered_data = data[data['position'].str.contains('C')]
        elif position == 'Forward':
            filtered_data = data[data['position'].str.contains('F')]

        if position == 'Goalie':
            s1 = 'Games Played'
            s2 = 'Wins'
            s3 = 'Losses'
            s4 = 'Ties'
            s5 = 'Shutouts'
            s6 = 'Point Shares'
            s7 = 'Minutes'
            s8 = 'Goals Against Average'
            s9 = 'Save Percentage'
        else:
            s1 = 'Games Played'
            s2 = 'Goals'
            s3 = 'Assists'
            s4 = 'Points'
            s5 = 'Plus/Minus'
            s6 = 'Point Shares'
            s7 = 'Penalties in Minutes'
            s8 = 'Shots on Goal'
            s9 = 'Game Winning Goals'

        with st.expander('Display filters'):
            max_s1 = int(data['s1'].max())
            s1x = st.slider(s1, 0, max_s1, 0, key='s1x_h')

            max_s2 = int(data['s2'].max())
            s2x = st.slider(s2, 0, max_s2, 0, key='s2x_h')

            max_s3 = int(data['s3'].max())
            s3x = st.slider(s3, 0, max_s3, 0, key='s3x_h')

            max_s4 = int(data['s4'].max())
            s4x = st.slider(s4, 0, max_s4, 0, key='s4x_h')

            max_s5 = int(data['s5'].max())
            s5x = st.slider(s5, 0, max_s5, 0, key='s5x_h')

            max_s6 = int(data['s6'].max())
            s6x = st.slider(s6, 0, max_s6, 0, key='s6x_h')

            max_s7 = int(data['s7'].max())
            s7x = st.slider(s7, 0, max_s7, 0, key='s7x_h')

            max_s8 = int(data['s8'].max())
            s8x = st.slider(s8, 0, max_s8, 0, key='s8x_h')

            max_s9 = int(data['s9'].max())
            s9x = st.slider(s9, 0, max_s9, 0, key='s9x_h')

        filtered_data = filtered_data[(filtered_data['s1'] > s1x) & (filtered_data['s2'] > s2x) &
                                      (filtered_data['s3'] > s3x) & (filtered_data['s4'] > s4x) &
                                      (filtered_data['s5'] > s5x) & (filtered_data['s6'] > s6x) &
                                      (filtered_data['s7'] > s7x) & (filtered_data['s8'] > s8x) &
                                      (filtered_data['s9'] > s9x)
                                      ]

        if st.checkbox('Show table', key='show_h'):
            st.subheader('Players')
            st.write(filtered_data)

        planet = st.selectbox(
            'Which Planet?',
            ('Sun', 'Moon', 'Mercury', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'North Node', 'ASC', 'MC'))

        title = 'Total Player Count by ' + planet + ' Sign'
        if planet == 'North Node':
            planet = 'nn'

        gb = planet.lower()

        order = ['ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO',
                 'LIBRA', 'SCORPIO', 'SAGITTARIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES']

        colors = ['red', 'brown', 'yellow', 'blue', 'red', 'brown', 'yellow', 'blue',
                  'red', 'brown', 'yellow', 'blue', 'red', 'brown', 'yellow', 'blue']

        title = 'Total Player Count by Sign'

        fig1 = plot_bar_chart(
            filtered_data, title, order, gb, colors)

        st.plotly_chart(fig1)

        filtered_data[['element', 'modality']] = filtered_data[gb].apply(
            classify_sign).apply(pd.Series)

        col2_a, col2_b = st.columns(2)

        with col2_a:
            color_map = {
                'fire': 'red',
                'earth': 'brown',
                'air': 'yellow',
                'water': 'blue'
            }
            fig1 = plot_pie_chart(
                filtered_data, 'Players by element', 'element', color_map)
            st.plotly_chart(fig1, use_container_width=True)

        with col2_b:
            color_map = {
                'cardinal': 'red',
                'fix': 'blue',
                'mutable': 'white'
            }
            fig2 = plot_pie_chart(
                filtered_data, 'Players by modality', 'modality', color_map)
            st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.write('')
