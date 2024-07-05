import React, { useState, useEffect } from 'react';

const Problem = () => {
  const [difficulty, setDifficulty] = useState('beginner');
  const [answer, setAnswer] = useState('');
  const [problemData, setProblemData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/problems')
      .then(response => response.json())
      .then(data => setProblemData(data))
      .catch(error => console.error(error));
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (answer.includes('Modus Ponens')) {
      alert('Correct answer!');
    }
  };

  if (!problemData) {
    return <div>Loading...</div>;
  }

  return (
    <div id="problem">
      <h2>Practice Problem: Rules of Inference</h2>
      <h3>Problem Statement</h3>
      <p>Use the rules of inference to prove the following argument:</p>
      <div>
        <p>Premises:</p>
        <ul>
          {problemData.premises.map((premise, index) => (
            <li key={index}>{premise}</li>
          ))}
        </ul>
        <p>Conclusion:</p>
        <p>{problemData.solution[problemData.solution.length - 1]}</p>
      </div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="difficulty">Difficulty:</label>
        <select id="difficulty" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <label htmlFor="answer">Your Answer:</label>
        <textarea id="answer" required value={answer} onChange={e => setAnswer(e.target.value)}></textarea>
        <button type="submit">Submit Answer</button>
      </form>
    </div>
  );
};

export default Problem;