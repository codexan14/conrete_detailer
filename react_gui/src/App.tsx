import { useState, useEffect } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

type InputRowProps = {
  rowName: string;
  rowValue: number;
  onRowValueChange: Function;
  rowUnit: string;
};

function InputRow({ rowName, rowValue, onRowValueChange, rowUnit }: InputRowProps) {
  return (
    <tr>
      <td>{rowName}</td>
      <td>
        <input
          value={rowValue}
          onChange={(e) => onRowValueChange(e.target.value)} />
      </td>
      <td>{rowUnit}</td>
    </tr>
  );
}

function InputSection() {
  const [webWidth, setWebWidth] = useState(300)
  const [height, setHeight] = useState(600)
  const [concreteCompressionStrength, setConcreteCompressionStrength] = useState(28)
  const [topReinforcementArea, setTopReinforcementArea] = useState(0)
  const [topReinforcementCentroid, setTopReinforcementCentroid] = useState(70)
  const [bottomReinforcementArea, setBottomReinforcementArea] = useState(1014)
  const [bottomReinforcementCentroid, setBottomReinforcementCentroid] = useState(height - 70)
  const [steelMaxStrain, setSteelMaxStrain] = useState(0.0021)

  function handleSubmit() {
    alert;
  }
  return <div>
    <InputRow
      rowName='Web Width'
      rowValue={webWidth}
      onRowValueChange={setWebWidth}
      rowUnit='mm'
    />

    <InputRow
      rowName='Height'
      rowValue={height}
      onRowValueChange={setHeight}
      rowUnit='mm'
    />

    <InputRow
      rowName='Concrete Compression Strength'
      rowValue={concreteCompressionStrength}
      onRowValueChange={setConcreteCompressionStrength}
      rowUnit='MPa'
    />

    <InputRow
      rowName='Top Reinforcement Area'
      rowValue={topReinforcementArea}
      onRowValueChange={setTopReinforcementArea}
      rowUnit='mm2'
    />

    <InputRow
      rowName='Top Reinforcement Centroid'
      rowValue={topReinforcementCentroid}
      onRowValueChange={setTopReinforcementCentroid}
      rowUnit='mm'
    />

    <InputRow
      rowName='Bottom Reinforcement Area'
      rowValue={bottomReinforcementArea}
      onRowValueChange={setBottomReinforcementArea}
      rowUnit='mm2'
    />

    <InputRow
      rowName='Bottom Reinforcement Centroid'
      rowValue={bottomReinforcementCentroid}
      onRowValueChange={setBottomReinforcementCentroid}
      rowUnit='mm'
    />

    <InputRow
      rowName='Maximum Steel Strain'
      rowValue={steelMaxStrain}
      onRowValueChange={setSteelMaxStrain}
      rowUnit='-'
    />
    <button
      onSubmit={handleSubmit}>Send To Fast API</button>
  </div>
}

function OutputSection() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
    .then((res) => res.json())
    .then((data) => setMessage(data.Hello))
    .catch((error) => console.log(error))
  }
    , []);

  const [variable, setVariable] = useState("go");
  const [response, setResponse] = useState("");

  const handleCheck = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/trial", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({variable}),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.key);
    } catch (err) {
      console.error("Request failed:", err);
    }
  };

  const [secondVariable, setSecondVariable] = useState([1, 2, 3])
  const [secondMessage, setSecondMessage] = useState("No message")

  const handleSecondFunction = async () => {
    try {
      const response = await fetch("127.0.0.1:8000/third", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({variable: secondVariable}),
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setSecondMessage(data.key)

    } catch (err) {
      console.error("Request failed:", err);
    }
  } ;

  return (
    <div>
      <label>2</label>
      <button
        onClick={handleCheck}>OMG</button>
      <label>{message}</label>
      <button
        onClick={handleSecondFunction}>SecondCheck</button>
      <label>{secondMessage}</label>
      <label>{secondMessage}</label>
    </div>
  );
}

  export default function App() {
    return (
      <div>
        <h1>Beam Analizer</h1>
        <table>
          <td>
            <table>
              <h2> Input Section </h2>
              <InputSection />
            </table>
          </td>
          <td>
            <table>
              <h2> Output Section </h2>
              <OutputSection />
            </table>
          </td>
        </table>

      </div>
    );
  }