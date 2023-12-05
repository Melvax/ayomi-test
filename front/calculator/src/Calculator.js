import React, { useState } from 'react';

const Calculator = () => {
  const [result, setResult] = useState("");
  const [operations, setOperations] = useState("");

  const handleClick = (e) => setResult(result.concat(e.target.name));
  const clear = () => setResult("");

  const calculate = async () => {
    try {
      const res = await fetch('http://localhost:8001/calculate', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression: result }),
      });
      const data = await res.json();
      setResult(data.result);
      retrieveOperations();
    } catch(err) {
      setResult("Error");
    }
  }

  const retrieveOperations = async () => {
    try {
      const res = await fetch('http://localhost:8001/operations/csv');
      const data = await res.text();
      setOperations(data);
    } catch(err) {
      console.error(err);
    }
  }

  return (
    <div className="container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div className="calculator" style={{ fontSize: '2em' }}>
        <form>
          <input type="text" value={result} style={{ width: '100%', height: '2em' }} />
        </form>
        <div style={{ height: '10px' }}></div>

        <div className="keypad" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
          {['7', '8', '9', '4', '5', '6', '1', '2', '3'].map(num => 
            <button key={num} name={num} onClick={handleClick}>{num}</button>
          )}
        </div>
        {['+', '-', '*', '/', ' '].map(op => 
          <button key={op} name={op} onClick={handleClick}>{op === ' ' ? 'Space' : op}</button>
        )}
        <br/>
        <button name="0" onClick={handleClick}>0</button>
        <button onClick={clear} id="clear">Clear</button>
        <button onClick={calculate} id="result">=</button>
        <br/>
        <button onClick={retrieveOperations} id="retrieve">Retrieve Operations</button>
          
        <pre style={{ fontSize: '0.3em' }}>{operations}</pre>
        </div>


      </div>
  );
};

export default Calculator;