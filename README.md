# 🤖 AI Resume Classifier & Job Matcher

Build your own AI-powered resume screening tool to analyze resumes, predict suitable job roles, and compare them with job descriptions for better career alignment!

---

## 📌 Overview

This project is designed to automate resume screening by extracting important information (Skills, Experience, Education, rojects), predicting job roles, and checking alignment with job descriptions using similarity metrics.

---

## 🎯 Features

✅ Upload a PDF resume  
✅ Paste a job description  
✅ Predict suitable job role  
✅ Match JD with resume using Cosine Similarity  
✅ Show structured JSON output (Skills, Education, Experience, Projects)  
✅ Feedback when resume & JD do not align  
✅ Built with 🐍 Python and 📊 Streamlit

---

## **Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Venkatesh0610/Resume-Analyzer.git 
cd AI-Resume-Matcher
```

### **2️⃣ Install Required Libraries**  
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm

```

### **4️⃣ Run the Application**  
```bash
streamlit run app.py
```

---

## **🧠 How It Works**  


📄 **Upload a Resume (PDF format)**

📝 **Paste the Job Description** into the text area

⌨️ Press Ctrl + Enter to analyze

🔍 The app will:

- **Predict the most suitable Job Role**

-**Show a Match Score between resume and JD**

- **Output a Structured JSON (Skills, Education, Experience, Projects)**

- **Display ❌ Feedback if the resume and JD are not a good match**

---

## **🙋‍♀️ About Me**

I'm Vuggu Anusha, a postgraduate student pursuing MCA with a strong interest in Data Science, Artificial Intelligence, and Natural Language Processing.  
This project reflects my passion for building intelligent tools that solve real-world problems and was developed as part of my learning journey with Social Prachar.
