import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random


class QuizGUI:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Ενδεικτικές Ερωτήσεις")
        self.root.geometry("800x750")
        self.root.configure(bg="#ecf0f1")
        self.questions = questions
        random.shuffle(self.questions)  # Randomize question order
        self.score = 0
        self.index = 0
        self.selected = tk.IntVar(value=-1)
        self.selected_multiple = {}
        self.fill_blanks_vars = {}
        self.wrong_answers = []

        # Header
        header_frame = tk.Frame(root, bg="#1e3c72")
        header_frame.pack(fill="x")

        self.title_label = tk.Label(header_frame, text="📚 Ενδεικτικές Ερωτήσεις", font=("Segoe UI", 26, "bold"), fg="white", bg="#1e3c72")
        self.title_label.pack(pady=16)

        self.progress_label = tk.Label(header_frame, text="", font=("Segoe UI", 11), fg="#b0c4de", bg="#1e3c72")
        self.progress_label.pack(pady=(0, 12))

        # Main frame
        content_frame = tk.Frame(root, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Question box
        question_box = tk.Frame(content_frame, bg="white", relief=tk.FLAT, bd=0)
        question_box.pack(fill="x", pady=(0, 20))
        
        question_inner = tk.Frame(question_box, bg="white")
        question_inner.pack(fill="x", padx=16, pady=16)

        self.question_label = tk.Label(question_inner, text="", font=("Segoe UI", 14, "bold"), wraplength=700, justify="left", bg="white", fg="#1e3c72")
        self.question_label.pack(fill="x", anchor="w")

        self.options_frame = tk.Frame(content_frame, bg="#ecf0f1")
        self.options_frame.pack(fill="both", expand=True, anchor="nw")

        # Button frame
        button_frame = tk.Frame(root, bg="#ecf0f1")
        button_frame.pack(fill="x", padx=25, pady=15)

        self.next_button = tk.Button(button_frame, text="➜ Επόμενη Ερώτηση", command=self.next_question, font=("Segoe UI", 12, "bold"), bg="#2196F3", fg="white", padx=40, pady=12, cursor="hand2", activebackground="#1976D2", relief=tk.FLAT, bd=0)
        self.next_button.pack(side="right")

        self.load_question()

    def load_question(self):
        self.selected.set(-1)
        self.selected_multiple = {}
        self.fill_blanks_vars = {}
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        q = self.questions[self.index]
        self.question_label.config(text=q['question'])
        self.progress_label.config(text=f"Question {self.index + 1} of {len(self.questions)}")

        # Check question type
        question_type = q.get("type", "single")
        
        if question_type == "fill_blanks":
            # Handle fill-in-the-blanks question
            for i, blank_options in enumerate(q["blanks"]):
                # Frame for each blank with border
                blank_frame = tk.Frame(self.options_frame, bg="#ecf0f1")
                blank_frame.pack(fill="x", pady=14)
                
                # Label for blank
                label = tk.Label(blank_frame, text=f"Επιλογή {i+1}:", font=("Segoe UI", 12, "bold"), bg="#ecf0f1", fg="#1e3c72")
                label.pack(anchor="w", padx=2, pady=(0, 8))
                
                dropdown_container = tk.Frame(blank_frame, bg="white", relief=tk.SOLID, bd=2, highlightthickness=1, highlightbackground="#2196F3")
                dropdown_container.pack(anchor="w", padx=16, pady=2, fill="x")
                
                var = tk.StringVar(value="-- Επιλογή --")
                self.fill_blanks_vars[i] = var
                
                style = ttk.Style()
                style.theme_use('clam')
                style.configure('TCombobox', font=("Segoe UI", 11), fieldbackground="white", foreground="#1e3c72")
                
                dropdown = ttk.Combobox(dropdown_container, textvariable=var, values=["-- Επιλογή --"] + blank_options, 
                                       state="readonly", font=("Segoe UI", 11), width=60)
                dropdown.pack(fill="both", expand=True, padx=0, pady=0)
                dropdown.set("-- Επιλογή --")
        
        elif question_type == "multi_select" or (", " in str(q.get("correct", "")) and len([part.strip() for part in str(q.get("correct", "")).split(",")]) > 1 and all(part.strip() in q.get("options", []) for part in str(q.get("correct", "")).split(","))):
            # Handle multi-select question
            for i, option in enumerate(q["options"]):
                var = tk.BooleanVar(value=False)
                self.selected_multiple[i] = var
                cb = tk.Checkbutton(
                    self.options_frame,
                    text=option,
                    variable=var,
                    anchor="w",
                    justify="left",
                    wraplength=700,
                    font=("Segoe UI", 11),
                    bg="#ecf0f1",
                    fg="#1e3c72",
                    selectcolor="#2196F3",
                    activebackground="#ecf0f1",
                    activeforeground="#1e3c72",
                    padx=12,
                    pady=10
                )
                cb.pack(fill="x", pady=6)
        else:
            # Handle regular single-select question with radiobuttons
            for i, option in enumerate(q["options"]):
                rb = tk.Radiobutton(
                    self.options_frame,
                    text=option,
                    variable=self.selected,
                    value=i,
                    anchor="w",
                    justify="left",
                    wraplength=700,
                    font=("Segoe UI", 11),
                    bg="#ecf0f1",
                    fg="#1e3c72",
                    selectcolor="#2196F3",
                    activebackground="#ecf0f1",
                    activeforeground="#1e3c72",
                    padx=12,
                    pady=10
                )
                rb.pack(fill="x", pady=6)

        if self.index == len(self.questions) - 1:
            self.next_button.config(text="Τέλος")
        else:
            self.next_button.config(text="Επόμενη")

    def next_question(self):
        # Check if quiz is already finished
        if self.index >= len(self.questions):
            return
            
        q = self.questions[self.index]
        question_type = q.get("type", "single")
        is_correct = False
        
        if question_type == "fill_blanks":
            # Handle fill-in-the-blanks question
            selected_blanks = [self.fill_blanks_vars[i].get().strip() for i in range(len(q["blanks"]))]
            expected_blanks = [ans.strip() for ans in q["correct"]]
            
            # Check if any blank is empty or still has the placeholder
            unfilled = []
            for i, blank in enumerate(selected_blanks):
                if blank == "" or blank == "-- Επιλογή --":
                    unfilled.append(i + 1)
            
            if unfilled:
                blank_list = ", ".join(map(str, unfilled))
                messagebox.showwarning("Ημιτελής σύμπλήρωση", f"Παρακαλώ συμπλήρωσε την/τις επιλογή/{unfilled} που λείπει.")
                return
            
            # Check if selected answers match correct answers
            if selected_blanks == expected_blanks:
                self.score += 1
                is_correct = True
            else:
                # Store wrong answer info
                self.wrong_answers.append({
                    "question_num": self.index + 1,
                    "question": q["question"],
                    "correct": ", ".join(expected_blanks)
                })
        
        elif question_type == "multi_select" or (", " in str(q.get("correct", "")) and len([part.strip() for part in str(q.get("correct", "")).split(",")]) > 1 and all(part.strip() in q.get("options", []) for part in str(q.get("correct", "")).split(","))):
            # Handle multi-select question
            selected_options = [q["options"][i] for i in range(len(q["options"])) if self.selected_multiple[i].get()]
            
            correct_answers = [ans.strip() for ans in q["correct"].split(",")]
            num_correct = len(correct_answers)
            
            if not selected_options:
                messagebox.showwarning("Επέλεξε απαντήσεις", "Παρακαλώ επέλεξε τουλάχιστον μια επιλογή.")
                return
            
            # Check if user selected the right number of answers
            if len(selected_options) < num_correct:
                messagebox.showwarning("Ανεπαρκείς επιλογές", f"Παρακαλώ επέλεξε {num_correct} επιλογές. Έχεις επιλέξει μόνο {len(selected_options)}.")
                return
            elif len(selected_options) > num_correct:
                messagebox.showwarning("Υπερβολικές επιλογές", f"Παρακαλώ επέλεξε ακριβώς {num_correct} επιλογές. Έχεις επιλέξει {len(selected_options)}.")
                return
            
            # Check if selected answers match correct answers
            if sorted(selected_options) == sorted(correct_answers):
                self.score += 1
                is_correct = True
            else:
                # Store wrong answer info
                self.wrong_answers.append({
                    "question_num": self.index + 1,
                    "question": q["question"],
                    "correct": ", ".join(correct_answers)
                })
        
        else:
            # Handle single-select question
            choice = self.selected.get()
            if choice < 0:
                messagebox.showwarning("Επέλεξε απάντηση", "Παρακαλώ επέλεξε μια επιλογή.")
                return

            if q["options"][choice] == q["correct"]:
                self.score += 1
                is_correct = True
            else:
                # Store wrong answer info
                self.wrong_answers.append({
                    "question_num": self.index + 1,
                    "question": q["question"],
                    "correct": q["correct"]
                })

        self.index += 1
        if self.index < len(self.questions):
            self.load_question()
        else:
            self.next_button.config(state="disabled")
            self.show_results()

    def show_results(self):
        total = len(self.questions)
        percentage = (self.score / total) * 100
        
        results_window = tk.Toplevel(self.root)
        results_window.title("Αποτελέσματα Κουίζ")
        results_window.geometry("900x700")
        results_window.configure(bg="#ecf0f1")
        
        header_frame = tk.Frame(results_window, bg="#1e3c72")
        header_frame.pack(fill="x")
        
        title_label = tk.Label(header_frame, text="✓ Αποτελέσματα", font=("Segoe UI", 24, "bold"), fg="white", bg="#1e3c72")
        title_label.pack(pady=18)
        
        if percentage == 100:
            score_text = f"🎉 Συγχαρητήρια!!! 🎉"
        elif percentage >= 80:
            score_text = f"⭐ Μπράβο!"
        elif percentage >= 60:
            score_text = f"👍 Καλή προσπάθεια!"
        else:
            score_text = f"💪 Συνέχισε την εξάσκηση!"
        
        score_label = tk.Label(header_frame, text=f"{score_text}\n\nΒαθμός: {self.score}/{total} ({percentage:.1f}%)", 
                               font=("Segoe UI", 15, "bold"), fg="white", bg="#1e3c72")
        score_label.pack(pady=18)
        
        button_frame = tk.Frame(results_window, bg="#ecf0f1")
        button_frame.pack(fill="x", padx=20, pady=15, side="bottom")
        
        button_container = tk.Frame(button_frame, bg="#ecf0f1")
        button_container.pack(anchor="center")
        
        restart_button = tk.Button(button_container, text="🔄 Επανάληψη", command=lambda: self.restart_quiz(results_window), 
                                 font=("Segoe UI", 12, "bold"), bg="#4CAF50", fg="white", 
                                 padx=30, pady=12, cursor="hand2", relief=tk.RAISED, bd=2)
        restart_button.pack(side="left", padx=15)
        
        close_button = tk.Button(button_container, text="✕ Κλείσε", command=self.root.destroy, 
                                 font=("Segoe UI", 12, "bold"), bg="#f44336", fg="white", 
                                 padx=30, pady=12, cursor="hand2", relief=tk.RAISED, bd=2)
        close_button.pack(side="left", padx=15)
        
        content_frame = tk.Frame(results_window, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=22, pady=22, side="top")
        
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(content_frame, yscrollcommand=scrollbar.set, font=("Segoe UI", 11), 
                              wrap="word", bg="white", fg="#2c3e50")
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        results_text = ""
        
        if self.wrong_answers:
            results_text += "ΛΑΘΟΣ ΑΠΑΝΤΗΣΕΙΣ:\n"
            results_text += "="*70 + "\n\n"
            for wrong in self.wrong_answers:
                results_text += f"Ερώτηση {wrong['question_num']}:\n"
                results_text += f"{wrong['question']}\n"
                results_text += f"Σωστή Απάντηση: {wrong['correct']}\n"
                results_text += "-"*70 + "\n\n"
        else:
            results_text = "Συγχαρητήρια! Απάντησες σωστά σε όλες τις ερωτήσεις!"
        
        text_widget.insert("1.0", results_text)
        text_widget.config(state="disabled")

    def restart_quiz(self, results_window):
        """Restart the quiz by resetting all variables and closing the results window"""
        results_window.destroy()
        self.score = 0
        self.index = 0
        self.selected.set(-1)
        self.selected_multiple = {}
        self.fill_blanks_vars = {}
        self.wrong_answers = []
        self.next_button.config(state="normal") 
        random.shuffle(self.questions)
        self.load_question()


if __name__ == "__main__":
    quiz_questions = [
        {"question": "Η σύνταξη προτροπών (prompt engineering) αφορά τη δημιουργία οδηγιών ή ερωτήσεων προς ένα μοντέλο ΤΝ με σκοπό την παραγωγή κατάλληλης απόκρισης.", "options": ["Σωστό", "Λάθος"], "correct": "Σωστό"},
        {"question": "Ποιο από τα παρακάτω θεωρείται ηθικός προβληματισμός που συνδέεται με τη χρήση Βοηθών ΤΝ;", "options": ["Η διευκόλυνση της καθημερινότητας των χρηστών", "Η δυνατότητα κατανόησης πολλών γλωσσών", "Η παρακολούθηση και καταγραφή προσωπικών συνομιλιών", "Η άμεση απόκριση σε ερωτήματα του χρήστη"], "correct": "Η παρακολούθηση και καταγραφή προσωπικών συνομιλιών"},
        {"question": "Επιβλεπόμενη μάθηση είναι η διαδικασία όπου ο αλγόριθμος…", "options": ["κατασκευάζει μια συνάρτηση που απεικονίζει δεδομένες εισόδους σε γνωστές επιθυμητές εξόδους", "κατασκευάζει ένα μοντέλο για κάποιο σύνολο εισόδων υπό μορφή παρατηρήσεων χωρίς να γνωρίζει τις επιθυμητές εξόδους", "μαθαίνει μια στρατηγική ενεργειών μέσα από άμεση αλληλεπίδραση με το περιβάλλον"], "correct": "κατασκευάζει μια συνάρτηση που απεικονίζει δεδομένες εισόδους σε γνωστές επιθυμητές εξόδους"},
        {"question": "Ποια είναι η βασική διαφορά μεταξύ της τεχνικής διεθνοποίησης (Internationalization) και της τεχνικής τοπικοποίησης (Localization);", "options": ["Η διεθνοποίηση αναφέρεται στη διαδικασία προσαρμογής ενός προϊόντος σε μια συγκεκριμένη γλώσσα ενώ η τοπικοποίηση στον σχεδιασμό ενός προϊόντος ώστε να είναι εύκολα προσαρμόσιμο σε διάφορες γλώσσες και περιοχές", "Η τοπικοποίηση αναφέρεται στη διαδικασία σχεδιασμού λογισμικού που το καθιστά προσαρμόσιμο για χρήση σε διάφορες γλώσσες και περιοχές ενώ η διεθνοποίηση στη διαδικασία προσαρμογής ενός προϊόντος σε συγκεκριμένη γλώσσα μιας συγκεκριμένης περιοχής", "Η διεθνοποίηση αφορά στον σχεδιασμό ενός προϊόντος ώστε να είναι εύκολα προσαρμόσιμο σε διάφορες γλώσσες και περιοχές, ενώ η τοπικοποίηση στην προσαρμογή του προϊόντος σε τοπικές πρακτικές και πολιτιστικές προτιμήσεις"], "correct": "Η διεθνοποίηση αφορά στον σχεδιασμό ενός προϊόντος ώστε να είναι εύκολα προσαρμόσιμο σε διάφορες γλώσσες και περιοχές, ενώ η τοπικοποίηση στην προσαρμογή του προϊόντος σε τοπικές πρακτικές και πολιτιστικές προτιμήσεις"},
        {"question": "Επιλέξτε τρία (3) πλεονεκτήματα της γλώσσας προγραμματισμού τεχνητής νοημοσύνης Haskell.", "options": ["Οι δομές δεδομένων είναι άρτια σχεδιασμένες", "Τα κυριότερα σημεία της γλώσσας ενισχύουν μια συνθετική μέθοδο για την έκφραση των αλγορίθμων", "Η εργασία με τα γραφήματα είναι περίπλοκες" , "Τα monads Rundown και LogicT καθιστούν απλή την έκφραση μη ντετερμινιστικών αλγορίθμων"], "correct": "Οι δομές δεδομένων είναι άρτια σχεδιασμένες, Τα κυριότερα σημεία της γλώσσας ενισχύουν μια συνθετική μέθοδο για την έκφραση των αλγορίθμων, Τα monads Rundown και LogicT καθιστούν απλή την έκφραση μη ντετερμινιστικών αλγορίθμων"},
        {"question": "Το Τμήμα Ασφάλειας Ηλεκτρονικών και Τηλεφωνικών Επικοινωνιών ανήκει…", "options": ["στη Διεύθυνσης Δίωξης Ηλεκτρονικού Εγκλήματος (ΔΙ.Δ.Η.Ε.)", "στη Διεύθυνση Κυβερνοχώρου της Εθνικής Υπηρεσίας Πληροφοριών", "στην Αρχή Διασφάλισης του Απορρήτου των Επικοινωνιών (ΑΔΑΕ)", "στην Εθνική Επιτροπή Τηλεπικοινωνιών και Ταχυδρομείων"], "correct": "στη Διεύθυνσης Δίωξης Ηλεκτρονικού Εγκλήματος (ΔΙ.Δ.Η.Ε.)"},
        {"question": "Οι \"καινοτόμοι\" ηγέτες διαδραματίζουν αποφασιστικό ρόλο στη σχεδίαση του επιχειρηματικού μοντέλου και στην υιοθέτηση τεχνολογιών Τεχνητής Νοημοσύνης", "options": ["Σωστό", "Λάθος"], "correct": "Σωστό"},
        {"question": "Τα μοντέλα τεχνητής νοημοσύνης (AI) που βασίζονται σε αλγορίθμους, μπορούν να χρησιμοποιηθούν για να εκτιμήσουν τους κινδύνους που σχετίζονται με το εμπόριο, αναλύοντας οικονομικούς δείκτες, ιστορικά δεδομένα και γεωπολιτικές τάσεις", "options": ["Σωστό", "Λάθος"], "correct": "Σωστό"},
        {"question": "Τα …...(1)…... χρησιμοποιούν …...(2)…... για …...(3)…...", "type": "fill_blanks", "blanks": [["Descriptive Analytics", "Prescriptive Analytics", "Cloud-based Platforms", "Predictive Analytics"], ["Big Data και AI-driven algorithms", "τεχνητή νοημοσύνη AI", "το Google BigQuery", "Machine Learning και AI"], ["την πρόβλεψη μελλοντικών γεγονότων", "να εστιάζουν στην ανάλυση του παρελθόντος", "την αποθήκευση δεδομένων και όχι για την ανάλυσή τους", "να δημιουργήσουν μοντέλα πρόβλεψης μελλοντικών τάσεων"]], "correct": ["Predictive Analytics", "Machine Learning και AI", "να δημιουργήσουν μοντέλα πρόβλεψης μελλοντικών τάσεων"]},
        {"question": "Επιλέξτε δύο (2) κατηγορίες προσωπικών δεδομένων.", "options": ["Ηλεκτρονική διεύθυνση", " Ανώνυμα δεδομένα", "Αριθμός μητρώου εταιρείας", "Διεύθυνση διαδικτυακού πρωτοκόλλου (IP)"], "correct": "Ηλεκτρονική διεύθυνση, Διεύθυνση διαδικτυακού πρωτοκόλλου (IP)"},
        {"question": "Οι Βοηθοί Τεχνητής Νοημοσύνης μπορούν να απαντούν σε ερωτήσεις χρηστών και να εκτελούν εντολές βάσει φυσικής γλώσσας.", "options": ["Σωστό", "Λάθος"], "correct": "Σωστό"},
        {"question": "Ποια πρόκληση σχετικά με το μέλλον της σύνταξης προτροπών θεωρείται από τους ειδικούς ως κρίσιμη για την υπεύθυνη χρήση της τεχνητής νοημοσύνης;", "options": ["Η μείωση των προτροπών από απλούς χρήστες", "Η πλήρης αυτοματοποίηση της απάντησης από τα μοντέλα", "Η ανάγκη για διαφάνεια και ανιχνευσιμότητα στις προτροπές", "Η απόκρυψη των προτροπών από το τελικό περιεχόμενο"], "correct": "Η ανάγκη για διαφάνεια και ανιχνευσιμότητα στις προτροπές"},
        {"question": "Η χρήση της ρομποτικής τεχνολογίας για την ανίχνευση θανατηφόρων και τοξικών χημικών ουσιών γίνεται με…", "options": ["ρομπότ ανίχνευσης χημικών ουσιών στο έδαφος και στον αέρα", "ρομπότ που διαχειρίζεται άλλες συσκευές ανίχνευσης χημικών ουσιών στο έδαφος και στον αέρα", "ρομπότ που συλλέγει δείγματα από το έδαφος και τον αέρα και αναλύονται αργότερα σε εξειδικευμένα εργαστήρια", "ρομπότ με θερμικές και φασματικές κάμερες"], "correct": "ρομπότ ανίχνευσης χημικών ουσιών στο έδαφος και στον αέρα"},
        {"question": "Το ChatGPT μπορεί να χρησιμοποιηθεί μόνο για απαντήσεις σε απλές ερωτήσεις γνώσης και δεν ενδείκνυται για δημιουργικές ή συνθετικές εργασίες.", "options": ["Σωστό", "Λάθος"], "correct": "Λάθος"},
        {"question": "Ποια από τις στρατηγικές αξιοποίησης της Τεχνητής Νοημοσύνης σε συνδυασμό με την ψηφιακή τεχνολογία θεωρείται εμπορική στρατηγική πρακτική και χρησιμοποιείται κυρίως στον ιδιωτικό και όχι στον δημόσιο τομέα;", "options": ["Ενίσχυση της ψηφιοποίησης των υπηρεσιών (e-Government)", "Χρήση ΤΝ για την διασφάλιση της διαφάνειας μεταξύ συστημάτων υπηρεσιών", "Παροχή προσωποποιημένων εμπειριών πελάτη μέσω ανάλυσης συμπεριφοράς", "Χρήση ΤΝ για την πρόληψη φαινομένων απάτης και διαφθοράς"], "correct": "Παροχή προσωποποιημένων εμπειριών πελάτη μέσω ανάλυσης συμπεριφοράς"},
        {"question": "Ποια από τις παρακάτω προτάσεις περιγράφει καλύτερα την έννοια της Τεχνητής Νοημοσύνης (ΤΝ);", "options": ["Η ΤΝ είναι η ικανότητα των μηχανών να αντιγράφουν χειρωνακτικές εργασίες", "Η ΤΝ αφορά την τεχνολογία αναπαραγωγής ήχου και εικόνας", "Η ΤΝ είναι η δυνατότητα ενός συστήματος να εκτελεί εργασίες που απαιτούν ανθρώπινη νοημοσύνη", "Η ΤΝ αναφέρεται αποκλειστικά στη ρομποτική τεχνολογία"], "correct": "Η ΤΝ είναι η δυνατότητα ενός συστήματος να εκτελεί εργασίες που απαιτούν ανθρώπινη νοημοσύνη"},
        {"question": "Οι τεχνολογίες …...(1)…..., όπως …...(2)…... χρησιμοποιούνται στα Advanced Analytics για την πρόβλεψη μελλοντικών τάσεων και την αυτοματοποίηση της λήψης αποφάσεων.", "type": "fill_blanks", "blanks": [["Big Data και AI-driven Algorithms", "Microsoft", "συστημάτων Cloud-based", "στατικών μοντέλων"], ["Machine Learning και Deep Learning", "Microsoft Excel και Microsoft Power BI", "Google BigQuery και Snowflake", "τα μοντέλα γραμμικής παλινδρόμησης"]], "correct": ["Big Data και AI-driven Algorithms", "Machine Learning και Deep Learning"]},
        {"question": "Ποιο από τα παρακάτω δεν αποτελεί τύπο Βοηθού Τεχνητής Νοημοσύνης;", "options": ["Ψηφιακοί προσωπικοί βοηθοί όπως η Siri και η Alexa", "Εφαρμογές συστάσεων όπως το Netflix και το Spotify", "Εικονικοί σύμβουλοι πελατών σε ιστοσελίδες", "Προγράμματα αυτόνομης πλοήγησης σε δορυφόρους GPS"], "correct": "Προγράμματα αυτόνομης πλοήγησης σε δορυφόρους GPS"},
        {"question": "Ποια ψηφιακή δεξιότητα θεωρείται κρίσιμη για την αξιολόγηση της αξιοπιστίας μιας διαδικτυακής πηγής πληροφοριών;", "options": ["Ικανότητα προγραμματισμού σε γλώσσες Python ή Java", "Ικανότητα κριτικής σκέψης και αξιολόγησης περιεχομένου", "Ικανότητα γρήγορης πληκτρολόγησης", "Ικανότητα χρήσης λογισμικού γραφικών"], "correct": "Ικανότητα κριτικής σκέψης και αξιολόγησης περιεχομένου"},
        {"question": "Ένα Μοντέλο Μηχανικής Μάθησης (Machine Learning Model) χρησιμοποιεί έναν ……(1)…… τύπο για να κάνει προβλέψεις σχετικά με ……(2)…… γεγονότα.", "type": "fill_blanks", "blanks": [["αλγεβρικό", "μαθηματικό", "μαθηματικό", "αλγεβρικό"], ["ασαφή", "ασαφή", "μελλοντικά", "μελλοντικά"]], "correct": ["μαθηματικό", "μελλοντικά"]},
        {"question": "Ποια από τις παρακάτω πρακτικές χρήσεις περιγράφει σωστά μια ενσωματωμένη λειτουργία πρόσθετου στο ChatGPT;", "options": ["Ανάλυση του συναισθηματικού περιεχομένου σε τραγούδια", "Κράτηση ξενοδοχείων σε πραγματικό χρόνο μέσω πρόσθετου όπως το Kayak ή το Expedia", "Δημιουργία βίντεο βασισμένων σε φωνητικές εντολές", "Ανάλυση φυσικοχημικών δεδομένων σε εργαστήρια"], "correct": "Κράτηση ξενοδοχείων σε πραγματικό χρόνο μέσω πρόσθετου όπως το Kayak ή το Expedia"},
        {"question": "Ποιο από τα παρακάτω ζεύγη αντιστοιχεί σωστά σε ένα όφελος και μία πρόκληση από τη χρήση ΤΝ στον κλάδο της φιλοξενίας;", "options": ["Όφελος: Αυτοματοποιημένη εξυπηρέτηση –Πρόκληση: Αυξημένο ενδιαφέρον των πελατών", "Όφελος: Μείωση χρόνου αναμονής – Πρόκληση: Κίνδυνοι ασφάλειας δεδομένων", "Όφελος: Μηδενική ανάγκη ανθρώπινου δυναμικού – Πρόκληση: Αύξηση κόστους προσωπικού", "Όφελος: Περιορισμός αυτονομίας πελάτη – Πρόκληση: Βελτίωση εμπειρίας επισκέπτη"], "correct": "Όφελος: Μείωση χρόνου αναμονής – Πρόκληση: Κίνδυνοι ασφάλειας δεδομένων"},
        {"question": "Ποια από τις παρακάτω είναι τυπική χρήση της Τεχνητής Νοημοσύνης για την υποστήριξη της λήψης αποφάσεων σε μια αγροτική εκμετάλλευση;", "options": ["Δημιουργία διαφημιστικών φυλλαδίων για αγροτικά προϊόντα", "Πρόβλεψη καιρικών συνθηκών με βάση ιστορικά δεδομένα", "Ανάπτυξη παραδοσιακών καλλιεργητικών πρακτικών χωρίς δεδομένα", "Επιλογή αγροτικής τεχνολογίας αποκλειστικά βάσει κόστους"], "correct": "Πρόβλεψη καιρικών συνθηκών με βάση ιστορικά δεδομένα"},
        {"question": "Ένα chatbot χρησιμοποιεί ………… για την κατανόηση και την ανταπόκριση στα μηνύματα των πελατών.", "options": ["προκαθορισμένα σενάρια", "τεχνητή νοημοσύνη (AI)", "προκαθορισμένα σενάρια και τεχνητή νοημοσύνη (AI)"], "correct": "προκαθορισμένα σενάρια και τεχνητή νοημοσύνη (AI)"},
        {"question": "Η \"Τεχνητή Νοημοσύνη\" (Artificial Intelligence) για να είναι ………… πρέπει να είναι σύννομη, δεοντολογική και στιβαρή καθ' όλο τον κύκλο ζωής του συστήματος.", "options": ["σύγχρονη", "αξιόπιστη", "εφαρμόσιμη", "κατανοητή"], "correct": "αξιόπιστη"},
        {"question": "Τι αποτελεί πλεονέκτημα της βιομηχανίας 4.0 για τις συνθήκες εργασίας των εργαζομένων;", "options": ["Η βελτίωσης εργονομίας χώρου εργασίας και μείωση σωματικής καταπόνησης", "Η αυτοματοποίηση μονότονων εργασιών", "Η εκπαίδευση και προσομοίωση επικίνδυνων ή πολύπλοκων εργασιών με χρήση εικονικής και επαυξημένης πραγματικότητας για εξοικείωση των εργαζομένων και μείωση εργατικών ατυχημάτων", "Όλα τα παραπάνω"], "correct": "Όλα τα παραπάνω"},
        {"question": "Ποια από τις παρακάτω συνεργασίες ανθρώπου-μηχανής εκφράζει την αρχή της \"παραμετροποίησης\";", "options": ["Ο βοηθός ΤΝ επιλέγει τις ενέργειες χωρίς επέμβαση του χρήστη", "Ο βοηθός λαμβάνει αποφάσεις μέσω τυχαίας επιλογής", "Ο χρήστης ρυθμίζει τις ειδοποιήσεις και τις εντολές βάσει των αναγκών του", "Η μηχανή εκπαιδεύεται αποκλειστικά από προγραμματιστές"], "correct": "Ο χρήστης ρυθμίζει τις ειδοποιήσεις και τις εντολές βάσει των αναγκών του"},
        {"question": "Τα δέντρα απόφασης δεν είναι από τους γνωστότερους αλγόριθμους της επιβλεπόμενης επαγωγικής μάθησης.", "options": ["Σωστό", "Λάθος"], "correct": "Λάθος"},
        
    ]

    root = tk.Tk()
    app = QuizGUI(root, quiz_questions)
    root.mainloop()