import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")

        # Define CSS for styling
        st.markdown(
            """
            <style>
            .metric-container {
                text-align: center;
            }
            .metric-title {
                font-size: 35px;
                color: #4CAF50;
            }
            .metric-value {
                font-size: 35px;
                font-weight: bold;
                color: #000;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Create columns for alignment
        col1, col2, col3, col4 = st.columns(4)

        # Display metrics using HTML with variables
        col1.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Total Messages</div>
                <div class="metric-value">{num_messages}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col2.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Total Words</div>
                <div class="metric-value">{words}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col3.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Media Shared</div>
                <div class="metric-value">{num_media_messages}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col4.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Links Shared</div>
                <div class="metric-value">{num_links}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # col1,col2,col3,col4=st.columns(4)
        # with col1:
        #     st.header("Total Messages")
        #     st.title(num_messages)
        # with col2:
        #     st.header("Total Words")
        #     st.title(words)
        # with col3:
        #     st.header("Media Shared")
        #     st.title(num_media_messages)
        # with col4:
        #     st.header("Links Shared")
        #     st.title(num_links)
        #monthy timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        if selected_user=='Overall':
            st.title("Most Busy Users")
            X,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()


            col1,col2=st.columns(2)
            with col1:
                ax.bar(X.index, X.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        st.title("Most Used Words")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        #emoji

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)