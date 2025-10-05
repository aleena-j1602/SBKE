const background = document.querySelector('.background');

for (let i = 0; i < 50; i++) {
  const dot = document.createElement('div');
  dot.classList.add('particle');
  dot.style.left = `${Math.random() * 100}%`;
  dot.style.top = `${Math.random() * 100}%`;
  dot.style.animationDuration = `${5 + Math.random() * 15}s`;
  background.appendChild(dot);
}