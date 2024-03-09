import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';


import './App.css'

function App() {
  const [count, setCount] = useState()

  /*return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<Add_Todo></Add_Todo>}/>
        </Routes>
    </BrowserRouter>
  )*/
  return(
    <div id='main'>
      <div>
        <input id='Task' type='text' placeholder='Task'></input>
        <input id='Priority' type='text' placeholder='Priority'></input>
        <input id='Date' type='text' placeholder='Data'></input>
        <button onClick={addTodo}>ADD</button>
      </div>
    </div>
  )
}
async function addTodo(){
  let Task=document.getElementById('Task').value
  let Priority=document.getElementById('Priority').value
  let Date=document.getElementById('Date').value
  let val;
  const res=await axios.get(`http://localhost:5000/add_todo/${Task}/${Priority}/${Date}/null`);
  console.log(res.data);
  val=res.data
  console.log(val[0]['Priority']);
}
function Complete(){
  return(<h1>Completed</h1>)
}
export default App
