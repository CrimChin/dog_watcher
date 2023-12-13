#!/usr/bin/env node

// Connecting to ROS
var ros = new ROSLIB.Ros({
  url: 'ws://localhost:9090'
});

// Create an image viewer
var imageViewer = new ROSLIB.RosImage({
  ros: ros,
  topic: '/model_image', // Change this to the actual image topic
  queue_size: 1
});

// Get the image display element
var imageDisplay = document.getElementById('imageDisplay');

// Subscribe to the image topic
imageViewer.subscribe(function(message) {
  // Update the image display with the received image
  imageDisplay.src = 'data:image/jpeg;base64,' + message.data;
});

// Handle errors
imageViewer.on('error', function(error) {
  console.error('Error connecting to ROS:', error);
});

// Handle close events
imageViewer.on('close', function() {
  console.log('Connection to ROS closed.');
});



