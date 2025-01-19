import streamlit as st

class TaskInfo:
    def show(self):
        st.write("""
        **Cel zadania:**  
        1. Zalogować się do systemu robotów i pobrać firmware. 
        
        **Wymagania:**
        1. Zalogować się do systemu pod adresem xyz.ag3nts.org używając poświadczeń:
           - Login: tester
           - Hasło: 574e112a        
        
        2. Obejść system anty-captcha poprzez:
           - Pobranie aktualnego pytania ze strony (zmienia się co 7 sekund)
           - Wysłanie pytania do LLM w celu uzyskania odpowiedzi
           - Wysłanie formularza z danymi logowania i odpowiedzią        
        
        3. Po udanym logowaniu:
           - Pobrać firmware robota
           - Zapisać odpowiedź HTML
        """) 