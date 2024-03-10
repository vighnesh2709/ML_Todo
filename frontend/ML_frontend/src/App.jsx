import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function TodoComponent({ tasks }) {
  return (
    <div>
      {tasks.map((task, index) => (
        <li key={index}>
          Task: {task.Task}, Finish Date: {task.Finish_Date}, Priority: {task.Priority}
        </li>
      ))}
    </div>
  );
}

function addTodo(setTasks) {
  return async () => {
    let task_1 = document.getElementById('Task').value;
    let priority = document.getElementById('Priority').value;
    let date = document.getElementById('Date').value;

    const res = await axios.get(`http://localhost:5000/add_todo/${task_1}/${priority}/${date}/null`);
    const newTasks = res.data;
    setTasks(newTasks);
  };
}

function App() {
  const [tasks, setTasks] = useState([]);

  const handleAddTodo = addTodo(setTasks);

  return (
    <div id='main'>
      <div>
        <input id='Task' type='text' placeholder='Task'></input>
        <input id='Priority' type='text' placeholder='Priority'></input>
        <input id='Date' type='text' placeholder='Date'></input>
        <button onClick={handleAddTodo}>ADD</button>
      </div>
      <div>
        <TodoComponent tasks={tasks} />
      </div>
    </div>
  );
}

export default App;
