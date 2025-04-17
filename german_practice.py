import streamlit as st
import pandas as pd
import random

# Set page config
st.set_page_config(
    page_title="德语练习 | German Practice",
    page_icon="🇩🇪",
    layout="centered"
)

# Add title
st.title("德语练习 | German Practice")

# Add keyboard shortcuts
st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        // Space key
        if (e.code === 'Space') {
            e.preventDefault();
            document.querySelector('button[data-testid="baseButton-secondary"]').click();
        }
        // Left arrow
        if (e.code === 'ArrowLeft') {
            const prevButton = document.querySelector('button:contains("上一题")');
            if (prevButton) prevButton.click();
        }
        // Right arrow
        if (e.code === 'ArrowRight') {
            const nextButton = document.querySelector('button:contains("下一题")');
            if (nextButton) nextButton.click();
        }
    });
    </script>
""", unsafe_allow_html=True)

# Mode selection
mode = st.radio(
    "选择模式 | Select Mode",
    ["学习模式 | Study Mode", "练习模式 | Practice Mode"],
    horizontal=True
)

st.markdown("---")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Start Speaking German Fluently _ Questions with Answers!  - Sheet1.csv")
    # Remove duplicates and empty rows
    df = df.dropna().drop_duplicates()
    return df

df = load_data()

# Initialize session states
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'show_german' not in st.session_state:
    st.session_state.show_german = False
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Common styles
st.markdown("""
    <style>
    .chinese-text {
        font-size: 96px;
        font-weight: bold;
        color: #1E88E5;
        margin: 50px 0;
        line-height: 1.4;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f8ff;
    }
    .german-text {
        font-size: 96px;
        font-weight: bold;
        color: #43A047;
        margin: 50px 0;
        line-height: 1.4;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0fff0;
    }
    .question-number {
        font-size: 36px;
        font-weight: bold;
        color: #666;
        text-align: center;
        margin: 20px 0;
    }
    .stButton > button {
        font-size: 28px;
        padding: 20px 0;
    }
    .keyboard-shortcuts {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    .keyboard-shortcuts code {
        background-color: #e0e0e0;
        padding: 3px 6px;
        border-radius: 3px;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

if mode == "练习模式 | Practice Mode":
    # Function to get a random question
    def get_random_question():
        return df.iloc[random.randint(0, len(df)-1)]

    # Display current question
    if st.session_state.current_question is None:
        st.session_state.current_question = get_random_question()

    # Create a container for the question display
    question_container = st.container()

    with question_container:
        st.markdown(f'<p class="chinese-text">{st.session_state.current_question["chinese"]}</p>', unsafe_allow_html=True)
        
        # Show German text if button is clicked
        if st.session_state.show_german:
            st.markdown(f'<p class="german-text">{st.session_state.current_question["german"]}</p>', unsafe_allow_html=True)

    # Create two columns for buttons
    col1, col2 = st.columns(2)

    with col1:
        # Show German button
        if st.button("显示德语 | Show German (空格键 Space)", use_container_width=True):
            st.session_state.show_german = True
            st.rerun()

    with col2:
        # Next question button
        if st.button("下一题 | Next Question (右箭头 →)", use_container_width=True):
            st.session_state.current_question = get_random_question()
            st.session_state.show_german = False
            st.rerun()

else:  # Study Mode
    total_questions = len(df)
    
    # Display question number
    st.markdown(f'<p class="question-number">第 {st.session_state.current_index + 1} / {total_questions} 题</p>', unsafe_allow_html=True)
    
    # Display current pair
    current_pair = df.iloc[st.session_state.current_index]
    st.markdown(f'<p class="chinese-text">{current_pair["chinese"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="german-text">{current_pair["german"]}</p>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("上一题 | Previous (左箭头 ←)", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.rerun()

    with col2:
        if st.button("下一题 | Next (右箭头 →)", use_container_width=True):
            if st.session_state.current_index < total_questions - 1:
                st.session_state.current_index += 1
                st.rerun()

# Add instructions based on mode
st.markdown("---")

# Add keyboard shortcuts help
st.markdown("""
<div class="keyboard-shortcuts">
<h3>键盘快捷键 | Keyboard Shortcuts:</h3>
<ul>
<li>空格键 <code>Space</code>: 显示德语/下一题 | Show German/Next Question</li>
<li>左箭头 <code>←</code>: 上一题 | Previous Question</li>
<li>右箭头 <code>→</code>: 下一题 | Next Question</li>
</ul>
</div>
""", unsafe_allow_html=True)

if mode == "练习模式 | Practice Mode":
    st.markdown("""
    ### 使用说明 | Instructions:
    1. 先尝试记住中文对应的德语 | Try to remember the German translation for the Chinese text
    2. 点击"显示德语"或按空格键查看答案 | Click "Show German" or press Space to see the answer
    3. 点击"下一题"或按右箭头继续练习 | Click "Next Question" or press Right Arrow to continue
    """)
else:
    st.markdown("""
    ### 使用说明 | Instructions:
    1. 通过题号查看进度 | Track your progress with question numbers
    2. 使用左右箭头或按钮浏览题目 | Use arrow keys or buttons to navigate
    3. 中文和德语同时显示，便于学习 | Chinese and German shown together for learning
    """) 