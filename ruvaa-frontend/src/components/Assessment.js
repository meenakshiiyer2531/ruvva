import React, { useState } from "react";

function Assessment() {
  const questions = [
    {
      text: "Do you enjoy solving logical problems?",
      options: [
        { text: "Yes", points: 2 },
        { text: "No", points: 0 },
      ],
    },
    {
      text: "Do you like creative arts?",
      options: [
        { text: "Yes", points: 2 },
        { text: "No", points: 0 },
      ],
    },
    {
      text: "Do you enjoy working in teams?",
      options: [
        { text: "Yes", points: 2 },
        { text: "No", points: 0 },
      ],
    },
  ];

  const [currentQ, setCurrentQ] = useState(0);
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);

  const handleAnswer = (points) => {
    setScore(score + points);
    if (currentQ + 1 < questions.length) {
      setCurrentQ(currentQ + 1);
    } else {
      setCompleted(true);
    }
  };

  return (
    <div className="assessment-page">
      {!completed ? (
        <div className="quiz-card">
          <h2>📝 Quick Assessment</h2>
          <p className="question">{questions[currentQ].text}</p>
          <div className="options">
            {questions[currentQ].options.map((opt, i) => (
              <button key={i} onClick={() => handleAnswer(opt.points)}>
                {opt.text}
              </button>
            ))}
          </div>
          <p className="progress">
            Question {currentQ + 1} of {questions.length}
          </p>
        </div>
      ) : (
        <div className="result-card">
          <h2>🎉 Assessment Completed!</h2>
          <p>Your total score is: <b>{score}</b></p>
          {score >= questions.length * 2 * 0.7 ? (
            <p>🌟 Great! You have strong interests in logic and creativity.</p>
          ) : (
            <p>👍 Keep exploring your interests and skills!</p>
          )}
          <button onClick={() => { setCurrentQ(0); setScore(0); setCompleted(false); }}>
            Restart
          </button>
        </div>
      )}

      <style>{`
        .assessment-page {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          width: 100%;
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #e0f7fa, #ffffff);
        }

        .quiz-card, .result-card {
          background: #ffffff;
          padding: 40px 50px;
          border-radius: 25px;
          box-shadow: 0 15px 40px rgba(0,0,0,0.2);
          text-align: center;
          max-width: 600px;
          width: 90%;
          transition: 0.3s;
        }

        h2 {
          margin-bottom: 25px;
          color: #0077b6;
        }

        .question {
          font-size: 1.3rem;
          margin-bottom: 20px;
        }

        .options {
          display: flex;
          justify-content: center;
          gap: 20px;
          flex-wrap: wrap;
        }

        button {
          padding: 12px 28px;
          background: #00b4d8;
          color: white;
          border: none;
          border-radius: 20px;
          font-size: 1rem;
          cursor: pointer;
          font-weight: bold;
          transition: 0.3s;
        }

        button:hover {
          background: #0077b6;
          transform: translateY(-2px) scale(1.05);
          box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        .progress {
          margin-top: 15px;
          font-size: 0.9rem;
          color: #555;
        }

        .result-card p {
          font-size: 1.1rem;
          margin: 15px 0;
        }

        @media(max-width:768px){
          .quiz-card, .result-card { padding: 30px 25px; }
          .question { font-size: 1.1rem; }
          button { padding: 10px 20px; font-size: 0.95rem; }
        }
      `}</style>
    </div>
  );
}

export default Assessment;
