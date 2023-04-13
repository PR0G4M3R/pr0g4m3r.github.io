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