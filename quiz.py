import streamlit as st

st.title("Mini Quiz")

questions = [
    {
        "question": "Jak robi pjes?",
        "options": ["Hau", "Miau", "Beee", "Muuu"],
        "answer": 0
    },
    {
        "question": "Ile wynosi pierwiastek kwadratowy z 64?",
        "options": ["6", "7", "8", "9"],
        "answer": 2
    },
    {
        "question": "Który pierwiastek chemiczny ma symbol 'O'?",
        "options": ["Złoto", "Tlen", "Sód", "Wodór"],
        "answer": 1
    },
    {
        "question": "ile dni trwa rok?",
        "options": ["24", "350", "7", "365"],
        "answer": 3
    }
]

user_answers = []
score = 0

with st.form("quiz_form"):
    for i, q in enumerate(questions):
        user_choice = st.radio(f"{i+1}. {q['question']}", q["options"], key=i, index=None)
        user_answers.append(user_choice)
    submitted = st.form_submit_button("Sprawdź wynik")

if submitted:
    for i, q in enumerate(questions):
        if user_answers[i] is None:
            st.error(f"Nie zaznaczono odpowiedzi w pytaniu {i+1}.")
            continue
        if q["options"].index(user_answers[i]) == q["answer"]:
            score += 1

    if score/len(questions) >= 0.5:
        st.success(f"Twój wynik: {score} / {len(questions)}")
    else:
        st.error(f"Twój wynik: {score} / {len(questions)}")


col1, col2, col3 = st.columns(3)
with col1:
    st.header("Kolumna 1")
    st.button("Przycisk 1")
with col2:
    st.header("Kolumna 2")
    st.button("Przycisk 2")
with col3:
    st.header("Kolumna 3")
    st.button("Przycisk 3")