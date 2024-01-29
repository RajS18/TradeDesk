import streamlit as st  # streamlit library
import pandas as pd  # pandas library
import yfinance as yf  # yfinance library
import datetime  # datetime library
from datetime import date
from plotly import graph_objs as go  # plotly library
from prophet import Prophet  # prophet library
# plotly library for prophet model plotting
from prophet.plot import plot_plotly
import time  # time library
from streamlit_option_menu import option_menu  # select_options library

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

# Main code
add_meta_tag()

# Sidebar Section Starts Here
today = date.today()  # today's date
st.write('''# TradeDesk ''')  # title

st.sidebar.write('''# TradeDesk ''')

with st.sidebar: 
        selected = option_menu("Utilities", ["Asset Performance Analysis", "Real-Time Asset Prices", "Asset price Prediction Modelling", 'About'])

start = st.sidebar.date_input(
    'Start', datetime.date(2022, 1, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
# Sidebar Section Ends Here

# read csv file
path = 'TickersData.csv'
stock_df = pd.read_csv(path)

# Stock Performance Comparison Section Starts Here
if(selected == 'Asset Performance Analysis'):  # if user selects 'Stocks Performance Comparison'
    st.subheader("Stocks Performance Analysis")
    tickers = stock_df["Company Name"]
    # dropdown for selecting assets
    dropdown = st.multiselect('Pick your assets', tickers)

    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)
        # st.success('Loaded')

    dict_csv = pd.read_csv(path, header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    for i in dropdown:  # for each asset selected
        val = dict_csv.get(i)  # get symbol from csv file
        symb_list.append(val)  # append symbol to list

    def relativeret(df):  # function for calculating relative return
        rel = df.pct_change()  # calculate relative return
        cumret = (1+rel).cumprod() - 1  # calculate cumulative return
        cumret = cumret.fillna(0)  # fill NaN values with 0
        return cumret  # return cumulative return

    if len(dropdown) > 0:  # if user selects atleast one asset
        df = relativeret(yf.download(symb_list, start, end))[
            'Adj Close']  # download data from yfinance
        # download data from yfinance
        raw_df = relativeret(yf.download(symb_list, start, end))
        raw_df.reset_index(inplace=True)  # reset index

        closingPrice = yf.download(symb_list, start, end)[
            'Adj Close']  # download data from yfinance
        volume = yf.download(symb_list, start, end)['Volume']
        
        st.subheader('Raw Data {}'.format(dropdown))
        st.write(raw_df)  # display raw data
        chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
        # dropdown for selecting chart type
        dropdown1 = st.selectbox('Pick your chart', chart)
        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

        st.subheader('Relative Returns {}'.format(dropdown))
                
        if (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
            st.line_chart(df)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

        elif (dropdown1) == 'Area Chart':  # if user selects 'Area Chart'
            st.area_chart(df)  # display area chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.area_chart(closingPrice)  # display area chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.area_chart(volume)  # display area chart

        elif (dropdown1) == 'Bar Chart':  # if user selects 'Bar Chart'
            st.bar_chart(df)  # display bar chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.bar_chart(closingPrice)  # display bar chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.bar_chart(volume)  # display bar chart

        else:
            st.line_chart(df, width=1000, height=800,
                          use_container_width=False)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

    else:  # if user doesn't select any asset
        st.write('Please select atleast one asset')  # display message
# Stock Performance Comparison Section Ends Here
    
# Real-Time Stock Price Section Starts Here
elif(selected == 'Real-Time Asset Prices'):  # if user selects 'Real-Time Stock Price'
    st.subheader("Real-Time Stock Prices")
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

    dict_csv = pd.read_csv(path, header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols

    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list

    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false

    def callback():  # function for updating data
        # if button is clicked
        st.session_state.button_clicked = True  # set button clicked to true
    if (
        st.button("Search", on_click=callback)  # button for searching data
        or st.session_state.button_clicked  # if button is clicked
    ):
        if(a == ""):  # if user doesn't select any company
            st.write("Click Search to Search for a Open-traded org.")
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
        else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data
            def calculate_sma(data, window=20):
                ans = data['Close'].rolling(window=window).mean()
                return ans
            def get_sma_shapes(data):
                sma_window = 20  # You can adjust the window size as needed
                sma = calculate_sma(data, window=sma_window)
            
                shapes = [
                    dict(
                        x0=data['Date'].iloc[0],
                        x1=data['Date'].iloc[-1],
                        y0=sma.min(),
                        y1=sma.max(),
                        xref='x',
                        yref='y',
                        type='line',
                        line=dict(color='orange', width=2)
                    )
                ]
            
                return shapes
            def calculate_bollinger_bands(data, window=20, num_std=2):
                sma = data['Close'].rolling(window=window).mean()
                rolling_std = data['Close'].rolling(window=window).std()
                upper_band = sma + num_std * rolling_std
                lower_band = sma - num_std * rolling_std
                
                return upper_band, lower_band
            def get_bollinger_bands_shapes(data):
                bollinger_window = 20  # You can adjust the window size as needed
                upper_band, lower_band = calculate_bollinger_bands(data, window=bollinger_window)
            
                shapes = [
                    dict(
                        x0=data['Date'].iloc[0],
                        x1=data['Date'].iloc[-1],
                        y0=upper_band,
                        y1=upper_band,
                        xref='x',
                        yref='y',
                        type='line',
                        line=dict(color='green', width=2, dash='dash')
                    ),
                    dict(
                        x0=data['Date'].iloc[0],
                        x1=data['Date'].iloc[-1],
                        y0=lower_band,
                        y1=lower_band,
                        xref='x',
                        yref='y',
                        type='line',
                        line=dict(color='red', width=2, dash='dash')
                    )
                ]
            
                return shapes

            def calculate_rsi(data, window=14):
                price_diff = data['Close'].diff(1)
                
                gain = price_diff.where(price_diff > 0, 0)
                loss = -price_diff.where(price_diff < 0, 0)
                
                avg_gain = gain.rolling(window=window).mean()
                avg_loss = loss.rolling(window=window).mean()
                
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
                
                return rsi
            def get_rsi_shapes(data):
                rsi_window = 14  # You can adjust the window size as needed
                rsi = calculate_rsi(data, window=rsi_window)
            
                shapes = [
                    dict(
                        x0=data['Date'].iloc[0],
                        x1=data['Date'].iloc[-1],
                        y0=rsi,
                        y1=rsi,
                        xref='x',
                        yref='y',
                        type='line',
                        line=dict(color='purple', width=2)
                    )
                ]
            
                return shapes
            data_sma = calculate_sma(data)
            data_rsi = calculate_rsi(data)
            data_bb_up,data_bb_down = calculate_bollinger_bands(data)
            
            def plot_raw_data(data):  # function for plotting raw data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Open'], mode='lines', name="stock_open"))  # x-axis: date, y-axis: open
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Close'], mode='lines', name="stock_close"))  # x-axis: date, y-axis: close
            
                # Update layout to make the chart as big as possible
                fig.update_layout(
                    title='Line Chart of {}'.format(a),
                    yaxis_title='Stock Price',
                    xaxis_title='Date',
                    height=800,  # Set chart height to 800px
                    xaxis_rangeslider=dict(visible=True),  # Enable rangeslider
                    hovermode="x unified"  # Enable unified hover mode
                )
            
                # Enable hover data with tooltips
                fig.update_traces(hoverinfo='x+y+text', hovertext=data.apply(
                    lambda row: f"Open: {row['Open']}, Close: {row['Close']}", axis=1))
            
                # Enable rangeselector buttons for different time intervals
                fig.update_xaxes(
                    rangeslider=dict(visible=True),
                    rangeselector=dict(
                        buttons=list([
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(count=30, label="1m", step="day", stepmode="backward"),
                            dict(count=90, label="3m", step="day", stepmode="backward"),
                            dict(count=180, label="6m", step="day", stepmode="backward"),
                            dict(count=365, label="1y", step="day", stepmode="backward"),
                            dict(count=365, label="YTD", step="day", stepmode="todate"),
                            dict(count=1825, label="5y", step="day", stepmode="backward"),
                        ])
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)  # use_container_width=True for automatic adjustment

            def plot_candle_data(data):  # function for plotting candle data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Candlestick(x=data['Date'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'],
                                             name='market data'))
                sma_visible = sma_check
                rsi_visible = rsi_check
                bb_visible = bb_check
                if(sma_visible):
                    fig.add_trace(go.Scatter(
                        x=data['Date'], y=data_sma, mode='lines', name="SMA (20)", line=dict(color="orange")))
                if(rsi_visible):
                    fig.add_trace(go.Scatter(
                        x=data['Date'], y=data_rsi, mode='lines', name="RSI (14)", line=dict(color="cyan")))
                if(bb_visible):
                    fig.add_trace(go.Scatter(
                        x=data['Date'], y=data_bb_up, mode='lines', name="BB-Up (20.2)", line=dict(color="green")))
                    fig.add_trace(go.Scatter(
                        x=data['Date'], y=data_bb_down, mode='lines', name="BB-Down (20.2)", line=dict(color="red")))

                # Update layout to make the chart as big as possible
                fig.update_layout(
                    title='Candlestick Chart of {}'.format(a),
                    yaxis_title='Stock Price',
                    xaxis_title='Date',
                    height=800,  # Set chart height to 800px
                    xaxis_rangeslider=dict(visible=True),  # Enable rangeslider
                    hovermode="x unified",  # Enable unified hover mode
                    xaxis_rangebreaks=[dict(values=data['Date'].iloc[[0, -1]], pattern='day of week')]
                )
            
                # Enable hover data with tooltips
                fig.update_traces(hoverinfo='x+y+text', hovertext=data.apply(
                    lambda row: f"Open: {row['Open']}, Close: {row['Close']}, High: {row['High']}, Low: {row['Low']}", axis=1))
            
                # Enable rangeselector buttons for different time intervals
                fig.update_xaxes(
                    rangeslider=dict(visible=True),
                    rangeselector=dict(
                        buttons=list([
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(count=30, label="1m", step="day", stepmode="backward"),
                            dict(count=90, label="3m", step="day", stepmode="backward"),
                            dict(count=180, label="6m", step="day", stepmode="backward"),
                            dict(count=365, label="1y", step="day", stepmode="backward"),
                            dict(count=365, label="YTD", step="day", stepmode="todate"),
                            dict(count=1825, label="5y", step="day", stepmode="backward"),
                        ])
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True) 
            # Add checkbox to toggle SMA visibility
            sma_check = st.checkbox("Toggle SMA Visibility", key="sma_visible", value=False)
            # Add checkbox to toggle Bollinger Bands visibility
            bb_check = st.checkbox("Toggle Bollinger Bands Visibility", key="bb_visible", value=False)
            # Add checkbox to toggle RSI visibility
            rsi_check = st.checkbox("Toggle RSI Visibility", key="rsi_visible", value=False)  
            chart = ('Candle Stick', 'Line Chart')  # chart types
            
            # dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
            
            if (dropdown1) == 'Candle Stick':  
                plot_candle_data(data)  # plot candle data
            elif (dropdown1) == 'Line Chart':# if user selects 'Line Chart'
                plot_raw_data(data)  # plot raw data
            else:  # if user doesn't select any chart
                plot_candle_data(data)  # plot candle data

# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here
elif(selected == 'Asset price Prediction Modelling'):  # if user selects 'Stock Prediction'
    st.subheader("Stock Prediction Model")

    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)
    with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
    dict_csv = pd.read_csv(path, header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list
    if(a == ""):  # if user doesn't select any company
        st.write("Enter a Stock Name")  # display message
    else:  # if user selects a company
        # download data from yfinance
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)  # reset index
        st.subheader('Raw Data of {}'.format(a))  # display raw data
        st.write(data)  # display data

        def plot_raw_data():  # function for plotting raw data
            fig = go.Figure()  # create figure
            fig.add_trace(go.Scatter(  # add scatter plot
                x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
            fig.add_trace(go.Scatter(  # add scatter plot
                x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
            fig.layout.update(  # update layout
                title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
            st.plotly_chart(fig)  # display plotly chart

        plot_raw_data()  # plot raw data
        # slider for selecting number of years
        n_years = st.slider('Years of prediction:', 1, 4)
        period = n_years * 365  # calculate number of days

        # Predict forecast with Prophet
        # create dataframe for training data
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(
            columns={"Date": "ds", "Close": "y"})  # rename columns

        m = Prophet()  # create object for prophet
        m.fit(df_train)  # fit data to prophet
        future = m.make_future_dataframe(
            periods=period)  # create future dataframe
        forecast = m.predict(future)  # predict future dataframe

        # Show and plot forecast
        st.subheader('Forecast Data of {}'.format(a))  # display forecast data
        st.write(forecast)  # display forecast data

        st.subheader(f'Forecast plot for {n_years} years')  # display message
        fig1 = plot_plotly(m, forecast)  # plot forecast
        st.plotly_chart(fig1)  # display plotly chart

        st.subheader("Forecast components of {}".format(a))  # display message
        fig2 = m.plot_components(forecast)  # plot forecast components
        st.write(fig2)  # display plotly chart

# Stock Price Prediction Section Ends Here

elif(selected == 'About'):
    st.subheader("About")
    
    st.markdown("""
        <style>
    .big-font {
        font-size:25px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font">TradeDesk is a simple light weight web application that allows users to visualize Assest Performance and do Comparative anlysis, Get Real-Time Asset Prices with multiple technical indicators like RSI, SMA and Bollinger Bands (with a scope to add more) and deliver a sophisticated Asset Price Prediction model. This is integrated with realtime orderbook simulator and a stock screener for retail algorithmic traders as well {Saperate on module called Screener}</p>', unsafe_allow_html=True)
    