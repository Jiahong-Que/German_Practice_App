import streamlit as st
import pandas as pd
import random

# Set page config
st.set_page_config(
    page_title="Jiahong | German Practice",
    page_icon="🇩🇪",
    layout="centered"
)

# Add title
st.title("Jiahong | German Practice")

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
col1, col2 = st.columns([2, 1])
with col1:
    mode = st.radio(
        "选择模式 | Select Mode",
        ["学习模式 | Study Mode", "练习模式 | Practice Mode"],
        horizontal=True
    )
with col2:
    font_size = st.slider(
        "字体大小 | Font Size",
        min_value=12,
        max_value=120,
        value=24,
        step=8,
        help="调整中文和德语文本的字体大小 | Adjust the font size of Chinese and German text"
    )

st.markdown("---")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Start Speaking German Fluently | Questions with Answers! .csv")
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
st.markdown(f"""
    <style>
    .chinese-text {{
        font-size: {font_size}px;
        font-weight: bold;
        color: #1E88E5;
        margin: {font_size//2}px 0;
        line-height: 1.4;
        text-align: center;
        padding: {font_size//3}px;
        border-radius: 10px;
        background-color: #f0f8ff;
    }}
    .german-text {{
        font-size: {font_size}px;
        font-weight: bold;
        color: #43A047;
        margin: {font_size//2}px 0;
        line-height: 1.4;
        text-align: center;
        padding: {font_size//3}px;
        border-radius: 10px;
        background-color: #f0fff0;
    }}
    .question-number {{
        font-size: {max(36, font_size//2)}px;
        font-weight: bold;
        color: #666;
        text-align: center;
        margin: 20px 0;
    }}
    .stButton > button {{
        font-size: 28px;
        padding: 20px 0;
    }}
    .keyboard-shortcuts {{
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }}
    .keyboard-shortcuts code {{
        background-color: #e0e0e0;
        padding: 3px 6px;
        border-radius: 3px;
        font-family: monospace;
    }}
    .question-selector {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }}
    .question-selector-label {{
        font-size: 20px;
        color: #666;
        margin-bottom: 10px;
    }}
    div[data-baseweb="input"] input {{
        font-size: 24px !important;
        text-align: center !important;
        color: #1a73e8 !important;
        font-weight: bold !important;
    }}
    .toggle-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px 0;
    }}
    .toggle-label {{
        font-size: 18px;
        color: #666;
        margin-right: 10px;
    }}
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
    
    # Question selector with improved styling
    st.markdown('<div class="question-selector-label">题号选择 | Question Number</div>', unsafe_allow_html=True)
    
    # Create three columns for the number input
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        selected_question = st.number_input(
            "",
            min_value=1,
            max_value=total_questions,
            value=st.session_state.current_index + 1,
            help="输入题号直接跳转到指定题目 | Enter a question number to jump to it directly",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #666;">/ {total_questions}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_question != st.session_state.current_index + 1:
        st.session_state.current_index = selected_question - 1
        st.rerun()
    
    # Add toggle switch for showing/hiding German text
    st.markdown('<div class="toggle-container">', unsafe_allow_html=True)
    st.markdown('<span class="toggle-label">显示德语 | Show German</span>', unsafe_allow_html=True)
    show_german = st.toggle("", value=st.session_state.show_german, key="study_mode_toggle")
    if show_german != st.session_state.show_german:
        st.session_state.show_german = show_german
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current pair
    current_pair = df.iloc[st.session_state.current_index]
    st.markdown(f'<p class="chinese-text">{current_pair["chinese"]}</p>', unsafe_allow_html=True)
    if st.session_state.show_german:
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
    3. 输入题号可以直接跳转到指定题目 | Enter a question number to jump to it directly
    4. 中文和德语同时显示，便于学习 | Chinese and German shown together for learning
    """) 
