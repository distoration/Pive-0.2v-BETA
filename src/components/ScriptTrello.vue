<template>
  <div class="container">
    <h1 class="app-title">Pive</h1>
    <div class="calendar">
  
      <h2>Calendar</h2>
      <input type="date" v-model="selectedDate" @change="updateTasks">
    </div>
    <div class="general-description">
      <textarea v-model="generalDescription" placeholder="Write your general description here..."></textarea>
      <button class="save-button" @click="saveGeneralDescription(selectedDate)">SAVE</button>
    </div>
    <div class="task-list">
      <h2>My Tasks:</h2>
      
      <p :class="finishedTasksColor">TASKS FINISHED {{ numFinishedTasks }}/{{ tasks.length }}</p>
      <ul class="tasks">
        <li v-for="task in filteredTasks" :key="task.id" class="task-item">
          <div class="task-number">{{ task.number }}.</div>
          <div class="task-description">
            <input type="text" v-model="task.description" placeholder="Add a description">
            <input type="text" v-model="task.notes" placeholder="Description...">
            <div class="task-actions">
              <div v-if="!task.inProgress && !task.done">
                <button class="work-on-it" @click="startProgress(task)">Work on it!</button>
              </div>
              <div v-if="task.inProgress && !task.done">
                <button class="finish" @click="markAsComplete(task)">FINISH!</button>
                <button v-if="task.paused" class="resume" @click="continueTimer(task)">RESUME</button>
                <button v-else class="pause" @click="pauseTimer(task)">PAUSE</button>
              </div>
              <button v-if="!task.done" class="delete" @click="deleteTask(task)">DELETE TASK</button>
              <div class="timer">
                <span class="timer-icon">&#x23F1;</span>{{ task.timeElapsed }}
              </div>
            </div>
          </div>
          <div v-if="task.done" class="finished-task">TASK FINISHED</div>
          <div v-if="task.timeSpent > 0" class="time-spent">Time spent: {{ task.timeSpent }} seconds</div>
        </li>
      </ul>
      <div class="new-task">
        <input type="text" placeholder="Task name..." v-model="newTaskDescription" @keyup.enter="addTask">
        <button @click="addTask">ADD TASK</button>
      </div>
    </div>
    <div class="notification" v-if="notificationVisible">{{ notification }}</div>

  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid';

export default {
  name: "DirtyDesk",
  data() {
  return {
    generalDescription: "",
    generalDescriptions: {},
    selectedDate: new Date().toISOString().substr(0, 10),
    tasks: [],
    newTaskDescription: "",
    notification: "",
    notificationVisible: false,
  };
},

saveGeneralDescription(dateKey) {
  this.$set(this.generalDescriptions, dateKey, this.generalDescription);
  localStorage.setItem("generalDescriptions", JSON.stringify(this.generalDescriptions));
  localStorage.setItem("tasks", JSON.stringify(this.tasks));
  this.showNotification("General description has been saved");
},

  selectedDate(newValue, oldValue) {
    if (this.generalDescriptions[oldValue] !== this.generalDescription) {
      this.saveGeneralDescription(oldValue);
    }
    this.generalDescription = this.generalDescriptions[newValue] || "";
  },


  computed: {
    filteredTasks() {
      return this.tasks.filter((task) => task.date === this.selectedDate);
    },
    numFinishedTasks() {
      return this.tasks.filter((task) => task.done).length;
    },
    finishedTasksColor() {
    return this.numFinishedTasks === this.tasks.length ? 'green' : 'red';
  },
  },
  methods: {
    addTask() {
      if (this.newTaskDescription.trim() === "") return;
      const taskNumber = this.tasks.length + 1;
      const uuid = window.location.pathname.split('/').pop();
      const newTask = {
        id: Date.now(),
        number: taskNumber,
        description: this.newTaskDescription,
        notes: "",
        inProgress: false,
        paused: false,
        done: false,
        date: this.selectedDate,
        timeElapsed: 0,
        timeSpent: 0,
        interval: null,
        uuid: uuid,
      };
      this.tasks.push(newTask);
      this.newTaskDescription = "";

      
    },


    deleteTask(task) {
      const index = this.tasks.indexOf(task);
      if (index > -1) {
        this.tasks.splice(index, 1);
      }
    },
    startProgress(task) {
      task.inProgress = true;
      task.interval = setInterval(() => {
        task.timeElapsed += 1;
      }, 1000);
    },
    pauseTimer(task) {
      clearInterval(task.interval);
      task.paused = true;
    },
    continueTimer(task) {
      task.paused = false;
      task.interval = setInterval(() => {
        task.timeElapsed += 1;
      }, 1000);
    },
    markAsComplete(task) {
      clearInterval(task.interval);
      task.inProgress = false;
      task.done = true;
      task.timeSpent = task.timeElapsed;
    },
    updateTasks() {
  const uuid = window.location.pathname.split('/').pop();
  this.filteredTasks = this.tasks.filter((task) => task.date === this.selectedDate && task.uuid === uuid);
  this.generalDescription = this.generalDescriptions[this.selectedDate] || "";
},




mounted() {
  const storedGeneralDescriptions = localStorage.getItem("generalDescriptions");
  const storedTasks = localStorage.getItem("tasks");
  if (storedGeneralDescriptions) {
    this.generalDescriptions = JSON.parse(storedGeneralDescriptions);
    this.generalDescription = this.generalDescriptions[this.selectedDate] || "";
  }
  if (storedTasks) {
    this.tasks = JSON.parse(storedTasks);
  }
},





    

    created() {
      const uuid = uuidv4();
      const url = `${window.location.origin}/task-list/${uuid}`;
      console.log(`Your unique task list URL is: ${url}`);
    },

    showNotification(message) {
    this.notification = message;
    this.notificationVisible = true;
    setTimeout(() => {
      this.notificationVisible = false;
    }, 3000);
  },
    
  },

  watch: {
    selectedDate(newValue, oldValue) {
      if (this.generalDescriptions[oldValue] !== this.generalDescription) {
        this.saveGeneralDescription(oldValue);
      }
      this.generalDescription = this.generalDescriptions[newValue] || "";
    },
  },
};
</script>
<style>
/* Global styles */

