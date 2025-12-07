import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math

# 20개 색상 팔레트 정의
palette_csv = [
    (0.1,0.3,0.8),(0.9,0.8,0.5),(0.9,0.4,0.3),(0.2,0.6,0.3),(0.9,0.9,0.95),
    (0.4,0.7,1.0),(1.0,0.8,0.2),(0.3,0.8,0.2),(0.9,0.2,0.4),(0.7,0.5,0.9),
    (1.0,1.0,0.4),(0.6,0.1,0.5),(0.5,1.0,0.7),(1.0,0.7,0.6),(0.5,0.25,0.1),
    (0.8,0.95,1.0),(0.6,0.6,0.6),(1.0,0.3,0.1),(0.1,0.1,0.2),(0.7,0.3,0.7)
]

def show_palette(palette, title="Palette"):
    """Display color palette as horizontal bars"""
    fig, ax = plt.subplots(figsize=(len(palette)*0.5, 1.5))
    for i, c in enumerate(palette):
        ax.fill_between([i, i+1], 0, 1, color=c)
        ax.text(i+0.5, -0.15, f"{i+1}", ha="center", va="top", fontsize=8)
    ax.axis("off")
    ax.set_xlim(0, len(palette))
    ax.set_ylim(-0.3, 1)
    ax.set_title(title, pad=10, fontsize=10, weight='bold')
    return fig

def blob(center=(0.5,0.5), r=0.3, points=200, wobble=0.15):
    """Generate a wobbly blob shape"""
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def draw_poster(n_layers=12, wobble=0.2, palette=None, seed=42, custom_text=""):
    """Generate the abstract poster"""
    random.seed(seed)
    np.random.seed(seed)
    
    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis('off')
    ax.set_facecolor((0.97, 0.97, 0.97))

    if palette is None:
        palette = [(1,0,0), (0,1,0), (0,0,1)]

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx, cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # Add text
    if custom_text:
        display_text = custom_text
    else:
        display_text = "Interactive Poster • My 20-Color Palette"
    
    ax.text(0.05, 0.95, display_text,
            transform=ax.transAxes, fontsize=12, weight="bold")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

# Streamlit App Configuration
st.set_page_config(page_title="20-Color Palette Poster", page_icon="🎨", layout="wide")

st.title("🎨 20색 팔레트 포스터 생성기")
st.markdown("20가지 컬러 팔레트를 활용한 추상 아트를 만들어보세요!")

# Show color palette
st.subheader("🌈 컬러 팔레트")
palette_fig = show_palette(palette_csv, "My 20-Color Palette")
st.pyplot(palette_fig)
plt.close(palette_fig)

st.markdown("---")

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ 설정")
    
    # Layer settings
    n_layers = st.slider("레이어 수", min_value=3, max_value=30, value=12, step=1,
                        help="더 많은 레이어 = 더 복잡한 패턴")
    
    wobble = st.slider("흔들림 정도", min_value=0.0, max_value=0.5, value=0.2, step=0.05,
                      help="Blob의 불규칙성 정도")
    
    seed = st.number_input("시드 값", min_value=0, value=42, step=1,
                          help="같은 시드 = 같은 패턴")
    
    st.markdown("---")
    
    # Text customization
    st.markdown("#### 📝 텍스트")
    custom_text = st.text_input("포스터 텍스트 (비워두면 기본값 사용)", 
                                value="",
                                placeholder="Interactive Poster • My 20-Color Palette")
    
    st.markdown("---")
    
    # Color selection
    st.markdown("#### 🎨 색상 선택")
    use_all_colors = st.checkbox("모든 20색 사용", value=True)
    
    if not use_all_colors:
        st.markdown("사용할 색상 선택 (번호):")
        selected_colors = st.multiselect(
            "색상 번호",
            options=list(range(1, 21)),
            default=[1, 2, 3, 4, 5],
            help="팔레트에서 사용할 색상의 번호를 선택하세요"
        )
        if selected_colors:
            selected_palette = [palette_csv[i-1] for i in selected_colors]
        else:
            selected_palette = palette_csv
    else:
        selected_palette = palette_csv
    
    st.markdown("---")
    
    # Generate buttons
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🎲 새 패턴", use_container_width=True):
            st.session_state.seed = random.randint(0, 10000)
            st.rerun()
    
    with col_b:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.seed = 42
            st.rerun()
    
    # Update seed if stored in session state
    if 'seed' in st.session_state:
        seed = st.session_state.seed

with col2:
    st.subheader("🖼️ 포스터")
    
    # Generate poster
    with st.spinner("포스터를 생성하는 중..."):
        poster_fig = draw_poster(
            n_layers=n_layers,
            wobble=wobble,
            palette=selected_palette,
            seed=seed,
            custom_text=custom_text
        )
        st.pyplot(poster_fig)
        plt.close(poster_fig)

# Footer
st.markdown("---")
st.markdown("""
### 💡 사용 팁
- **레이어 수**: 3-10은 심플한 디자인, 15-30은 복잡한 디자인
- **흔들림 정도**: 0.0은 부드러운 원형, 0.5는 매우 불규칙한 형태
- **색상 선택**: 특정 색상만 사용하고 싶다면 "모든 20색 사용" 체크 해제
- **시드 값 저장**: 마음에 드는 패턴의 시드 값을 기록해두세요!

#### 색상 팔레트 가이드
1-5: 블루, 베이지, 오렌지, 그린, 화이트  
6-10: 스카이블루, 골드, 라임, 핑크, 라벤더  
11-15: 옐로우, 퍼플, 민트, 피치, 브라운  
16-20: 아이스블루, 그레이, 레드, 네이비, 자주
""")

# Sidebar
st.sidebar.header("ℹ️ 정보")
st.sidebar.info(
    "이 앱은 20가지 컬러 팔레트를 사용하여 "
    "독특한 추상 포스터를 생성합니다. "
    "다양한 설정을 조합하여 무한한 디자인을 만들어보세요!"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**현재 설정:**")
st.sidebar.text(f"레이어: {n_layers}")
st.sidebar.text(f"흔들림: {wobble}")
st.sidebar.text(f"시드: {seed}")
st.sidebar.text(f"사용 색상: {len(selected_palette)}개")
