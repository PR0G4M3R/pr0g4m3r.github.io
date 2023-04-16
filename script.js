let alertMsg = ['Hello There!', 'Welcome!', 'Hi!'];

window.alert(alertMsg[Math.floor(Math.random() * alertMsg.length)]);


document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 's') {
      scrollBy(0,35)
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key.toLowerCase() === 'w') {
      scrollBy(0,-35)
  }
});
