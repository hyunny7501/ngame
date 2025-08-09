import streamlit as st
import time
from gemini_service import GeminiNRowService

def main():
    """Main Streamlit application for Korean N-행시 generator"""
    
    # Set page configuration
    st.set_page_config(
        page_title="🌟 N행시 만들기",
        page_icon="🎨",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if 'poem_history' not in st.session_state:
        st.session_state.poem_history = []
    
    # Main header with emojis and styling
    st.title("🌟 N행시 만들기 🎨")
    st.markdown("### 🤖 AI와 함께하는 재미있는 단어놀이!")
    
    # Subtitle with instructions
    st.markdown("""
    <div style='background-color: #E8F4FD; padding: 15px; border-radius: 10px; margin: 20px 0;'>
        <h4 style='color: #2E3440; margin: 0;'>🎯 사용법</h4>
        <p style='color: #2E3440; margin: 5px 0 0 0;'>
            ✨ 한글 단어를 입력하면 AI가 재미있는 N행시를 만들어줘요!<br>
            ✍️ 여러분도 직접 N행시를 써보고 AI와 비교해보세요!<br>
            🏆 창의력을 키우는 즐거운 단어놀이를 시작해보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown("#### 📝 단어를 입력해주세요")
    
    # Create columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_word = st.text_input(
            label="한글 단어",
            placeholder="예: 바다, 친구, 꿈, 사랑...",
            help="2-10글자의 한글 단어를 입력해주세요",
            label_visibility="collapsed"
        )
    
    with col2:
        generate_button = st.button("✨ N행시 만들기", type="primary", use_container_width=True)
    
    # Show examples
    with st.expander("💡 단어 예시"):
        example_words = ["바다", "친구", "꿈", "사랑", "행복", "가족", "학교", "놀이", "여행", "음식"]
        
        # Create clickable example buttons
        st.markdown("**클릭하면 자동으로 입력돼요!**")
        example_cols = st.columns(5)
        
        for i, word in enumerate(example_words):
            with example_cols[i % 5]:
                if st.button(f"🎯 {word}", key=f"example_{word}"):
                    st.session_state.example_word = word
                    st.rerun()
    
    # Handle example word selection
    if 'example_word' in st.session_state:
        user_word = st.session_state.example_word
        del st.session_state.example_word
        st.rerun()
    
    # Handle word input and user creation first
    if user_word and len(user_word.strip()) > 0:
        # Initialize Gemini service for validation
        try:
            gemini_service = GeminiNRowService()
            
            # Validate input
            is_valid, error_msg = gemini_service.validate_korean_word(user_word)
            
            if not is_valid:
                st.error(error_msg)
                return
                
            clean_word = user_word.strip()
            
            # Show user input section first
            st.markdown("---")
            st.markdown("### ✍️ 먼저 여러분이 N행시를 만들어보세요!")
            
            # Store user poem in session state
            if f'user_poem_{clean_word}' not in st.session_state:
                st.session_state[f'user_poem_{clean_word}'] = [''] * len(clean_word)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                       padding: 25px; border-radius: 15px; margin: 20px 0;
                       box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                <h4 style='color: #333; text-align: center; margin-bottom: 20px;'>
                    ✨ "{user_word}" N행시 만들기 ✨
                </h4>
                <div style='background-color: white; padding: 20px; border-radius: 10px;'>
            """, unsafe_allow_html=True)
            
            # Create input fields for each character
            user_poem_lines = []
            for i, char in enumerate(clean_word):
                user_line = st.text_input(
                    f"[{char}]로 시작하는 문장을 써보세요:",
                    value=st.session_state[f'user_poem_{clean_word}'][i],
                    key=f"user_line_{clean_word}_{i}",
                    placeholder=f"[{char}]..."
                )
                st.session_state[f'user_poem_{clean_word}'][i] = user_line
                user_poem_lines.append(f"[{char}] {user_line}" if user_line else f"[{char}] ...")
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Show user's complete poem preview
            if any(line.strip() for line in st.session_state[f'user_poem_{clean_word}']):
                st.markdown("**📝 내가 만든 N행시 미리보기:**")
                user_poem_preview = "\n".join(user_poem_lines)
                st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                           font-size: 16px; line-height: 1.6; border-left: 4px solid #ff6b6b;
                           white-space: pre-line; font-weight: 500;'>
                    {user_poem_preview}
                </div>
                """, unsafe_allow_html=True)
            
            # Button to generate AI version for comparison
            st.markdown("### 🤖 이제 AI와 비교해볼까요?")
            
            if st.button("🎯 AI N행시 보기 & 비교하기", type="primary", use_container_width=True):
                # Generate AI poem
                with st.spinner("🎨 AI가 창의적인 N행시를 만들고 있어요..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    # Generate the poem
                    poem = gemini_service.generate_nrow_poem(user_word.strip())
                    st.session_state[f'ai_poem_{clean_word}'] = poem
                
        except Exception as e:
            st.error(f"오류가 발생했어요: {str(e)} 😢")
            st.info("잠시 후 다시 시도해주세요! 🔄")
                
    # Show comparison if AI poem exists
    if user_word and len(user_word.strip()) > 0:
        clean_word = user_word.strip()
        if f'ai_poem_{clean_word}' in st.session_state:
            poem = st.session_state[f'ai_poem_{clean_word}']
            
            # Display comparison results
            st.markdown("---")
            st.markdown("### 🏆 비교 결과")
            
            # Create two columns for comparison
            col_user, col_ai = st.columns(2)
            
            with col_user:
                st.markdown("#### ✍️ 내가 만든 N행시")
                user_poem_complete = ""
                if f'user_poem_{clean_word}' in st.session_state:
                    user_lines = [line for line in st.session_state[f'user_poem_{clean_word}'] if line.strip()]
                    if user_lines:
                        user_poem_complete = "\n".join([f"[{clean_word[i]}] {line}" for i, line in enumerate(st.session_state[f'user_poem_{clean_word}']) if line.strip()])
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                           padding: 20px; border-radius: 15px; margin: 10px 0;
                           box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                    <h5 style='color: #333; text-align: center; margin-bottom: 15px;'>
                        ✨ "{user_word}" (내 작품) ✨
                    </h5>
                    <div style='background-color: white; padding: 15px; border-radius: 10px;
                               font-size: 16px; line-height: 1.6; font-weight: 500;
                               color: #2E3440; white-space: pre-line;'>
                        {user_poem_complete if user_poem_complete else "아직 작성하지 않았어요!"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_ai:
                st.markdown("#### 🤖 AI가 만든 N행시")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           padding: 20px; border-radius: 15px; margin: 10px 0;
                           box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
                    <h5 style='color: white; text-align: center; margin-bottom: 15px;'>
                        ✨ "{user_word}" (AI 작품) ✨
                    </h5>
                    <div style='background-color: white; padding: 15px; border-radius: 10px;
                               font-size: 16px; line-height: 1.6; font-weight: 500;
                               color: #2E3440; white-space: pre-line;'>
                        {poem}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Enhanced feedback section with diverse messages
            if user_poem_complete:
                st.markdown("---")
                st.markdown("### 🎉 멋진 작품이 완성되었어요!")
                
                # Diverse encouragement messages with icons and two lines
                import random
                encouragement_messages = [
                    ("🌟✨", "와! 정말 창의적인 N행시예요!", "상상력이 넘쳐나는 멋진 작품이네요!"),
                    ("🎨🎭", "예술가처럼 아름다운 표현이에요!", "감성이 풍부한 시를 만들었어요!"),
                    ("🏆👑", "최고의 작품! 진짜 대단해요!", "이런 훌륭한 N행시는 처음 봐요!"),
                    ("💎🌈", "보석같이 빛나는 단어들이에요!", "무지개처럼 다채로운 표현력이 놀라워요!"),
                    ("🚀⭐", "우주로 날아갈 만큼 멋져요!", "별처럼 반짝이는 아이디어가 가득해요!"),
                    ("🎪🎊", "축제처럼 즐거운 N행시네요!", "파티가 열릴 만큼 신나는 작품이에요!"),
                    ("🌸🦋", "꽃처럼 아름다운 글이에요!", "나비처럼 우아하게 표현했네요!"),
                    ("🔥💫", "열정이 가득 담긴 작품이에요!", "번개처럼 번뜩이는 아이디어예요!"),
                    ("🎵🎶", "음악처럼 리듬감 있는 시네요!", "멜로디가 들리는 것 같아요!"),
                    ("🌙☀️", "달빛처럼 신비로운 표현이에요!", "햇살처럼 따뜻한 마음이 담겨있어요!")
                ]
                
                icon, line1, line2 = random.choice(encouragement_messages)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ffeaa7, #fab1a0); 
                           padding: 20px; border-radius: 12px; margin: 15px 0;
                           box-shadow: 0 3px 10px rgba(0,0,0,0.1); text-align: center;'>
                    <div style='font-size: 24px; margin-bottom: 10px;'>{icon}</div>
                    <div style='font-size: 18px; font-weight: bold; color: #2d3436; margin-bottom: 5px;'>{line1}</div>
                    <div style='font-size: 16px; color: #636e72;'>{line2}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Action buttons for comparison view
            st.markdown("### 🎯 다음 단계")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🔄 다시 생성", help="AI가 새로운 N행시를 만들어줘요"):
                    if f'ai_poem_{clean_word}' in st.session_state:
                        del st.session_state[f'ai_poem_{clean_word}']
                    st.rerun()
            
            with col2:
                if st.button("📋 AI 복사", help="AI 작품을 복사해요"):
                    st.code(f'"{user_word}" N행시 (AI 작품)\n\n{poem}', language=None)
                    st.success("AI N행시가 복사 영역에 표시되었어요!")
            
            with col3:
                if user_poem_complete and st.button("✍️ 내 작품 복사", help="내 작품을 복사해요"):
                    st.code(f'"{user_word}" N행시 (내 작품)\n\n{user_poem_complete}', language=None)
                    st.success("내 N행시가 복사 영역에 표시되었어요!")
            
            with col4:
                if st.button("🎲 다른 단어로", help="새로운 단어로 시작해요"):
                    # Clear all session data for new word
                    keys_to_remove = [key for key in st.session_state.keys() if isinstance(key, str) and (key.startswith(f'user_poem_{clean_word}') or key.startswith(f'ai_poem_{clean_word}'))]
                    for key in keys_to_remove:
                        del st.session_state[key]
                    if 'example_word' in st.session_state:
                        del st.session_state.example_word
                    st.rerun()
            
            # Add to history (both poems)
            if user_poem_complete and poem:  # Only save when both exist
                st.session_state.poem_history.append({
                    'word': user_word.strip(),
                    'ai_poem': poem,
                    'user_poem': user_poem_complete,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
    
    # Show history if available
    if st.session_state.poem_history:
        st.markdown("---")
        with st.expander(f"📚 지금까지 만든 N행시 ({len(st.session_state.poem_history)}개)"):
            for i, entry in enumerate(reversed(st.session_state.poem_history[-5:])):  # Show last 5
                # Handle both old format (poem) and new format (ai_poem, user_poem)
                ai_poem = entry.get('ai_poem', entry.get('poem', ''))
                user_poem = entry.get('user_poem', '')
                
                st.markdown(f"""
                <div style='background-color: #F8F9FA; padding: 15px; border-radius: 8px; margin: 10px 0;
                           border-left: 4px solid #FF6B6B;'>
                    <strong>🎯 "{entry['word']}"</strong> 
                    <small style='color: #666;'>({entry['timestamp']})</small>
                """, unsafe_allow_html=True)
                
                if user_poem:
                    # Show both AI and user versions
                    hist_col1, hist_col2 = st.columns(2)
                    with hist_col1:
                        st.markdown("**🤖 AI 버전:**")
                        st.markdown(f"""
                        <div style='background-color: #E3F2FD; padding: 10px; border-radius: 5px; 
                                   font-size: 13px; line-height: 1.4; white-space: pre-line;'>
                            {ai_poem}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with hist_col2:
                        st.markdown("**✍️ 내 버전:**")
                        st.markdown(f"""
                        <div style='background-color: #FCE4EC; padding: 10px; border-radius: 5px; 
                                   font-size: 13px; line-height: 1.4; white-space: pre-line;'>
                            {user_poem}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Show only AI version (backward compatibility)
                    st.markdown(f"""
                    <div style='margin-top: 10px; white-space: pre-line; font-size: 14px;'>
                        {ai_poem}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            if len(st.session_state.poem_history) > 5:
                st.info(f"+ {len(st.session_state.poem_history) - 5}개 더 있어요!")
            
            if st.button("🗑️ 기록 지우기"):
                st.session_state.poem_history = []
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px; margin-top: 30px;'>
        <p>🤖 Powered by Gemini AI | 만든 N행시를 가족이나 친구들과 공유해보세요! 📱</p>
        <p>💡 <strong>팁:</strong> AI와 자신의 N행시를 비교해보며 창의력을 키워보세요!</p>
        <p>🎨 <strong>도전:</strong> 다양한 단어로 시도해보면 더 재미있는 N행시를 만날 수 있어요!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
