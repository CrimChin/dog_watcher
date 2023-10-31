#!/usr/bin/env node

// Connecting to ROS
var ROSLIB = require('roslib');

var ros = new ROSLIB.Ros({
  url : 'ws://localhost:9090'
});

ros.on('connection', function() {
console.log('Connected to websocket server.');
});

ros.on('error', function(error) {
console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
console.log('Connection to websocket server closed.');
});

// Publishing a Topic
// ------------------

let model_image = new ROSLIB.Topic({
  ros : ros,
  name : '/model_image',
  messageType : '/Image'
});

function renderVideo(message){
    
}

console.log("Publishing cmd_vel");
model_image.subscribe(renderVideo(message))


// const todoList = [];

// console.log("Hello World");
// let person_one = {
//     firstName: 'Chinedu',
//     lastName: 'Onyewuenyi',
//     age: 27
// }

// function createCircle(radius){
//     return {
//         radius,
//         draw: function(){
//             console.log('Draw');
//         }
//     };
// }

// function renderToDoList(){
//     let todoListHTML = '';
    
//     for (let i= 0; i < todoList.length; i++){
//         const todo = todoList[i];
//         const html = `
//             <p>
//                 ${todo} 
//                 <button onclick ="
//                     todoList.splice(${i},1);
//                     renderToDoList();        
//                 ">Delete</button> 
//             </p>
//         `
//         todoListHTML += html
//     }

//     document.querySelector('.js-todo-list')
//         .innerHTML = todoListHTML;
// }

// function addToDo() {
//     const inputElement = document.querySelector('.js-name-input');
//     const name = inputElement.value;
    
//     todoList.push(name);
//     console.log(todoList);
//     renderToDoList()
//     inputElement.value = ''
// }



// console.log(person_one.firstName)

// function streamVideo(person){
//     console.log('Hello'+ ' ' +person.firstName);

// }

// streamVideo(person_one)
