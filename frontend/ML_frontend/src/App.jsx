import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function TodoComponent({ tasks }) {
  useEffect(()=>{
    console.log(tasks)
  },[tasks])

   return (
      <div>
        {tasks.map((task, index) => (
          <div key={index} id={task.ID}>
            ID:{task.ID} Task: {task.Task}, Finish Date: {task.Finish_Date}, Priority: {task.Priority}
            <button onClick={()=>{completed(task.ID,task.Task,task.Finish_Date)}}>completed</button>
          </div>
        ))}
      </div>
    );
  
}

function completed(id,Task,Date){
  console.log(id)
  console.log(Task)
  console.log(Date)
  axios.get(`http://localhost:5000/completed/${Task}/${Date}/${id}`)
  .then((res)=>{
    console.log(res.date)
  })
  
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

  useEffect(() => {
    
    const fetchTasks = async () => {
      const res = await axios.get('http://localhost:5000/get_tasks');
      setTasks(res.data);
    };

    fetchTasks();
  }, []); 

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
