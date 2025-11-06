import streamlit as st

st.title("Mini Quiz")

tab1, tab2 = st.tabs(["Quiz", "Dodatkowe informacje"])

questions = [
    {
        "question": "Jak robi pjes?",
        "options": ["Hau", "Miau", "Beee", "Muuu"],
        "answer": 0,
        "hint": "https://pl.wikipedia.org/wiki/Pies_domowy"
    },
    {
        "question": "Ile wynosi pierwiastek kwadratowy z 64?",
        "options": ["6", "7", "8", "9"],
        "answer": 2,
        "hint": "https://www.matemaks.pl/pierwiastek-kwadratowy.html"
    },
    {
        "question": "Który pierwiastek chemiczny ma symbol 'O'?",
        "options": ["Złoto", "Tlen", "Sód", "Wodór"],
        "answer": 1,
        "hint": "https://www.oke.gda.pl/plikiOKE/Egzamin_eksternistyczny/Informatory/Liceum/2007_11_07_lo_tablice_chemiczne.pdf"
    },
    {
        "question": "ile dni trwa rok?",
        "options": ["24", "350", "7", "365"],
        "answer": 3,
        "hint": "https://www.kalendarzswiat.pl/kalendarz/2025"
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
                st.page_link(q['hint'], label=f"podpowiedź do pytania {i+1}")
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
        with st.container():
            st.header("Statystyki")
            col11, col12, col13 = st.columns([2, 1, 1])
            with col11:
                st.metric("Liczba pytań: ", len(questions))
            with col12:    
                st.metric("Wymagane % do zaliczenia: ", (len(questions)/2)/len(questions) * 100)
            with col13:
                st.metric("Wymagany wynik: ", f"{int(len(questions)*0.5)} pkt")
    with col2:
        st.header("Poziom trudności:")
        st.write("Niski")
    with col3:
        st.header("Linki edukacyjne")
        st.page_link("https://pl.wikipedia.org/wiki/Pierwiastek_chemiczny", label="Pierwiastki chemiczne")
        st.page_link("https://www.matemaks.pl", label="Matematyka z Matemaks")


with st.expander("Rozwiń, aby zobaczyć kod źródłowy"):
    st.page_link("https://github.com/Mikku0/streamlit-cloud-test/blob/master/quiz.py", label="kod na githubie")
