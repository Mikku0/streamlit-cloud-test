import streamlit as st

st.title("Mini Quiz")

tab1, tab2 = st.tabs(["Quiz", "Kolumny"])

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
with tab1:
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            user_choice = st.radio(f"{i+1}. {q['question']}", q["options"], key=i, index=None)
            user_answers.append(user_choice)
            with st.expander("Podpowiedź:"):
                st.page_link("https://pl.wikipedia.org/wiki/Pies_domowy", label="podpowiedź do pytania 1")
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

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
    
    with col2:
        st.header("Kolumna 2")
        st.button("Przycisk 2")
    with col3:
        st.header("Kolumna 3")
        st.button("Przycisk 3")

with st.expander("Rozwiń, aby zobaczyć kod źródłowy"):
    st.page_link("https://github.com/Mikku0/streamlit-cloud-test/blob/master/quiz.py", label="kod na githubie")

st.sidebar.title("Panel boczny")
selected_option = st.sidebar.selectbox("Wybierz opcję",["Strona główna", "Analiza danych", "Wizualizacje"])
if selected_option == "Strona główna":
    st.write("Witamy na stronie głównej")
elif selected_option == "Analiza danych":
    st.write("Sekcja analizy danych")
else:
    st.write("Sekcja wizualizacji")