.green {
  color: green;
}

.red {
  color: red;
}

.save-button {
  border: none;
  border-radius: 3px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #00bfff;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #0099cc;
}

body {
  font-family: Arial, sans-serif;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}



/* Calendar styles */
.calendar {
  margin-bottom: 1rem;
}

.calendar input[type="date"]::-webkit-inner-spin-button {
  display: none;
}

.calendar input[type="date"]::-webkit-calendar-picker-indicator {
  margin-right: 0.5rem;
  width: 20px;
  height: 20px;
  background-image: url(calendar.png);
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.6;
  cursor: pointer;
}

.calendar input[type="date"]::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

/* Task list styles */
.task-list {
  margin-top: 1rem;
}

.task-list h2 {
  margin-bottom: 0.5rem;
}

.task-list p {
  margin-bottom: 0.5rem;
}

.task-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 1rem;
}

.task-item:hover {
  background-color: #f5f5f5;
}

.task-number {
  margin-right: 0.5rem;
  font-size: 1.5rem;
  font-weight: bold;
}

.task-description {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.task-description input {
  margin-bottom: 0.5rem;
  padding: 0.25rem;
  border: none;
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  font-size: 1rem;
}

.task-description .work-on-it,
.task-description .finish,
.task-description .pause,
.task-description .resume,
.task-description .delete {
  border: none;
  border-radius: 3px;
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  cursor: pointer;
}

.task-description .work-on-it {
  background-color: #00bfff;
}

.task-description .work-on-it:hover {
  background-color: #0099cc;
}

.task-description .finish {
  background-color: #32cd32;
}

.task-description .finish:hover {
  background-color: #00cc00;
}

.task-description .pause {
  background-color: #ff8c00;
}

.task-description .pause:hover {
  background-color: #ff6600;
}

.task-description .resume {
  background-color: #ff8c00;
}

.task-description .resume:hover {
  background-color: #ff6600;
}

.task-description .delete {
  background-color: #ff0000;
  width: 100%;
}

.task-description .delete:hover {
  background-color: #cc0000;
}

.finished-task {
  font-size: 1.2rem;
  font-weight: bold;
  color: #32cd32;
  margin-right: 0.5rem;
}

.timer {
  margin-left: auto;
  padding: 0.25rem 0.5rem;
  font-size: 1rem;
  color: #333;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 3px;
  text-align: center;
}
.timer-icon {
    margin-right: 0.25rem;
  }

  .general-description {
  margin-bottom: 1rem;
}

.general-description textarea {
  width: 100%;
  height: 100px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 1rem;
  resize: vertical;
}

.time-spent {
  font-size: 1rem;
  color: #808080;
  margin-top: 0.5rem;
}

.new-task {
  display: flex;
  margin-top: 1rem;
}

.new-task input {
  margin-right: 0.5rem;
  padding: 0.25rem;
  border: none;
  border-radius: 3px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  font-size: 1rem;
  flex: 1;
}

.new-task button {
  border: none;
  border-radius: 3px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #00bfff;
  cursor: pointer;
}

.new-task button:hover {
  background-color: #0099cc;
}

.app-title {
  text-align: center;
  color: #111;
  border-bottom: 1px solid #111;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.notification {
  position: fixed;
  right: 1rem;
  top: 1rem;
  padding: 1rem;
  border-radius: 3px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #32cd32;
}

.work-on-it {
  width: 100%;
}
</style>
