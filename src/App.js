import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';


function Message({ userMessage }) {
  const [response, setResponse] = useState(null)

  useEffect(() => {
    fetch(`api/message?message=${userMessage}`)
      .then(res => res.json())
      .then(json => setResponse(json.message))
  }, [])

  console.log(response)

  return (
    <div className='bg-gray-100 p-4 rounded-lg border-2 m-2'>
      <div className='bg-blue-100 text-xl p-2 rounded-lg'>&rarr; &emsp; {userMessage} </div>
      <div className='text-lg font-mono p-2'>&#11025; &emsp;{response || "Response is loading..."}</div>
    </div>
  )
}

function App() {

  const [interactions, setInteractions] = useState([])
  const [input, setInput] = useState(null)

  return (
    <div className="flex flex-col h-screen w-screen px-5 pb-5 space-y-2">
      <div className='bg-slate w-full flex flex-grow flex-col bg-slate-100 rounded py-1'>
        {interactions.map(i => <Message userMessage={i}></Message>)}
      </div>
      <div className='relative bottom-0 left-0 w-full h-16 bg-slate-200 border-4 border-slate-300 rounded-xl p-1'>
        <input value={input} onInput={e => setInput(e.target.value)} className='static left-1 top-1 h-12 rounded-sm bg-slate-50 focus:border-2 focus:border-cyan-100 w-full'></input>
        <button className='absolute right-1 top-1 h-12 rounded-lg bg-cyan-100 px-8 text-center uppercase hover:bg-cyan-200' onClick={() => {setInteractions(interactions.concat(input)); setInput("")}}>Send</button>
      </div>
    </div>  
  );
}

export default App;
