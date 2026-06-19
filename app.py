import streamlit as st
import google.generativeai as genai
# הגדרת אייקון וכותרת רשמיים לאפליקציה בדפדפן ובמסך הבית
st.set_page_config(page_title="קול לילה 🌙", page_icon="🌙")
# קישור לתמונה של האייקון שלך (כרגע תמונת ירח זהב, את יכולה להחליף לכל קישור של תמונה)
ICON_URL = "https://img.icons8.com/fluency/96/crescent-moon.png"

# הזרקת קוד HTML חכם כדי שהטלפון יזהה את האייקון בשמירה למסך הבית
st.markdown(
    f"""
    <head>
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <link rel="icon" type="image/png" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-image" content="{ICON_URL}">
    </head>
    """,
    unsafe_allow_code=True
)
# --- מנגנון שמירת המפתח בכתובת האתר (Query Params) ---
# נבדוק אם יש כבר מפתח שמור בכתובת האתר
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = st.query_params.get("api_key", "")

# --- סרגל צד לבקשת מפתח API מהמשתמש ---
st.sidebar.title("הגדרות חיבור")

# תיבת הקלט מקבלת את המפתח השמור כברירת מחדל
user_api_key = st.sidebar.text_input(
    "הכניסו מפתח Gemini API:",
    value=st.session_state.user_api_key,
    type="password",
    help="המפתח יישמר בכתובת האתר ולא תצטרכי להזין אותו שוב."
)

# ברגע שהמשתמש מזין מפתח, נשמור אותו בכתובת האתר
if user_api_key and user_api_key != st.session_state.user_api_key:
    st.session_state.user_api_key = user_api_key
    st.query_params["api_key"] = user_api_key
    st.rerun()

st.sidebar.markdown("[איך משיגים מפתח בחינם?](https://aistudio.google.com/)")

# חסימת המשך הציור אם אין מפתח
if not user_api_key:
    st.info("🔑 כדי להתחיל יש להזין מפתח בסרגל הצד")
    st.stop()

# אתחול המודל עם המפתח שהמשתמש הכניס
genai.configure(api_key=user_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
# ----------------------------------------------------

# הגדרת הממשק - מותאם לקריאה רכה בלילה
st.title("קול לילה 🌙")
st.write("ברוכה הבאה למרחב ההשתקפות הלילי שלך. קחי נשימה עמוקה, ונסי לענות על שלושת העוגנים:")

# תיבות טקסט לכתיבה חופשית
thought_input = st.text_area("1. מחשבה שעולה לי עכשיו או שליוותה אותי היום:")
emotion_input = st.text_area("2. רגש דומיננטי שאני מרגישה עכשיו או שליווה אותי היום:")
action_input = st.text_area("3. פעולה שעשיתי היום:")

# כפתור ההפעלה
if st.button("צור את מדיטציית הלילה שלי"):
    # בדיקה שהמשתמשת אכן מילאה את השדות
    if thought_input and emotion_input and action_input:
        
        # בניית הפרומפט המדויק שמנחה את המודל איך לשזור את הרבדים
        prompt = f"""
        אתה מנחה מדיטציה מקצועי בשיטת 'קול לילה'. התפקיד שלך הוא לטוות את שלושת עוגני ההשתקפות שהמשתמשת שיתפה לכדי מדיטציה לילית אישית, זורמת ומרגיעה.
        
        הנה העוגנים של הערב:
        - רובד המחשבה: "{thought_input}"
        - רובד הרגש: "{emotion_input}"
        - רובד הפעולה/תנועה: "{action_input}"
        
        הנחיות קשיחות לכתיבת המדיטציה:
        1. השתמש בשפה עברית רכה, עדינה, פואטית ומכילה (פנייה בלשון נקבה כברירת מחדל).
        2. הובל את המשתמשת בהדרגה: התחל בהרגעת המחשבות והנחתן בצד, עמוק אל תוך קבלה והכלה של הרגש ללא שיפוטיות, וסיים בשחרור פיזי של תנועת ועשיית היום מהגוף והנחיית נשימות לקראת שינה.
        3. אל תשתמש בשום סימן Markdown כמו כותרות או מילים מודגשות (בלי כוכביות **, בלי סולמיות #). הטקסט צריך להיות חלק, רציף וקל לקריאה או להקראה באותו טון.
        4. אורך המדיטציה: כ-850 מילים (בערך 10 דקות הקראה איטית). סיים בברכת לילה טוב עדינה ושקט.
        """
        
        with st.spinner("אורג עבורך רגע של שקט..."):
            try:
                # שליחה לג'מיני
                response = model.generate_content(prompt)
                
                # הצגת התוצאה בממשק
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"השגיאה שגוגל החזירה היא: {e}")
    else:
        st.warning("בבקשה מלאי את שלושת השדות כדי שנוכל ליצור עבורך את המדיטציה הלילה.")
