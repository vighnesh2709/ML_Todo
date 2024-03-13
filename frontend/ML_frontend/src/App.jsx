import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function TodoComponent({ tasks, setTasks }) {
  useEffect(() => {
    console.log(tasks);
  }, [tasks]);

  return (
    <div>
      {tasks.map((task, index) => (
        <div key={index} id={task.ID}>
          ID: {task.ID}, Task: {task.Task}, Finish Date: {task.Finish_Date}, Priority: {task.Priority} pred:{task.Prediction}
          <button onClick={() => completed(task.ID, task.Task, task.Finish_Date)}>completed</button> 
        </div>
      ))}
    </div>
  );
}

async function completed(id, Task, Date) {
  console.log(id);
  console.log(Task);
  console.log(Date);
  try {
    await axios.get(`http://localhost:5000/completed/${Task}/${Date}/${id}`);
  } catch (error) {
    console.error(error);
  }
}

function addTodo(setTasks, tasks) {
  return async () => {
    let task_1 = document.getElementById('Task').value;
    let priority = document.getElementById('Priority').value;
    let date = document.getElementById('Date').value;

    try {
      const res = await axios.post(`http://localhost:5000/add_todo/${task_1}/${priority}/${date}/null`);
      const pred = await axios.get(`http://localhost:5000/${priority}/${date}`);
      const pred_value = pred.data; 
    } catch (error) {
      console.error(error);
    }
  };
}

function App() {
  const [tasks, setTasks] = useState([]);

  const handleAddTodo = addTodo(setTasks, tasks);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await axios.get('http://localhost:5000/get_tasks');
        setTasks(res.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchTasks();
  }, []);

  useEffect(() => {
    const fetchUpdatedTasks = async () => {
      try {
        const res = await axios.get('http://localhost:5000/get_tasks');
        setTasks(res.data);
      } catch (error) {
        console.error(error);
      }
    };

    // Use this effect to update tasks when setTasks is called
    fetchUpdatedTasks();
  }, [tasks]);

  return (
    <div id='main'>
      <div>
        <input id='Task' type='text' placeholder='Task'></input>
        <input id='Priority' type='text' placeholder='Priority'></input>
        <input id='Date' type='text' placeholder='Date'></input>
        <button onClick={handleAddTodo}>ADD</button>
      </div>
      <div>
        <TodoComponent tasks={tasks} setTasks={setTasks} />
      </div>
    </div>
  );
}

export default App;
